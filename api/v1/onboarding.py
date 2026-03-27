import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
# Assuming your auth dependency is located here based on previous code
from api.deps import get_current_user 
from models.users import User
from models.compass import (
    Profile, AcademicProfile, PsychometricProfile, 
    LifestyleProfile, FinancialProfile, AspirationProfile
)
from schemas.compass import (
    BasicProfileUpdate, AcademicProfileUpdate, PsychometricProfileUpdate,
    LifestyleProfileUpdate, FinancialProfileUpdate, AspirationProfileUpdate
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/onboarding", tags=["Onboarding (AI Compass)"])

def upsert_profile_module(db: Session, model_class, user_id: str, update_data: dict):
    """ Helper function to cleanly Update or Insert a 1-to-1 profile record. """
    record = db.query(model_class).filter(model_class.user_id == user_id).first()
    
    if record:
        # Update existing record
        for key, value in update_data.items():
            setattr(record, key, value)
    else:
        # Create new record
        record = model_class(user_id=user_id, **update_data)
        db.add(record)
        
    db.commit()
    db.refresh(record)
    return record

@router.put("/basic/")
async def update_basic_profile(
    payload: BasicProfileUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """ [Mod 1] Updates demographic and school data. """
    record = upsert_profile_module(db, Profile, current_user.id, payload.model_dump())
    return {"message": "Basic profile saved successfully", "id": str(record.id)}

@router.put("/academic/")
async def update_academic_profile(
    payload: AcademicProfileUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """ [Mod 2] Updates academic performance and learning styles. """
    record = upsert_profile_module(db, AcademicProfile, current_user.id, payload.model_dump())
    return {"message": "Academic profile saved successfully", "id": str(record.id)}

@router.put("/psychometric/")
async def update_psychometric_profile(
    payload: PsychometricProfileUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """ [Mods 5, 6] Updates RIASEC, strengths, and motivations. """
    record = upsert_profile_module(db, PsychometricProfile, current_user.id, payload.model_dump())
    return {"message": "Psychometric profile saved successfully", "id": str(record.id)}

@router.put("/lifestyle/")
async def update_lifestyle_profile(
    payload: LifestyleProfileUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """ [Mod 7] Ingests screen time/stress and Auto-generates Discipline & Focus scores. """
    
    # --- Backend Intelligence: Auto-Scoring Engine ---
    data = payload.model_dump()
    
    # 1. Calculate Focus Score (Starts at 100, drops with screen time and stress)
    focus_penalty = (data['screen_time'] * 5)
    if data['stress_level'].lower() == "high": focus_penalty += 20
    elif data['stress_level'].lower() == "medium": focus_penalty += 10
    data['focus_score'] = max(0.0, 100.0 - focus_penalty)
    
    # 2. Calculate Discipline Score (Based on sleep and screen time limits)
    discipline_score = 100.0
    if data['sleep_quality'].lower() == "poor": discipline_score -= 30
    elif data['sleep_quality'].lower() == "average": discipline_score -= 15
    if data['screen_time'] > 4: discipline_score -= 20
    data['discipline_score'] = max(0.0, discipline_score)

    # 3. Calculate Digital Risk Score
    data['digital_risk_score'] = min(100.0, (data['screen_time'] / 8.0) * 100)
    
    record = upsert_profile_module(db, LifestyleProfile, current_user.id, data)
    
    return {
        "message": "Lifestyle profile analyzed and saved.", 
        "generated_scores": {
            "focus_score": record.focus_score,
            "discipline_score": record.discipline_score,
            "digital_risk_score": record.digital_risk_score
        }
    }

@router.put("/financial/")
async def update_financial_profile(
    payload: FinancialProfileUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """ [Mod 8] Updates feasibility context (Income, Coaching Access). """
    record = upsert_profile_module(db, FinancialProfile, current_user.id, payload.model_dump())
    return {"message": "Financial profile saved successfully", "id": str(record.id)}

@router.put("/aspirations/")
async def update_aspiration_profile(
    payload: AspirationProfileUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """ [Mod 9] Updates dream careers and vision. """
    record = upsert_profile_module(db, AspirationProfile, current_user.id, payload.model_dump())
    return {"message": "Aspiration profile saved successfully", "id": str(record.id)}