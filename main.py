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
from api.v1.onboarding import router as onboarding_router
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Career Counseling AI API",
    description="Multilingual AI-driven career guidance platform",
    version="1.0.0"
)

# CORS configuration for React frontend
# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # The magic wildcard: Allows ANY IP on your LAN
    allow_credentials=False,  # MUST be False when using "*" to keep browsers happy
    allow_methods=["*"],      # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],      # Allows all headers (like our JWT Authorization header)
)

# Register all routes
app.include_router(auth_router)
app.include_router(ingest_router)
app.include_router(aptitude_router)
app.include_router(personality_router)
app.include_router(profile_router)
app.include_router(career_router)
app.include_router(onboarding_router)
@app.get("/")
async def root():
    return {"message": "Career Counseling AI API is running."}