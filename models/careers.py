import uuid
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class Career(Base):
    __tablename__ = "careers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    base_success_probability = Column(Float)

class Skill(Base):
    __tablename__ = "skills"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category = Column(String)

class CareerSkill(Base):
    __tablename__ = "career_skills"
    career_id = Column(UUID(as_uuid=True), ForeignKey("careers.id", ondelete="CASCADE"), primary_key=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True)
    weight = Column(Integer)

class StudentInsight(Base):
    __tablename__ = "student_insights"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    ai_summary = Column(Text)
    recommended_career_id = Column(UUID(as_uuid=True), ForeignKey("careers.id"))
    success_probability = Column(Float)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())