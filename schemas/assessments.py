# schemas/assessments.py
from pydantic import BaseModel, Field
from typing import List, Dict

class AnswerInput(BaseModel):
    question_id: int
    score: int = Field(..., ge=1, le=5, description="Score must be between 1 and 5")

class PersonalityTestSubmission(BaseModel):
    answers: List[AnswerInput]

class TraitScores(BaseModel):
    O: int  # Openness
    C: int  # Conscientiousness
    E: int  # Extraversion
    A: int  # Agreeableness
    N: int  # Neuroticism

class PersonalityScoringResult(BaseModel):
    message: str
    dominant_traits: List[str]
    # We return the scores to the frontend so they can show a cool graph
    scores: TraitScores

class AptitudeScoreSubmit(BaseModel):
    total_questions: int
    correct_answers: int
    weaknesses: str = "None identified"  # e.g., "Struggled with Time & Distance"

class AptitudeScoreResponse(BaseModel):
    message: str
    overall_score_percentage: int
    result_id: str