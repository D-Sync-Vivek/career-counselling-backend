import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import Routers
from api.v1.auth import router as auth_router
from api.v1.submit import router as submit_router
from api.v1.ques import router as ques_router
from api.v1.aptitude import router as aptitude_router
from api.v1.profile import router as profile_router
from api.v1.career import router as career_router
from api.v1.roadmap import router as roadmap_router
from router.personality import router as personality_router
from api.v1.mentor import router as mentor_router
from api.v1.parent import router as parent_router
from api.v1.chat import router as chat_router, purge_old_messages_loop
# --- NEW IMPORTS FOR DATABASE CREATION ---
from core.database import engine, Base
from models.users import User  # Importing this ensures SQLAlchemy knows the table exists before creating
from models.roadmap import Roadmap, RoadmapPhase, RoadmapTask
from models.mentor import Mentor, MentorAvailability, MentorshipRequest, SessionLog, ChatMessage, MentorFeedback, ParentFeedback, ParentStudentLink
from models.profile import Profile, AcademicProfile, PsychometricProfile, LifestyleProfile, FinancialProfile, AspirationProfile
from models.career import Career, Skill, CareerSkill, UserSkill, StudentInsight
from models.assessment import Test, Result
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- ADD THIS LINE TO CREATE TABLES ---
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")
    
    # Start the 24h message cleanup background task on server boot
    task = asyncio.create_task(purge_old_messages_loop())
    logger.info("Chat cleanup task started.")
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="Career Counseling AI API",
    description="Multilingual AI-driven career guidance platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration for React frontend
origins = [
    "http://187.127.139.208:5173",  # Your VPS Frontend
    "http://localhost:5173"         # Keep this if you still code locally
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # Use the specific origins list
    allow_credentials=True,  # Now this is safe and legal
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
app.include_router(auth_router)
app.include_router(roadmap_router)
app.include_router(ques_router)
app.include_router(submit_router)
app.include_router(aptitude_router)
app.include_router(profile_router)
app.include_router(career_router)
app.include_router(personality_router)
app.include_router(mentor_router)
app.include_router(parent_router)
app.include_router(chat_router)

@app.get("/")
async def root():
    return {"message": "Career Counseling AI API is running."}