import logging
from sqlalchemy import text
from core.database import engine, Base

# IMPORT EVERY MODEL SO SQLALCHEMY SEES THEM
from models.users import User
from models.compass import Profile, AcademicProfile, PsychometricProfile, LifestyleProfile, FinancialProfile, AspirationProfile
from models.assessments import Test, Result
from models.careers import Career, Skill, CareerSkill, UserSkill, StudentInsight
from models.roadmaps import Roadmap, RoadmapMilestone
from models.mentorship import Mentor, MentorAvailability, SessionLog, ChatMessage, MentorFeedback, ParentFeedback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_db():
    logger.info("Connecting to PostgreSQL...")
    
    with engine.begin() as conn:
        logger.warning("Dropping all existing relational tables (CASCADE)...")
        # We drop the new tables as well in case we run this script again later
        conn.execute(text("""
            DROP TABLE IF EXISTS users, profiles, academic_profiles, psychometric_profiles, 
            lifestyle_profiles, financial_profiles, aspiration_profiles, mentors, 
            mentor_availability, tests, results, careers, skills, career_skills, 
            user_skills, student_insights, roadmaps, roadmap_milestones, sessions, 
            chat_messages, mentor_feedback, parent_feedback, 
            langchain_pg_embedding, langchain_pg_collection CASCADE;
        """))
    
    logger.info("Creating comprehensive DB schema from updated ER Diagram...")
    Base.metadata.create_all(bind=engine)
    
    logger.info("✅ Full Production Database with AI Career Compass Schema created successfully!")

if __name__ == "__main__":
    reset_db()