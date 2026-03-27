import uuid
from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    full_name = Column(String, nullable=False)
    dob = Column(DateTime) # Using DateTime for Date for simplicity
    gender = Column(String)
    current_class = Column(String)
    school_type = Column(String)
    state = Column(String)
    area_type = Column(String)
    medium_of_learning = Column(String)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="profile")

class AcademicProfile(Base):
    __tablename__ = "academic_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    overall_percentage_band = Column(String)
    strongest_subject = Column(String)
    weakest_subject = Column(String)
    favorite_subject = Column(String)
    learning_style = Column(String)
    study_hours_home = Column(Integer)
    homework_completion = Column(String)
    achievements = Column(Text)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PsychometricProfile(Base):
    __tablename__ = "psychometric_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    personality_type = Column(String)
    riasec_code = Column(String)
    work_environment = Column(String)
    work_style = Column(String)
    biggest_strength = Column(String)
    biggest_weakness = Column(String)
    motivation_driver = Column(String)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class LifestyleProfile(Base):
    __tablename__ = "lifestyle_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    screen_time = Column(Integer)
    sleep_quality = Column(String)
    stress_level = Column(String)
    focus_score = Column(Float)
    discipline_score = Column(Float)
    digital_risk_score = Column(Float)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class FinancialProfile(Base):
    __tablename__ = "financial_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    family_structure = Column(String)
    income_band = Column(String)
    father_education = Column(String)
    mother_education = Column(String)
    affordability_level = Column(String)
    coaching_access = Column(Boolean)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AspirationProfile(Base):
    __tablename__ = "aspiration_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    dream_career = Column(String)
    life_direction = Column(Text)
    ten_year_vision = Column(Text)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())