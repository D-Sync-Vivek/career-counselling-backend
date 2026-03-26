import logging
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

# --- Setup Logging (Matching Existing Style) ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/personality", tags=["Personality Engine"])

# --- Database Schema Design (Conceptual) ---
# In PostgreSQL, your table would look like this:
# CREATE TABLE personality_questions (
#     id SERIAL PRIMARY KEY,
#     trait VARCHAR(10) NOT NULL, -- 'O', 'C', 'E', 'A', 'N'
#     question_text TEXT NOT NULL,
#     is_reverse_scored BOOLEAN DEFAULT FALSE
# );

# For high-performance read-heavy operations where questions rarely change, 
# a static dictionary loaded into memory is an architecturally sound starting point.
BIG_FIVE_QUESTIONS = [
    {"id": 1, "trait": "O", "text": "I have a rich vocabulary and enjoy abstract ideas.", "reverse": False},
    {"id": 2, "trait": "O", "text": "I have difficulty understanding abstract ideas.", "reverse": True},
    {"id": 3, "trait": "C", "text": "I am always prepared and pay attention to details.", "reverse": False},
    {"id": 4, "trait": "C", "text": "I often leave my belongings around and make a mess.", "reverse": True},
    {"id": 5, "trait": "E", "text": "I am the life of the party and feel comfortable around people.", "reverse": False},
    {"id": 6, "trait": "E", "text": "I don't talk a lot and prefer to stay in the background.", "reverse": True},
    {"id": 7, "trait": "A", "text": "I sympathize with others' feelings and take time out for them.", "reverse": False},
    {"id": 8, "trait": "A", "text": "I am not really interested in others and their problems.", "reverse": True},
    {"id": 9, "trait": "N", "text": "I get stressed out easily and worry about things.", "reverse": False},
    {"id": 10, "trait": "N", "text": "I am relaxed most of the time and seldom feel blue.", "reverse": True},
]

# --- Pydantic Models ---
class QuestionOut(BaseModel):
    id: int
    text: str
    # Notice we intentionally exclude 'trait' and 'reverse' from the output model.
    # The frontend should not know the internal scoring logic.

class QuestionListResponse(BaseModel):
    total_questions: int
    questions: List[QuestionOut]

# --- Endpoints ---
@router.get("/questions", response_model=QuestionListResponse)
async def get_personality_questions():
    """ 
    Fetches the Big Five personality questions. 
    Strips internal scoring metadata before sending to the client.
    """
    logger.info("Fetching Big Five personality questions for client.")
    
    # Map the internal data to the safe output schema
    safe_questions = [
        QuestionOut(id=q["id"], text=q["text"]) 
        for q in BIG_FIVE_QUESTIONS
    ]
    
    return QuestionListResponse(
        total_questions=len(safe_questions),
        questions=safe_questions
    )

class AnswerInput(BaseModel):
    question_id: int
    score: int  # Must be between 1 and 5

class TestSubmission(BaseModel):
    answers: List[AnswerInput]

class TraitScores(BaseModel):
    O: int  # Openness
    C: int  # Conscientiousness
    E: int  # Extraversion
    A: int  # Agreeableness
    N: int  # Neuroticism

class ScoringResult(BaseModel):
    message: str
    scores: TraitScores
    dominant_traits: List[str]

# --- Phase 2 Endpoints ---
@router.post("/score", response_model=ScoringResult)
async def score_personality_test(submission: TestSubmission):
    """
    Receives the 1-5 answers from the frontend, applies reverse scoring, 
    and calculates the final Big Five personality profile deterministically.
    """
    logger.info(f"Grading personality test with {len(submission.answers)} answers.")
    
    # 1. Initialize empty score buckets
    raw_scores = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
    
    # 2. Create a quick lookup map from our hidden database
    question_map = {q["id"]: q for q in BIG_FIVE_QUESTIONS}
    
    # 3. Process each answer
    for ans in submission.answers:
        if ans.question_id not in question_map:
            raise HTTPException(status_code=400, detail=f"Invalid question ID: {ans.question_id}")
            
        if ans.score < 1 or ans.score > 5:
            raise HTTPException(status_code=400, detail="Score must be between 1 and 5.")
            
        # Retrieve the hidden grading rules
        q_data = question_map[ans.question_id]
        trait = q_data["trait"]
        is_reverse = q_data["reverse"]
        
        # Apply Reverse Scoring Logic:
        # If reverse is True, a 5 becomes a 1, a 4 becomes a 2, etc. (Formula: 6 - score)
        final_score = (6 - ans.score) if is_reverse else ans.score
        
        raw_scores[trait] += final_score

    # 4. Find the top 2 dominant traits for the career recommendation later
    # Sorts traits by their score in descending order
    sorted_traits = sorted(raw_scores.items(), key=lambda item: item[1], reverse=True)
    top_2_traits = [sorted_traits[0][0], sorted_traits[1][0]]

    logger.info(f"Scoring complete. Dominant traits: {top_2_traits}")

    return ScoringResult(
        message="Personality test scored successfully.",
        scores=TraitScores(**raw_scores),
        dominant_traits=top_2_traits
    )