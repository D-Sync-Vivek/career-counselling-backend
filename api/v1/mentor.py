import base64
import logging
import os
from datetime import datetime, timedelta, time, date, timezone
from uuid import UUID
from typing import List, Optional

import httpx
from fastapi import (
    APIRouter, Depends, HTTPException, Query,
    WebSocket, WebSocketDisconnect, status
)
from jose import jwt, JWTError
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from langchain_huggingface import HuggingFaceEmbeddings

from core.database import get_db
from core.security import SECRET_KEY, ALGORITHM
from api.deps import get_current_user
from models.users import User, UserRole
from models.mentorship import (
    Mentor, SessionLog, ChatMessage, MentorshipRequest
)

IST = timezone(timedelta(hours=5, minutes=30))

# ── Dyte Configuration ────────────────────────────────────────────────────────
DYTE_ORG_ID = os.getenv("DYTE_ORG_ID", "")
DYTE_API_KEY = os.getenv("DYTE_API_KEY", "")
DYTE_BASE_URL = "https://api.dyte.io/v2"

def _dyte_headers() -> dict:
    token = base64.b64encode(f"{DYTE_ORG_ID}:{DYTE_API_KEY}".encode()).decode()
    return {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["Mentorship"])

# Semantic Search Model
embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# ── Connection Manager ──────────────────────────────────────────────────────

class ConnectionManager:
    def __init__(self):
        self._rooms: dict[str, set[WebSocket]] = {}

    async def connect(self, room: str, ws: WebSocket):
        if room not in self._rooms:
            self._rooms[room] = set()
        self._rooms[room].add(ws)

    def disconnect(self, room: str, ws: WebSocket):
        if room in self._rooms:
            self._rooms[room].discard(ws)
            if not self._rooms[room]:
                del self._rooms[room]

    async def broadcast(self, room: str, payload: dict):
        if room in self._rooms:
            for ws in self._rooms[room]:
                try:
                    await ws.send_json(payload)
                except Exception:
                    pass

manager = ConnectionManager()

# ── SCHEMAS ────────────────────────────────────────────────────────────────

class MentorResponse(BaseModel):
    id: UUID
    user_id: UUID
    full_name: Optional[str] = None
    expertise: str
    bio: Optional[str] = None
    years_experience: int
    rating: float
    is_verified: bool
    class Config:
        from_attributes = True

class MentorProfileIn(BaseModel):
    expertise: str
    bio: Optional[str] = None
    years_experience: int = 0

class ConnectionRequestIn(BaseModel):
    mentor_id: UUID
    message: Optional[str] = None

class StudentProfileSnapshot(BaseModel):
    student_id: UUID
    full_name: Optional[str]
    apti_data: Optional[dict]
    personality_data: Optional[dict]
    academic_data: Optional[dict]
    aspiration_data: Optional[dict]

class PendingConnectionResponse(BaseModel):
    request_id: UUID
    student_id: UUID
    student_name: Optional[str]
    message: Optional[str]
    created_at: datetime
    request_type: str

class UpcomingSessionResponse(BaseModel):
    session_id: UUID
    scheduled_at: datetime
    other_party_name: str
    other_user_id: Optional[UUID]
    is_live: bool
    seconds_until_start: int

# ✅ NEW: Schema for the Instant Session trigger
class InstantSessionIn(BaseModel):
    delay_minutes: int = Field(default=0, ge=0, description="0 for instant, 60 for 1 hour")
    topic: str = Field(default="Open Mentorship Session")

# ── PROFILE & SEARCH ──────────────────────────────────────────────────────

@router.post("/profiles/mentors/", status_code=201)
def create_mentor_profile(body: MentorProfileIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.MENTOR:
        raise HTTPException(status_code=403, detail="Mentor role required.")
    
    try:
        vector = embed_model.embed_query(body.expertise)
        mentor = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
        
        if mentor:
            mentor.expertise = body.expertise
            mentor.expertise_vector = vector
            mentor.bio = body.bio
            mentor.years_experience = body.years_experience
            message = "AI-indexed profile updated."
        else:
            mentor = Mentor(
                user_id=current_user.id,
                expertise=body.expertise,
                expertise_vector=vector,
                bio=body.bio,
                years_experience=body.years_experience,
                is_verified=True
            )
            db.add(mentor)
            message = "AI-indexed profile created."
        
        db.commit()
        return {"message": message}
    except Exception as e:
        db.rollback()
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/profiles/mentors/me", response_model=MentorResponse)
def get_my_mentor_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.MENTOR:
        raise HTTPException(status_code=403, detail="Mentor role required.")
        
    mentor = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor profile not found.")
        
    return {
        "id": mentor.id,
        "user_id": mentor.user_id,
        "expertise": mentor.expertise,
        "rating": mentor.rating,
        "is_verified": mentor.is_verified,
        "bio": mentor.bio,
        "years_experience": mentor.years_experience,
        "full_name": current_user.full_name
    }

@router.get("/mentorship/search/", response_model=List[MentorResponse])
def search_mentors(career_goal: str = Query(...), db: Session = Depends(get_db)):
    search_vector = embed_model.embed_query(career_goal)
    results = (
        db.query(Mentor)
        .options(joinedload(Mentor.user))
        .filter(Mentor.is_verified == True)
        .order_by(Mentor.expertise_vector.cosine_distance(search_vector))
        .limit(10).all()
    )
    return [
        MentorResponse(
            id=m.id,
            user_id=m.user_id,
            full_name=m.user.full_name if m.user else None,
            expertise=m.expertise,
            bio=m.bio,
            years_experience=m.years_experience,
            rating=m.rating,
            is_verified=m.is_verified,
        )
        for m in results
    ]

@router.get("/mentorship/mentors/{mentor_id}", response_model=MentorResponse)
def get_mentor_detail(mentor_id: UUID, db: Session = Depends(get_db)):
    mentor = (
        db.query(Mentor)
        .options(joinedload(Mentor.user))
        .filter(Mentor.id == mentor_id)
        .first()
    )
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found.")
    return MentorResponse(
        id=mentor.id,
        user_id=mentor.user_id,
        full_name=mentor.user.full_name if mentor.user else None,
        expertise=mentor.expertise,
        bio=mentor.bio,
        years_experience=mentor.years_experience,
        rating=mentor.rating,
        is_verified=mentor.is_verified,
    )


# ── BROADCAST SESSIONS (The New Architecture) ─────────────────────────────────

@router.post("/sessions/broadcast", status_code=201)
async def broadcast_instant_session(body: InstantSessionIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Mentor creates an instant or delayed session for all connected students."""
    mentor = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
    if not mentor:
        raise HTTPException(status_code=403, detail="Only mentors can broadcast sessions.")

    now = datetime.now(IST).replace(tzinfo=None)
    scheduled_time = now + timedelta(minutes=body.delay_minutes)

    dyte_meeting_id = None
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{DYTE_BASE_URL}/meetings",
                json={"title": f"{body.topic} - {current_user.full_name}"},
                headers=_dyte_headers(),
                timeout=10.0
            )
            resp.raise_for_status()
            dyte_meeting_id = resp.json()["data"]["id"]
    except Exception as e:
        logger.error(f"Dyte meeting creation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to initialize video server.")

    # Student ID is None because this is a broadcast
    session = SessionLog(
        student_id=None, 
        mentor_id=mentor.id,
        scheduled_at=scheduled_time,
        status="scheduled",
        dyte_meeting_id=dyte_meeting_id
    )
    db.add(session)
    db.commit()

    return {
        "message": "Broadcast scheduled!",
        "session_id": session.id,
        "scheduled_at": session.scheduled_at,
        "starts_in_seconds": body.delay_minutes * 60
    }


@router.get("/sessions/upcoming", response_model=List[UpcomingSessionResponse])
def get_upcoming_sessions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    If Mentor: Shows their active broadcasts.
    If Student: Shows active broadcasts from their connected Mentors.
    """
    now = datetime.now(IST).replace(tzinfo=None)
    res = []

    mentor_profile = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
    
    if mentor_profile:
        # Mentor View
        sessions = db.query(SessionLog).filter(
            SessionLog.mentor_id == mentor_profile.id,
            SessionLog.status == "scheduled",
            SessionLog.scheduled_at >= (now - timedelta(hours=2))
        ).order_by(SessionLog.scheduled_at.asc()).all()

        for s in sessions:
            sch_naive = s.scheduled_at.replace(tzinfo=None)
            res.append({
                "session_id": s.id, 
                "scheduled_at": sch_naive,
                "other_party_name": "Your Connected Students",
                "other_user_id": None,
                "is_live": now >= (sch_naive - timedelta(minutes=5)),
                "seconds_until_start": int((sch_naive - now).total_seconds())
            })
        return res

    elif current_user.role == UserRole.STUDENT:
        # Student View: Get ONLY sessions from connected mentors
        connected_mentors = db.query(MentorshipRequest.mentor_id).filter(
            MentorshipRequest.student_id == current_user.id,
            MentorshipRequest.status == "accepted",
            MentorshipRequest.request_type == "connection"
        ).subquery()

        sessions = db.query(SessionLog).filter(
            SessionLog.mentor_id.in_(connected_mentors),
            SessionLog.status == "scheduled",
            SessionLog.scheduled_at >= (now - timedelta(hours=2))
        ).order_by(SessionLog.scheduled_at.asc()).all()

        for s in sessions:
            mentor_user = db.query(User).join(Mentor).filter(Mentor.id == s.mentor_id).first()
            sch_naive = s.scheduled_at.replace(tzinfo=None)
            res.append({
                "session_id": s.id, 
                "scheduled_at": sch_naive,
                "other_party_name": mentor_user.full_name if mentor_user else "Mentor",
                "other_user_id": mentor_user.id if mentor_user else None,
                "is_live": now >= (sch_naive - timedelta(minutes=5)),
                "seconds_until_start": int((sch_naive - now).total_seconds())
            })
        return res

    return []


@router.post("/sessions/{session_id}/join-video")
async def join_video_session(session_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(SessionLog).filter(SessionLog.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    is_mentor = False
    is_authorized_student = False

    mentor_profile = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
    
    if mentor_profile and session.mentor_id == mentor_profile.id:
        is_mentor = True
    elif current_user.role == UserRole.STUDENT:
        # Check if student is connected to this mentor
        connection = db.query(MentorshipRequest).filter(
            MentorshipRequest.student_id == current_user.id,
            MentorshipRequest.mentor_id == session.mentor_id,
            MentorshipRequest.status == "accepted"
        ).first()
        if connection:
            is_authorized_student = True

    if not is_mentor and not is_authorized_student:
        raise HTTPException(status_code=403, detail="You must be connected to this mentor to join their broadcast.")

    if not session.dyte_meeting_id:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{DYTE_BASE_URL}/meetings",
                    json={"title": f"Mentorship Session - {session_id}"},
                    headers=_dyte_headers(),
                    timeout=10.0,
                )
                resp.raise_for_status()
                session.dyte_meeting_id = resp.json()["data"]["id"]
                db.commit()
        except Exception as e:
            logger.error(f"Dyte meeting creation failed on join: {e}")
            raise HTTPException(status_code=500, detail="Could not create video meeting. Check Dyte credentials.")

    preset_name = "group_call_host" if is_mentor else "group_call_participant"

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{DYTE_BASE_URL}/meetings/{session.dyte_meeting_id}/participants",
                json={
                    "name": current_user.full_name,
                    "custom_participant_id": str(current_user.id),
                    "preset_name": preset_name,
                },
                headers=_dyte_headers(),
                timeout=10.0
            )
            resp.raise_for_status()
            participant_token = resp.json()["data"]["token"]
    except Exception as e:
        logger.error(f"Dyte participant token generation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate video token.")

    return {"token": participant_token, "meeting_id": session.dyte_meeting_id}


@router.post("/sessions/{session_id}/end")
async def end_session(session_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(SessionLog).filter(SessionLog.id == session_id).first()
    mentor = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
    if not session or session.mentor_id != mentor.id:
        raise HTTPException(status_code=403)

    session.status = "completed"
    db.commit()
    await manager.broadcast(str(session_id), {"event": "SESSION_ENDED", "message": "Concluded.", "session_id": str(session_id)})
    return {"message": "Session completed."}


# ── CHAT & REAL-TIME ──────────────────────────────────────────────────────

@router.websocket("/mentorship/chat/{other_user_id}/")
async def websocket_chat(
    websocket: WebSocket,
    other_user_id: UUID,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if not user_email:
            raise JWTError
    except JWTError:
        return

    user = db.query(User).filter(User.email == user_email).first()
    other_user = db.query(User).filter(User.id == other_user_id).first()
    if not user or not other_user:
        return

    current_mentor = db.query(Mentor).filter(Mentor.user_id == user.id).first()
    other_mentor = db.query(Mentor).filter(Mentor.user_id == other_user_id).first()

    if current_mentor and not other_mentor:
        mentor_profile_id = current_mentor.id
        student_user_id = other_user_id
    elif other_mentor and not current_mentor:
        mentor_profile_id = other_mentor.id
        student_user_id = user.id
    else:
        await websocket.accept()
        await websocket.send_json({"event": "ERROR", "message": "Could not resolve mentor/student relationship."})
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    approved = db.query(MentorshipRequest).filter(
        MentorshipRequest.student_id == student_user_id,
        MentorshipRequest.mentor_id == mentor_profile_id,
        MentorshipRequest.status.in_(["approved", "accepted"])
    ).first()
    if not approved:
        await websocket.accept()
        await websocket.send_json({"event": "ERROR", "message": "No approved mentorship relationship found."})
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    ids = sorted([str(user.id), str(other_user_id)])
    room = f"{ids[0]}_{ids[1]}"

    await websocket.accept()
    await manager.connect(room, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            msg_text = data.get("message", "").strip()
            if msg_text:
                try:
                    new_msg = ChatMessage(
                        student_id=student_user_id,
                        mentor_id=mentor_profile_id,
                        sender_id=user.id,
                        message=msg_text
                    )
                    db.add(new_msg)
                    db.commit()
                    await manager.broadcast(room, {
                        "event": "NEW_MESSAGE",
                        "sender_id": str(user.id),
                        "sender": user.full_name,
                        "message": msg_text,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
                except Exception as e:
                    db.rollback()
                    logger.error(f"Persistence Failure: {e}")

    except WebSocketDisconnect:
        manager.disconnect(room, websocket)
    except Exception as e:
        logger.error(f"WebSocket Runtime Error: {e}")
        manager.disconnect(room, websocket)


# ── CONNECTION REQUESTS (no availability required) ────────────────────────────

@router.post("/connections/request", status_code=201)
def send_connection_request(body: ConnectionRequestIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Student role required.")

    mentor = db.query(Mentor).filter(Mentor.id == body.mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found.")

    existing = db.query(MentorshipRequest).filter(
        MentorshipRequest.student_id == current_user.id,
        MentorshipRequest.mentor_id == body.mentor_id,
        MentorshipRequest.request_type == "connection",
        MentorshipRequest.status.in_(["pending", "accepted"])
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="A connection request already exists with this mentor.")

    new_req = MentorshipRequest(
        student_id=current_user.id,
        mentor_id=body.mentor_id,
        availability_id=None,
        message=body.message,
        status="pending",
        request_type="connection"
    )
    db.add(new_req)
    db.commit()
    return {"message": "Connection request sent.", "request_id": str(new_req.id)}

@router.get("/mentors/requests/pending")
def get_pending_connection_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    mentor = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
    if not mentor:
        raise HTTPException(status_code=403, detail="Mentor profile not found.")

    pending = (
        db.query(MentorshipRequest, User)
        .join(User, MentorshipRequest.student_id == User.id)
        .filter(
            MentorshipRequest.mentor_id == mentor.id,
            MentorshipRequest.request_type == "connection",
            MentorshipRequest.status == "pending"
        )
        .order_by(MentorshipRequest.created_at.desc())
        .all()
    )

    result = []
    for req, student in pending:
        result.append({
            "request_id": req.id,
            "student_id": student.id,
            "student_name": student.full_name,
            "message": req.message,
            "created_at": req.created_at,
            "request_type": req.request_type,
            "student_snapshot": {
                "apti_data": student.apti_data or {},
                "personality_data": student.personality_data or {},
                "academic_data": student.academic_data or {},
                "aspiration_data": student.aspiration_data or {},
            }
        })
    return result

@router.get("/mentors/students/{student_id}/profile")
def get_student_profile_for_mentor(student_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    mentor = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
    if not mentor:
        raise HTTPException(status_code=403, detail="Mentor profile not found.")

    link = db.query(MentorshipRequest).filter(
        MentorshipRequest.student_id == student_id,
        MentorshipRequest.mentor_id == mentor.id,
        MentorshipRequest.request_type == "connection",
        MentorshipRequest.status.in_(["pending", "accepted"])
    ).first()
    if not link:
        raise HTTPException(status_code=403, detail="No connection request found for this student.")

    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    return {
        "student_id": student.id,
        "full_name": student.full_name,
        "apti_data": student.apti_data or {},
        "personality_data": student.personality_data or {},
        "academic_data": student.academic_data or {},
        "aspiration_data": student.aspiration_data or {},
        "lifestyle_data": student.lifestyle_data or {},
    }

@router.patch("/connections/{request_id}/accept")
def accept_connection_request(request_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    mentor = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
    if not mentor:
        raise HTTPException(status_code=403, detail="Mentor profile not found.")

    req = db.query(MentorshipRequest).filter(
        MentorshipRequest.id == request_id,
        MentorshipRequest.mentor_id == mentor.id,
        MentorshipRequest.request_type == "connection"
    ).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found.")
    if req.status != "pending":
        raise HTTPException(status_code=400, detail=f"Request is already '{req.status}'.")

    req.status = "accepted"
    db.commit()
    return {"message": "Connection accepted. Chat is now enabled.", "request_id": str(req.id)}

@router.patch("/connections/{request_id}/reject")
def reject_connection_request(request_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    mentor = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
    if not mentor:
        raise HTTPException(status_code=403, detail="Mentor profile not found.")

    req = db.query(MentorshipRequest).filter(
        MentorshipRequest.id == request_id,
        MentorshipRequest.mentor_id == mentor.id,
        MentorshipRequest.request_type == "connection"
    ).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found.")

    req.status = "rejected"
    db.commit()
    return {"message": "Connection request rejected.", "request_id": str(req.id)}