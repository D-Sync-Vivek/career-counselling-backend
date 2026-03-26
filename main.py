import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import Routers
from api.v1.auth import router as auth_router
from api.v1.ingest import router as ingest_router
from api.v1.aptitude import router as aptitude_router
from api.v1.personality import router as personality_router
from api.v1.profile import router as profile_router
from api.v1.career import router as career_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Career Counseling AI API",
    description="Multilingual AI-driven career guidance platform",
    version="1.0.0"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
app.include_router(auth_router)
app.include_router(ingest_router)
app.include_router(aptitude_router)
app.include_router(personality_router)
app.include_router(profile_router)
app.include_router(career_router)

@app.get("/")
async def root():
    return {"message": "Career Counseling AI API is running."}