import os
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

# LangChain Imports
from langchain_community.vectorstores import PGVector
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# Core & DB Imports
from core.vector_db import get_vector_store
from core.database import get_db
from api.deps import get_current_user
from models.users import User
from models.assessments import Test, Result
from schemas.assessments import AptitudeScoreSubmit, AptitudeScoreResponse

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Updated Prefix to match our API Documentation
router = APIRouter(prefix="/api/v1/assessments/aptitude", tags=["Aptitude Assessments"])

# --- Pydantic Models for Structured AI Output ---
class AptitudeMCQ(BaseModel):
    question: str = Field(description="The mathematical or logical aptitude question")
    options: List[str] = Field(description="Exactly 4 distinct options for the MCQ")
    correct_answer: str = Field(description="The exact text of the correct option")
    explanation: str = Field(description="A step-by-step mathematical breakdown of how to solve the problem")

class AptitudeQuizOutput(BaseModel):
    quiz_summary: str = Field(description="A 1-2 sentence overview of the concepts covered in this quiz")
    questions: List[AptitudeMCQ] = Field(description="A list of multiple choice questions")

# --- Endpoints ---

@router.post("/generate", response_model=AptitudeQuizOutput)
async def generate_aptitude_quiz(
    category: str, 
    topic: str, 
    target_grade: str, 
    difficulty: str,   
    num_questions: int = 5,
    vs: PGVector = Depends(get_vector_store),
    current_user: User = Depends(get_current_user) # <-- ADDED: Secures the endpoint!
):
    """ Retrieves context from Postgres and generates a structured, grade-appropriate aptitude quiz. """
    logger.info(f"User {current_user.email} generating {num_questions} {difficulty} questions on {topic}")

    # 1. Vector Search (RAG) - Strict Filtering
    try:
        # Note: If your ingested PDF chunks don't have 'target_grade' and 'difficulty' in their metadata, 
        # this filter might return empty. If it crashes, remove the filter and let the LLM handle difficulty.
        retriever = vs.as_retriever(
            search_kwargs={
                "k": 15, 
                "filter": {
                    "category": category,
                    "topic": topic,
                    "target_grade": target_grade, 
                    "difficulty": difficulty      
                }
            }
        )

        docs = retriever.invoke(f"Extract {difficulty} aptitude problems for grade {target_grade} regarding {topic}")
        context_text = "\n\n".join([doc.page_content for doc in docs])

        if not context_text:
            logger.warning("No context found in PostgreSQL for the given filters.")
            raise HTTPException(status_code=404, detail="No ingested data found matching this specific criteria.")
        
    except Exception as e:
        logger.error(f"Database retrieval failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database retrieval failed.")

    # 2. Initialize DeepSeek API
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_api_key:
        raise HTTPException(status_code=500, detail="CRITICAL: DEEPSEEK_API_KEY is missing in .env file.")
    
    llm = ChatOpenAI(
        model="deepseek-chat", 
        api_key=deepseek_api_key, 
        base_url="https://api.deepseek.com",
        temperature=0.3 
    )

    # 3. Setup the Pydantic Output Parser
    parser = PydanticOutputParser(pydantic_object=AptitudeQuizOutput)

    # 4. Create the Prompt
    system_prompt = """
    You are an expert educational assessor. 
    Your task is to generate a structured Aptitude Quiz based strictly on the provided context.
    
    CRITICAL CONSTRAINTS:
    - Target Audience: Grade {target_grade} student. The language and mathematical complexity MUST be appropriate for this age group.
    - Difficulty Level: {difficulty}. Ensure the problems match this specific difficulty level.
    - Generate EXACTLY {num_questions} Multiple Choice Questions (MCQs).
    - Provide a clear, step-by-step mathematical explanation for the correct answer tailored to a Grade {target_grade} reading level.
    - Do not hallucinate formulas; use the logic presented in the context.
    
    {format_instructions}
    
    Context from Vector Database:
    {context}
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Generate a {difficulty} aptitude quiz for Grade {target_grade} on Category: {category}, Topic: {topic}.")
    ])

    # 5. Execute the Chain
    logger.info("Sending prompt and context to DeepSeek API...")
    chain = prompt | llm | parser
    
    try:
        result = chain.invoke({
            "context": context_text,
            "category": category,
            "topic": topic,
            "target_grade": target_grade,
            "difficulty": difficulty,
            "num_questions": num_questions,
            "format_instructions": parser.get_format_instructions()
        })
        return result
    except Exception as e:
        logger.error(f"LLM Generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="LLM Generation failed.")
    
@router.post("/score", response_model=AptitudeScoreResponse)
async def save_aptitude_score(
    submission: AptitudeScoreSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ Grades the RAG aptitude test and saves the score to the database. """
    
    if submission.total_questions == 0:
        raise HTTPException(status_code=400, detail="Total questions cannot be zero.")
        
    percentage_score = int((submission.correct_answers / submission.total_questions) * 100)

    # Ensure the Test exists in the master Tests table
    test_record = db.query(Test).filter(Test.title == "General Aptitude RAG Test").first()
    if not test_record:
        test_record = Test(
            title="General Aptitude RAG Test",
            type="aptitude",
            total_questions=10
        )
        db.add(test_record)
        db.commit()
        db.refresh(test_record)

    # Save the student's result
    new_result = Result(
        user_id=current_user.id,
        test_id=test_record.id,
        overall_score=percentage_score,
        weakness_mapping=submission.weaknesses
    )
    
    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    return AptitudeScoreResponse(
        message="Aptitude score securely saved to database.",
        overall_score_percentage=percentage_score,
        result_id=str(new_result.id)
    )