import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
from models.users import User
from models.compass import Profile
# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/profile", tags=["Profile Builder"])

# --- Pydantic Models for Input ---
class BasicInfo(BaseModel):
    grade: str = Field(..., description="e.g., '9-10', '11-12'")
    interests: List[str] = Field(..., description="e.g., ['robotics', 'space', 'writing']")

class AptitudeScores(BaseModel):
    quantitative: int = Field(..., description="Percentage score 0-100")
    logical: int = Field(..., description="Percentage score 0-100")
    verbal: int = Field(..., description="Percentage score 0-100")

class PersonalityScores(BaseModel):
    dominant_traits: List[str] = Field(..., description="Top 2 traits, e.g., ['O', 'E']")
    raw_scores: Dict[str, int] = Field(..., description="Full OCEAN scores map")

class ProfileBuildRequest(BaseModel):
    basic_info: BasicInfo
    aptitude: AptitudeScores
    personality: PersonalityScores

# --- Pydantic Model for Output ---
class StudentProfileOutput(BaseModel):
    status: str
    profile_json: dict

# --- Endpoints ---
@router.post("/build", response_model=StudentProfileOutput)
async def build_student_profile(request: ProfileBuildRequest):
    """
    Aggregates all independent assessment scores into a single, LLM-optimized JSON payload.
    """
    logger.info(f"Building unified profile for Grade {request.basic_info.grade} student.")

    try:
        # Translate the raw Big Five codes into readable text for the AI context later
        # We do this deterministically here so the LLM doesn't have to "guess" what 'O' means.
        trait_map = {
            "O": "Openness", 
            "C": "Conscientiousness", 
            "E": "Extraversion", 
            "A": "Agreeableness", 
            "N": "Neuroticism"
        }
        
        readable_traits = [trait_map.get(t, t) for t in request.personality.dominant_traits]

        # Construct the perfectly formatted JSON payload
        unified_payload = {
            "student_demographics": {
                "grade_level": request.basic_info.grade,
                "stated_interests": request.basic_info.interests
            },
            "academic_aptitude": {
                "quantitative_score": f"{request.aptitude.quantitative}%",
                "logical_score": f"{request.aptitude.logical}%",
                "verbal_score": f"{request.aptitude.verbal}%"
            },
            "psychometric_profile": {
                "dominant_traits": readable_traits,
                "raw_ocean_scores": request.personality.raw_scores
            }
        }

        logger.info("Successfully generated unified JSON profile.")

        return StudentProfileOutput(
            status="success",
            profile_json=unified_payload
        )
        
    except Exception as e:
        logger.error(f"Failed to build profile: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to build student profile.")