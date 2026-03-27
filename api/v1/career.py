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
from models.users import User

# Ensure we import the newly split models!
from models.compass import (
    Profile, AcademicProfile, PsychometricProfile, 
    LifestyleProfile, FinancialProfile, AspirationProfile
)
from models.assessments import Result
from models.careers import Career, Skill, CareerSkill, StudentInsight

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/ai", tags=["AI Career Engine"])

# --- Pydantic Models for Structured AI Output ---
class SkillOutput(BaseModel):
    name: str = Field(description="Name of the skill, e.g., 'Python Programming'")
    category: str = Field(description="Category strictly from: 'technical', 'soft', 'cognitive'")
    weight: int = Field(description="Importance of this skill for the career from 1 to 10")

class CareerOutput(BaseModel):
    title: str = Field(description="Job title, e.g., 'Cloud Architect'")
    description: str = Field(description="A 2-sentence description of why this fits the student's realities.")
    base_success_probability: float = Field(description="Estimated success probability from 0.0 to 1.0 based on aptitude.")
    feasibility_score: float = Field(description="From 0.0 to 1.0 based on financial constraints and coaching access.")
    passion_skill_gap: float = Field(description="From 0.0 to 1.0 representing how much they need to learn to achieve this.")
    core_skills: List[SkillOutput] = Field(description="Top 5 skills needed for this career.")

class AIRecommendationResponse(BaseModel):
    ai_summary: str = Field(description="An empathetic summary factoring in their stress, lifestyle, and dreams.")
    recommended_careers: List[CareerOutput] = Field(description="Exactly 3 highly tailored career recommendations.")

# --- Endpoints ---

@router.post("/careers/recommend", response_model=AIRecommendationResponse)
async def recommend_careers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ Reads the student's entire 9-module profile and generates reality-based careers using DeepSeek. """
    logger.info(f"Initiating Upgraded AI Career Engine for {current_user.email}")

    # 1. Fetch ALL 9 Modules of Student Data
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    academic = db.query(AcademicProfile).filter(AcademicProfile.user_id == current_user.id).first()
    psycho = db.query(PsychometricProfile).filter(PsychometricProfile.user_id == current_user.id).first()
    lifestyle = db.query(LifestyleProfile).filter(LifestyleProfile.user_id == current_user.id).first()
    finance = db.query(FinancialProfile).filter(FinancialProfile.user_id == current_user.id).first()
    dreams = db.query(AspirationProfile).filter(AspirationProfile.user_id == current_user.id).first()
    
    # Get latest aptitude result
    latest_result = db.query(Result).filter(Result.user_id == current_user.id).order_by(Result.completed_at.desc()).first()

    # Basic Validation
    if not profile or not psycho:
        raise HTTPException(status_code=400, detail="Profile incomplete. Please complete the Basic and Psychometric onboarding modules.")

    # 2. Initialize DeepSeek
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_api_key:
        raise HTTPException(status_code=500, detail="CRITICAL: DEEPSEEK_API_KEY missing.")
    
    llm = ChatOpenAI(
        model="deepseek-chat", 
        api_key=deepseek_api_key, 
        base_url="https://api.deepseek.com", # Adjust base URL if your provider requires it
        temperature=0.3
    )
    
    parser = PydanticOutputParser(pydantic_object=AIRecommendationResponse)

    # 3. Build the Deep-Context Prompt
    system_prompt = """
    You are an elite, highly empathetic Career Counselor AI. Your goal is to analyze a student's complete 
    psycho-demographic profile and recommend 3 highly achievable careers.
    
    STUDENT CONTEXT:
    - Demographics: {grade_level}, {area_type} area
    - Academics: {academic_band}, Strongest: {strong_subj}, Weakest: {weak_subj}
    - Psychometric: {personality}, Strengths: {strength}, Weakness: {weakness}
    - Aptitude Score: {aptitude_score}%
    - Lifestyle realities: {screen_time} hrs screen time, Stress: {stress}, Discipline Score: {discipline}/100
    - Financial Realities: {income}, Affordability: {affordability}, Coaching Access: {coaching}
    - Dreams: {dream_career}, Vision: {vision}
    
    CONSTRAINTS:
    - If financial constraints are high and coaching is low, recommend achievable pathways (high feasibility score).
    - If stress is high and discipline is low, avoid extremely high-pressure, 80-hour workweek careers.
    - Base 'passion_skill_gap' on how far their current academics/aptitude are from the dream.
    
    {format_instructions}
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Analyze my deep context profile and give me reality-based recommendations.")
    ])

    # 4. Execute the AI Chain safely handling None values
    logger.info("Sending massive context payload to DeepSeek...")
    chain = prompt | llm | parser
    
    try:
        ai_result: AIRecommendationResponse = chain.invoke({
            "grade_level": profile.current_class if profile else "Unknown",
            "area_type": profile.area_type if profile else "Unknown",
            "academic_band": academic.overall_percentage_band if academic else "Unknown",
            "strong_subj": academic.strongest_subject if academic else "Unknown",
            "weak_subj": academic.weakest_subject if academic else "Unknown",
            "personality": psycho.personality_type if psycho else "Unknown",
            "strength": psycho.biggest_strength if psycho else "Unknown",
            "weakness": psycho.biggest_weakness if psycho else "Unknown",
            "aptitude_score": latest_result.overall_score if latest_result else "No test taken",
            "screen_time": lifestyle.screen_time if lifestyle else "Unknown",
            "stress": lifestyle.stress_level if lifestyle else "Unknown",
            "discipline": lifestyle.discipline_score if lifestyle else "Unknown",
            "income": finance.income_band if finance else "Unknown",
            "affordability": finance.affordability_level if finance else "Unknown",
            "coaching": str(finance.coaching_access) if finance else "Unknown",
            "dream_career": dreams.dream_career if dreams else "Unknown",
            "vision": dreams.ten_year_vision if dreams else "Unknown",
            "format_instructions": parser.get_format_instructions()
        })
    except Exception as e:
        logger.error(f"DeepSeek generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="AI generation failed. Check logs.")

    # 5. Dynamic Database Cataloging (The Enterprise Upsert)
    top_career_output = ai_result.recommended_careers[0]
    
    # 5a. Save the Top Career
    db_career = db.query(Career).filter(Career.title == top_career_output.title).first()
    if not db_career:
        db_career = Career(
            title=top_career_output.title,
            description=top_career_output.description,
            base_success_probability=top_career_output.base_success_probability
        )
        db.add(db_career)
        db.flush() 
        
    # 5b. Save Skills and link them via CareerSkill
    for skill_out in top_career_output.core_skills:
        db_skill = db.query(Skill).filter(Skill.name == skill_out.name).first()
        if not db_skill:
            # Enforce constraints just in case LLM hallucinates categories
            safe_category = skill_out.category.lower()
            if safe_category not in ['technical', 'soft', 'cognitive']:
                safe_category = 'technical'
                
            db_skill = Skill(name=skill_out.name, category=safe_category)
            db.add(db_skill)
            db.flush()
            
        # Merge link to prevent Unique Constraint errors
        career_link = CareerSkill(career_id=db_career.id, skill_id=db_skill.id, weight=skill_out.weight)
        db.merge(career_link)

    # 6. Save/Update the AI Insight to the Student's profile (1-to-1 enforcement)
    existing_insight = db.query(StudentInsight).filter(StudentInsight.student_id == current_user.id).first()
    
    if existing_insight:
        existing_insight.ai_summary = ai_result.ai_summary
        existing_insight.recommended_career_id = db_career.id
        existing_insight.success_probability = top_career_output.base_success_probability
        existing_insight.feasibility_score = top_career_output.feasibility_score
        existing_insight.passion_skill_gap = top_career_output.passion_skill_gap
    else:
        insight = StudentInsight(
            student_id=current_user.id,
            ai_summary=ai_result.ai_summary,
            recommended_career_id=db_career.id,
            success_probability=top_career_output.base_success_probability,
            feasibility_score=top_career_output.feasibility_score,
            passion_skill_gap=top_career_output.passion_skill_gap
        )
        db.add(insight)
        
    db.commit()

    logger.info(f"Deep Context Career recommendation completed for {current_user.email}")
    return ai_result