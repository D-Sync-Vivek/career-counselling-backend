import logging
from sqlalchemy import text
from core.database import engine, Base

# You MUST import every single model file here so SQLAlchemy knows they exist
from models.users import User, Profile, Mentor
from models.assessments import Test, Result
from models.careers import Career, Skill, CareerSkill, StudentInsight
from models.mentorship import SessionLog, ChatMessage, MentorFeedback, ParentFeedback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_db():
    logger.info("Connecting to Neon PostgreSQL...")
    
    with engine.begin() as conn:
        # Drop all standard tables to prevent UUID vs Integer conflicts
        logger.warning("Dropping all existing relational tables (CASCADE)...")
        conn.execute(text("""
            DROP TABLE IF EXISTS users, profiles, mentors, tests, results, 
            careers, skills, career_skills, student_insights, 
            sessions, chat_messages, mentor_feedback, parent_feedback CASCADE;
        """))
    
    logger.info("Creating comprehensive DB schema from ER Diagram...")
    Base.metadata.create_all(bind=engine)
    
    logger.info("✅ Full Production Database created successfully!")

if __name__ == "__main__":
    reset_db()