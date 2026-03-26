import uuid
import enum
from sqlalchemy import Column, String, Float, Boolean, Enum, ForeignKey, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class UserRole(str, enum.Enum):
    student = "student"
    mentor = "mentor"
    parent = "parent"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False) # Changed from hashed_password to match diagram
    role = Column(Enum(UserRole), default=UserRole.student, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships using strings to prevent circular imports
    profile = relationship("Profile", back_populates="user", uselist=False)
    mentor_profile = relationship("Mentor", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    full_name = Column(String)
    grade_level = Column(String)
    personality_type = Column(String)
    career_alignment_score = Column(Integer)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="profile")

class Mentor(Base):
    __tablename__ = "mentors"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    expertise = Column(String)
    hourly_rate = Column(Float) # Using Float for Decimal to simplify
    platform_cut = Column(Float)
    rating = Column(Float)
    is_verified = Column(Boolean, default=False)

    user = relationship("User", back_populates="mentor_profile")