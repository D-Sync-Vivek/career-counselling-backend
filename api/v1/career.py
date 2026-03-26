import os
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

# LangChain Imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# Core & DB Imports
from core.database import get_db
from api.deps import get_current_user
from models.users import User, Profile
from models.assessments import Result
from models.careers import Career, Skill, CareerSkill, StudentInsight

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/ai", tags=["AI Career Engine"])

# --- Pydantic Models for Structured AI Output ---
class SkillOutput(BaseModel):
    name: str = Field(description="Name of the skill, e.g., 'Python Programming'")
    category: str = Field(description="Category, e.g., 'Technical', 'Soft Skill', 'Analytical'")
    weight: int = Field(description="Importance of this skill for the career from 1 to 10")

class CareerOutput(BaseModel):
    title: str = Field(description="Job title, e.g., 'Data Scientist'")
    description: str = Field(description="A 2-sentence description of why this fits the student.")
    base_success_probability: float = Field(description="Estimated success probability from 0.0 to 1.0 based on their scores.")
    core_skills: List[SkillOutput] = Field(description="Top 5 skills needed for this career.")

class AIRecommendationResponse(BaseModel):
    ai_summary: str = Field(description="An empathetic, encouraging summary of the student's overall profile.")
    recommended_careers: List[CareerOutput] = Field(description="Exactly 3 career recommendations.")

# --- Endpoints ---

@router.post("/careers/recommend", response_model=AIRecommendationResponse)
async def recommend_careers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ Reads the student's DB profile/scores and generates tailored careers using DeepSeek. """
    
    logger.info(f"Initiating AI Career Engine for {current_user.email}")

    # 1. Fetch Student Data
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile or not profile.personality_type:
        raise HTTPException(status_code=400, detail="Profile incomplete. Please take the Personality Test first.")

    latest_result = db.query(Result).filter(Result.user_id == current_user.id).order_by(Result.completed_at.desc()).first()
    if not latest_result:
        raise HTTPException(status_code=400, detail="No aptitude scores found. Please take the Aptitude Test first.")

    # 2. Initialize DeepSeek
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_api_key:
        raise HTTPException(status_code=500, detail="CRITICAL: DEEPSEEK_API_KEY is missing in .env file.")
    
    llm = ChatOpenAI(
        model="deepseek-chat", 
        api_key=deepseek_api_key, 
        base_url="https://api.deepseek.com",
        temperature=0.4 # Slight creativity for career brainstorming
    )
    
    parser = PydanticOutputParser(pydantic_object=AIRecommendationResponse)

    # 3. Build the Context-Aware Prompt
    system_prompt = """
    You are an elite Career Counselor AI. Your goal is to analyze a student's profile and recommend 3 highly suitable careers.
    
    STUDENT PROFILE:
    - Grade Level: {grade_level}
    - Dominant Personality Trait: {personality}
    - Aptitude Score: {aptitude_score}%
    - Identified Weaknesses: {weaknesses}
    
    CONSTRAINTS:
    - Base the 'success probability' realistically on their aptitude score and how well their personality aligns with the career.
    - Be highly specific with the required skills.
    
    {format_instructions}
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Analyze my profile and recommend my top 3 careers with required skills.")
    ])

    # 4. Execute the AI Chain
    logger.info("Sending student data to DeepSeek...")
    chain = prompt | llm | parser
    
    try:
        ai_result: AIRecommendationResponse = chain.invoke({
            "grade_level": profile.grade_level or "Unknown",
            "personality": profile.personality_type,
            "aptitude_score": latest_result.overall_score,
            "weaknesses": latest_result.weakness_mapping,
            "format_instructions": parser.get_format_instructions()
        })
    except Exception as e:
        logger.error(f"DeepSeek generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="AI generation failed.")

    # 5. Dynamic Database Cataloging (The Enterprise Flex)
    top_career = ai_result.recommended_careers[0]
    
    # 5a. Check if the top career exists in our DB; if not, create it!
    db_career = db.query(Career).filter(Career.title == top_career.title).first()
    if not db_career:
        db_career = Career(
            title=top_career.title,
            description=top_career.description,
            base_success_probability=top_career.base_success_probability
        )
        db.add(db_career)
        db.flush() # Flushes to get the UUID without committing the whole transaction yet
        
        # 5b. Catalog the skills and link them
        for skill in top_career.core_skills:
            db_skill = db.query(Skill).filter(Skill.name == skill.name).first()
            if not db_skill:
                db_skill = Skill(name=skill.name, category=skill.category)
                db.add(db_skill)
                db.flush()
                
            # Link skill to career
            career_link = CareerSkill(career_id=db_career.id, skill_id=db_skill.id, weight=skill.weight)
            db.merge(career_link) # Merge prevents duplicates if the link already exists

    # 6. Save the AI Insight to the Student's profile
    insight = StudentInsight(
        student_id=current_user.id,
        ai_summary=ai_result.ai_summary,
        recommended_career_id=db_career.id,
        success_probability=top_career.base_success_probability
    )
    db.add(insight)
    db.commit()

    logger.info(f"Career recommendation successfully generated and saved for {current_user.email}")
    return ai_result