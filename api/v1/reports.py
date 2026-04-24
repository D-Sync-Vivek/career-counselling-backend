import os
import json
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from core.database import get_db
from models.users import CareerDiscoveryReport # Assuming you placed the model here earlier
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from api.deps import get_current_user
from models.users import User
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/reports", tags=["Report Generation"])
DATABASE_URL = os.getenv("DATABASE_URL")

# ==============================================================================
# 1. PYDANTIC SCHEMAS FOR LANGCHAIN OUTPUT PARSER
# These define the exact JSON structure DeepSeek must return.
# ==============================================================================

class TraitAnalysis(BaseModel):
    name: str = Field(description="e.g., Resilience, Team Work, Spatial Aptitude")
    score: int = Field(description="Score from 1 to 9 calculated from raw test data")
    meaning: str = Field(description="1 sentence defining the trait")
    expert_analysis: str = Field(description="3-4 sentences interpreting the student's score contextually.")
    development_plan: List[str] = Field(description="2-3 actionable bullet points to improve or leverage this trait.")

class DimensionCategory(BaseModel):
    dominant_traits: List[str] = Field(description="Top 2-3 traits in this dimension")
    traits: List[TraitAnalysis] = Field(description="Detailed breakdown of all traits in this dimension")

class FiveDimensionsReport(BaseModel):
    orientation_style: DimensionCategory
    interest: DimensionCategory
    personality: DimensionCategory
    aptitude: DimensionCategory
    emotional_quotient: DimensionCategory

class CareerMatch(BaseModel):
    career_name: str = Field(description="e.g., Computer Application & IT, Defense")
    overall_match_percentage: int = Field(description="Score out of 100")
    dimension_scores: Dict[str, int] = Field(description="Score out of 100 for each of the 5 dimensions. e.g., {'aptitude': 85, 'personality': 60}")
    justification: str = Field(description="2 paragraphs explaining WHY this career fits based on their Profile Data and 5D Psychometric Data.")
    trending_fields: List[str] = Field(description="e.g., UI/UX Designer, Web Developer")

class ComprehensiveReport(BaseModel):
    five_dimensions: FiveDimensionsReport
    career_matches: List[CareerMatch]


# ==============================================================================
# 2. REQUEST MODELS & ROUTES
# ==============================================================================

class GenerateReportRequest(BaseModel):
    user_id: str

@router.post("/generate")
async def generate_comprehensive_report(request: GenerateReportRequest):
    
    # 1. FETCH ALL USER DATA FROM DB
    query = """
    SELECT 
        full_name, academic_data, financial_data, lifestyle_data, aspiration_data,
        apti_data, personality_data, eq_data, orientation_data, career_interest_data
    FROM users 
    WHERE id = %s;
    """
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (request.user_id,))
                user_data = cur.fetchone()

        if not user_data:
            raise HTTPException(status_code=404, detail="User not found.")

        # 2. CREATE PENDING REPORT IN DB
        insert_report_query = """
        INSERT INTO career_discovery_reports (user_id, status) 
        VALUES (%s, 'generating') RETURNING id;
        """
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(insert_report_query, (request.user_id,))
                report_id = cur.fetchone()[0]
            conn.commit()

    except Exception as e:
        logger.error(f"Database error during initialization: {e}")
        raise HTTPException(status_code=500, detail="Database error.")

    # 3. SET UP DEEPSEEK & LANGCHAIN
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="DeepSeek API Key not configured.")

    llm = ChatOpenAI(
        model="deepseek-chat", 
        openai_api_key=api_key, 
        openai_api_base="https://api.deepseek.com",
        temperature=0.3  # Low temperature for analytical consistency
    )
    
    parser = PydanticOutputParser(pydantic_object=ComprehensiveReport)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an elite psychometrician and career counselor (like Mindler). "
                   "Analyze the student's self-reported profile context and their raw psychometric test scores. "
                   "Translate their raw test scores into 1-9 scale scores for the 5 dimensions. "
                   "Provide deep, personalized 'expert_analysis' for each trait. "
                   "Recommend the top 3-5 best-fit careers based on their financial/academic constraints AND psychometric strengths. "
                   "You must strictly follow the output formatting instructions.\n{format_instructions}"),
        ("human", "Student Data: {data}")
    ])

    try:
        # 4. EXECUTE AI CHAIN
        logger.info(f"Generating 30-page AI Report for user {request.user_id}...")
        
        chain = prompt | llm | parser
        
        # This will return a parsed Pydantic object (ComprehensiveReport)
        ai_parsed_report = chain.invoke({
            "data": json.dumps(user_data, default=str), 
            "format_instructions": parser.get_format_instructions()
        })
        
        # Convert the Pydantic object back to a dictionary for DB insertion
        report_dict = ai_parsed_report.model_dump()

        # 5. SAVE COMPLETED REPORT TO DB
        update_report_query = """
        UPDATE career_discovery_reports 
        SET five_dimensions_data = %s, 
            career_matches_data = %s, 
            status = 'completed',
            updated_at = NOW()
        WHERE id = %s;
        """
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(update_report_query, (
                    json.dumps(report_dict.get("five_dimensions", {})),
                    json.dumps(report_dict.get("career_matches", [])),
                    report_id
                ))
            conn.commit()

        return {
            "status": "success",
            "message": "Comprehensive Report generated successfully!",
            "report_id": report_id
        }

    except Exception as e:
        logger.error(f"AI Generation Failed: {e}")
        # Mark report as failed in database
        try:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE career_discovery_reports SET status = 'failed' WHERE id = %s;", (report_id,))
                conn.commit()
        except:
            pass
        raise HTTPException(status_code=500, detail="The AI Career Engine failed to generate the report.")


# ==============================================================================
# 3. GET REPORT ROUTE (For the Frontend to display the charts)
# ==============================================================================
@router.get("/me")
async def get_my_report(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Use SQLAlchemy to securely fetch the latest report for the logged-in user
        report = db.query(CareerDiscoveryReport).filter(
            CareerDiscoveryReport.user_id == current_user.id
        ).order_by(CareerDiscoveryReport.created_at.desc()).first()
        
        if not report:
            raise HTTPException(status_code=404, detail="No report found for this user.")
            
        return {
            "id": str(report.id),
            "status": report.status,
            "five_dimensions_data": report.five_dimensions_data,
            "career_matches_data": report.career_matches_data,
            "created_at": report.created_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching report: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")