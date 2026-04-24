import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# 👉 FIXED 1: Added 'func' to the SQLAlchemy imports!
from sqlalchemy import select, func 

from models.careers import Career, StudentInsight
from schemas.ai import CareerSelectRequest, CareerSelectResponse, SelectedCareerResponse
from core.database import get_db
from api.deps import get_current_user
from models.users import User
from models.roadmaps import Roadmap

router = APIRouter(prefix="/api/v1/ai", tags=["DeepSeek Career Engine"])

class CareerOption(BaseModel):
    title: str = Field(description="Career title")
    rationale: str = Field(description="Why this fits")

class AIRecommendationResponse(BaseModel):
    brutal_truth_summary: str = Field(description="Honest assessment of the student's trajectory")
    top_5_careers: List[CareerOption] = Field(description="5 tailored career paths")

@router.post("/recommend", response_model=AIRecommendationResponse)
async def generate_career_roadmap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    u = current_user
    
    data = {
        "academic": u.academic_data,
        "lifestyle": u.lifestyle_data,
        "aspiration": u.aspiration_data,
        "personality": u.personality_data,
        "aptitude": u.apti_data,
        "financial": u.financial_data
    }

    if not u.academic_data or not u.lifestyle_data:
        raise HTTPException(
            status_code=400, 
            detail="Assessment data incomplete. Please fill out Academic and Lifestyle modules."
        )

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="DeepSeek API Key not configured in environment.")

    llm = ChatOpenAI(
        model="deepseek-chat", 
        openai_api_key=api_key, 
        openai_api_base="https://api.deepseek.com",
        temperature=0.4
    )
    
    parser = PydanticOutputParser(pydantic_object=AIRecommendationResponse)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Career Counselor. Analyze the student's data and provide a realistic career roadmap. {format_instructions}"),
        ("human", "Analyze this student data: {data}")
    ])

    try:
        chain = prompt | llm | parser
        response = chain.invoke({
            "data": str(data), 
            "format_instructions": parser.get_format_instructions()
        })
        return response
        
    except Exception as e:
        print(f"AI Engine Error: {str(e)}")
        raise HTTPException(status_code=500, detail="The AI Career Engine failed to generate a response.")
    
@router.post("/select-career", response_model=CareerSelectResponse)
async def select_career(
    payload: CareerSelectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    career = db.query(Career).filter(Career.title == payload.career_title).first()
    
    if not career:
        career = Career(
            title=payload.career_title,
            description=f"AI recommended path for {payload.career_title}",
            base_success_probability=0.7 
        )
        db.add(career)
        db.flush() 

    insight = db.query(StudentInsight).filter(StudentInsight.student_id == current_user.id).first()
    
    if insight:
        insight.recommended_career_id = career.id
        insight.generated_at = func.now()
    else:
        insight = StudentInsight(
            student_id=current_user.id,
            recommended_career_id=career.id
        )
        db.add(insight)

    # 👉 FIXED 2: Added the roadmap deactivation logic back in!
    db.query(Roadmap).filter(Roadmap.student_id == current_user.id).update({"is_active": False})

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to persist selection.")

    return {"success": True, "career": career.title}


# 👉 FIXED 3: Restored the missing GET endpoint to fix the 404 Error!
@router.get("/selected-career", response_model=SelectedCareerResponse)
async def get_selected_career(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    insight = db.query(StudentInsight).filter(StudentInsight.student_id == current_user.id).first()
    
    if not insight or not insight.recommended_career_id:
        return {"career_title": None, "career_id": None}
    
    career = db.query(Career).filter(Career.id == insight.recommended_career_id).first()
    
    return {
        "career_title": career.title if career else None,
        "career_id": career.id if career else None
    }