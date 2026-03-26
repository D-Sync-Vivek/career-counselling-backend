# api/v1/personality.py
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from api.deps import get_current_user
from models.users import User, Profile
from schemas.assessments import PersonalityTestSubmission, PersonalityScoringResult, TraitScores

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/assessments/personality", tags=["Assessments"])

# --- Hardcoded DB for Phase 1 (We will move this to Postgres later) ---
BIG_FIVE_QUESTIONS = [
    {"id": 1, "trait": "O", "text": "I have a rich vocabulary.", "reverse": False},
    {"id": 2, "trait": "O", "text": "I have difficulty understanding abstract ideas.", "reverse": True},
    {"id": 3, "trait": "C", "text": "I am always prepared.", "reverse": False},
    {"id": 4, "trait": "C", "text": "I leave my belongings around.", "reverse": True},
]

@router.get("/questions")
async def get_personality_questions(current_user: User = Depends(get_current_user)):
    """ Fetches questions for the frontend. Secured by JWT. """
    safe_questions = [{"id": q["id"], "text": q["text"]} for q in BIG_FIVE_QUESTIONS]
    return {"total_questions": len(safe_questions), "questions": safe_questions}

@router.post("/score", response_model=PersonalityScoringResult)
async def score_personality_test(
    submission: PersonalityTestSubmission, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Bouncer checks token
):
    """ Grades the test and saves the dominant trait to the user's Profile. """
    
    # 1. Math Calculation (From Phase 2)
    raw_scores = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
    question_map = {q["id"]: q for q in BIG_FIVE_QUESTIONS}
    
    for ans in submission.answers:
        if ans.question_id not in question_map:
            raise HTTPException(status_code=400, detail=f"Invalid question ID: {ans.question_id}")
            
        q_data = question_map[ans.question_id]
        trait = q_data["trait"]
        is_reverse = q_data["reverse"]
        
        final_score = (6 - ans.score) if is_reverse else ans.score
        raw_scores[trait] += final_score

    # Find dominant trait
    sorted_traits = sorted(raw_scores.items(), key=lambda item: item[1], reverse=True)
    top_trait_code = sorted_traits[0][0]
    top_2_traits = [sorted_traits[0][0], sorted_traits[1][0]]

    # Map the code to a readable string for the database
    trait_map = {"O": "Openness", "C": "Conscientiousness", "E": "Extraversion", "A": "Agreeableness", "N": "Neuroticism"}
    dominant_personality = trait_map.get(top_trait_code, "Unknown")

    # 2. Database Update (The New Enterprise Logic)
    logger.info(f"Saving personality '{dominant_personality}' to Profile for User: {current_user.email}")
    
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found. Contact support.")
        
    profile.personality_type = dominant_personality
    db.commit()

    return PersonalityScoringResult(
        message="Test scored and permanently saved to profile.",
        dominant_traits=top_2_traits,
        scores=TraitScores(**raw_scores)
    )