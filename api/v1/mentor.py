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
    Mentor, MentorAvailability, SessionLog,
    ChatMessage, MentorshipRequest
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
# Semantic Search Model
embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# ── Utilities ──────────────────────────────────────────────────────────────

def get_next_weekday(start_date: date, weekday: int):
    days_ahead = (weekday - 1) - start_date.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)

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

class AvailabilitySlotResponse(BaseModel):
    id: UUID
    mentor_id: UUID
    day_of_week: int
    start_time: str
    end_time: str
    is_booked: bool
    class Config:
        from_attributes = True

class MentorProfileIn(BaseModel):
    expertise: str
    bio: Optional[str] = None
    years_experience: int = 0

class AvailabilitySlotIn(BaseModel):
    day_of_week: int = Field(..., ge=1, le=7)
    start_time: time
    end_time: time

class MentorAvailabilityUpdate(BaseModel):
    slots: List[AvailabilitySlotIn]

class RequestIn(BaseModel):
    mentor_id: UUID
    availability_id: UUID
    message: Optional[str] = None

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
        
    # FIX: Return a dictionary that injects the full_name from current_user
    return {
        "id": mentor.id,
        "user_id": mentor.user_id,
        "expertise": mentor.expertise,
        "rating": mentor.rating,
        "is_verified": mentor.is_verified,
        "bio": mentor.bio,
        "years_experience": mentor.years_experience,
        "full_name": current_user.full_name  # <-- Grabbed directly from auth!
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

# ── AVAILABILITY & SESSIONS ───────────────────────────────────────────────

@router.post("/availability/", status_code=201)
def set_mentor_availability(body: MentorAvailabilityUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.MENTOR:
        raise HTTPException(status_code=403)
    mentor = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
    if not mentor:
        raise HTTPException(status_code=404)

    db.query(MentorAvailability).filter(
        MentorAvailability.mentor_id == mentor.id,
        MentorAvailability.is_booked == False
    ).delete()

    now = datetime.now(IST).replace(tzinfo=None)
    today = now.date()
    today_weekday = today.weekday() + 1

    new_slots = []
    for slot in body.slots:
        if slot.day_of_week == today_weekday:
            slot_date = today
            earliest_start = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
            effective_start = max(datetime.combine(slot_date, slot.start_time), earliest_start)
        else:
            days_ahead = (slot.day_of_week - 1) - today.weekday()
            if days_ahead < 0: days_ahead += 7
            slot_date = today + timedelta(days=days_ahead)
            effective_start = datetime.combine(slot_date, slot.start_time)

        actual_end = datetime.combine(slot_date, slot.end_time)
        if effective_start + timedelta(hours=1) > actual_end: continue

        current_start = effective_start
        while current_start + timedelta(hours=1) <= actual_end:
            new_slots.append(MentorAvailability(
                mentor_id=mentor.id,
                day_of_week=slot.day_of_week,
                start_time=current_start.time(),
                end_time=(current_start + timedelta(hours=1)).time()
            ))
            current_start += timedelta(hours=1)

    db.add_all(new_slots)
    db.commit()
    return {"message": f"Created {len(new_slots)} slots."}

@router.get("/sessions/upcoming", response_model=List[UpcomingSessionResponse])
def get_upcoming_sessions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    now = datetime.now(IST).replace(tzinfo=None)
    mentor_profile = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
    mentor_id = mentor_profile.id if mentor_profile else None

    sessions = db.query(SessionLog).filter(
        or_(SessionLog.student_id == current_user.id, SessionLog.mentor_id == mentor_id),
        SessionLog.status == "scheduled",
        SessionLog.scheduled_at >= (now - timedelta(hours=2))
    ).order_by(SessionLog.scheduled_at.asc()).all()

    res = []
    for s in sessions:
        other_user_name = "User"
        other_user_id = None
        if mentor_id and s.mentor_id == mentor_id:
            # Current user is the mentor — other party is the student
            student_user = db.query(User).filter(User.id == s.student_id).first()
            other_user_name = student_user.full_name if student_user else "Student"
            other_user_id = student_user.id if student_user else None
        else:
            # Current user is the student — other party is the mentor's user account
            mentor_user = db.query(User).join(Mentor).filter(Mentor.id == s.mentor_id).first()
            other_user_name = mentor_user.full_name if mentor_user else "Mentor"
            other_user_id = mentor_user.id if mentor_user else None

        sch_naive = s.scheduled_at.replace(tzinfo=None)
        is_live = now >= (sch_naive - timedelta(minutes=5))
        seconds_until_start = int((sch_naive - now).total_seconds())

        res.append({
            "session_id": s.id, "scheduled_at": sch_naive,
            "other_party_name": other_user_name,
            "other_user_id": other_user_id,
            "is_live": is_live,
            "seconds_until_start": seconds_until_start
        })
    return res

# ── CHAT & REAL-TIME ──────────────────────────────────────────────────────

@router.websocket("/mentorship/chat/{other_user_id}/")
async def websocket_chat(
    websocket: WebSocket,
    other_user_id: UUID,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    # 1. PRE-ACCEPT AUTHENTICATION
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

    # 2. DETERMINE STUDENT / MENTOR ROLES
    current_mentor = db.query(Mentor).filter(Mentor.user_id == user.id).first()
    other_mentor = db.query(Mentor).filter(Mentor.user_id == other_user_id).first()

    if current_mentor and not other_mentor:
        mentor_profile_id = current_mentor.id
        student_user_id = other_user_id
    elif other_mentor and not current_mentor:
        mentor_profile_id = other_mentor.id
        student_user_id = user.id
    else:
        # Both mentors, or neither — relationship is ambiguous
        await websocket.accept()
        await websocket.send_json({"event": "ERROR", "message": "Could not resolve mentor/student relationship."})
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # 3. AUTHORIZATION — must have an approved or accepted mentorship link
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

    # 4. CANONICAL ROOM KEY (same room regardless of who connects first)
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
# ── REQUEST MANAGEMENT ────────────────────────────────────────────────────

@router.get("/requests/pending/")
def get_pending_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    mentor = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
    if not mentor: raise HTTPException(status_code=403)

    pending = (
        db.query(MentorshipRequest, User.full_name, MentorAvailability)
        .join(User, MentorshipRequest.student_id == User.id)
        .join(MentorAvailability, MentorshipRequest.availability_id == MentorAvailability.id)
        .filter(MentorshipRequest.mentor_id == mentor.id, MentorshipRequest.status == "pending")
        .all()
    )
    return [{"request_id": r[0].id, "student_name": r[1], "time_slot": f"Day {r[2].day_of_week}: {r[2].start_time}"} for r in pending]

@router.post("/requests/create", status_code=201)
def request_mentorship(body: RequestIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    slot = db.query(MentorAvailability).filter(MentorAvailability.id == body.availability_id).first()
    if not slot or slot.is_booked: raise HTTPException(status_code=400, detail="Slot unavailable.")
    
    existing = db.query(MentorshipRequest).filter(MentorshipRequest.availability_id == body.availability_id, MentorshipRequest.status == "pending").first()
    if existing: raise HTTPException(status_code=400, detail="Pending request exists.")

    new_req = MentorshipRequest(student_id=current_user.id, mentor_id=body.mentor_id, availability_id=body.availability_id, message=body.message, status="pending")
    db.add(new_req); db.commit()
    return {"message": "Request sent."}

@router.post("/requests/{request_id}/approve")
async def approve_request(request_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    mentor = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
    req = db.query(MentorshipRequest).filter(MentorshipRequest.id == request_id).first()
    if not req or req.mentor_id != mentor.id:
        raise HTTPException(status_code=404)

    slot = db.query(MentorAvailability).filter(MentorAvailability.id == req.availability_id).first()
    slot.is_booked = True
    req.status = "approved"

    # Create a Dyte video meeting for this session
    dyte_meeting_id = None
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{DYTE_BASE_URL}/meetings",
                json={"title": f"Mentorship Session - {current_user.full_name}"},
                headers=_dyte_headers(),
                timeout=10.0
            )
            resp.raise_for_status()
            dyte_meeting_id = resp.json()["data"]["id"]
    except Exception as e:
        logger.error(f"Dyte meeting creation failed: {e}")
        # Session is still created even if Dyte fails; join-video will surface the error

    session_date = get_next_weekday(datetime.now(IST).date(), slot.day_of_week)
    session = SessionLog(
        student_id=req.student_id,
        mentor_id=req.mentor_id,
        scheduled_at=datetime.combine(session_date, slot.start_time),
        status="scheduled",
        dyte_meeting_id=dyte_meeting_id
    )
    db.add(session)
    db.commit()
    return {"session_id": session.id, "scheduled_at": session.scheduled_at, "dyte_meeting_id": dyte_meeting_id}

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

@router.post("/sessions/{session_id}/join-video")
async def join_video_session(session_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(SessionLog).filter(SessionLog.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    mentor_profile = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
    is_mentor = mentor_profile is not None and session.mentor_id == mentor_profile.id
    is_student = session.student_id == current_user.id

    if not is_mentor and not is_student:
        raise HTTPException(status_code=403, detail="Not authorized for this session.")

    # If no Dyte meeting exists yet (e.g. session pre-dates Dyte integration), create one now
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

@router.get("/availability/{mentor_id}", response_model=List[AvailabilitySlotResponse])
def get_mentor_availability(mentor_id: UUID, db: Session = Depends(get_db)):
    # Must exclude NULL availability_id rows (connection requests) — SQL NOT IN (... NULL ...) = FALSE
    pending = db.query(MentorshipRequest.availability_id).filter(
        MentorshipRequest.status == "pending",
        MentorshipRequest.availability_id.isnot(None)
    ).subquery()
    slots = db.query(MentorAvailability).filter(
        MentorAvailability.mentor_id == mentor_id,
        MentorAvailability.is_booked == False,
        ~MentorAvailability.id.in_(pending)
    ).all()
    return [
        AvailabilitySlotResponse(
            id=s.id,
            mentor_id=s.mentor_id,
            day_of_week=s.day_of_week,
            start_time=str(s.start_time),
            end_time=str(s.end_time),
            is_booked=s.is_booked,
        )
        for s in slots
    ]

# ── CONNECTION REQUESTS (no availability required) ────────────────────────────

@router.post("/connections/request", status_code=201)
def send_connection_request(body: ConnectionRequestIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Student sends a generic 'I want to connect' request to a mentor."""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Student role required.")

    mentor = db.query(Mentor).filter(Mentor.id == body.mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found.")

    # Prevent duplicate pending/accepted connection requests
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
    """Mentor sees all pending connection requests with student profile snapshots."""
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
            # Read-only snapshot — no passwords, no private fields
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
    """Mentor views a student's read-only profile (must have a connection request or accepted link)."""
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
    """Mentor accepts a connection request — enables chat immediately."""
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
    """Mentor rejects a connection request."""
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