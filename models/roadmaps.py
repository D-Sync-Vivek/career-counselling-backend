import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from core.database import Base

class Roadmap(Base):
    __tablename__ = "roadmaps"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    career_id = Column(UUID(as_uuid=True), ForeignKey("careers.id"))
    total_months = Column(Integer)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

class RoadmapMilestone(Base):
    __tablename__ = "roadmap_milestones"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roadmap_id = Column(UUID(as_uuid=True), ForeignKey("roadmaps.id", ondelete="CASCADE"))
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"))
    month_number = Column(Integer)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="pending")
    completed_at = Column(DateTime(timezone=True))