import uuid
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from core.database import Base

class Test(Base):
    __tablename__ = "tests"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    total_questions = Column(Integer)

class Result(Base):
    __tablename__ = "results"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    test_id = Column(UUID(as_uuid=True), ForeignKey("tests.id", ondelete="CASCADE"))
    overall_score = Column(Float)
    speed_score = Column(Float)
    accuracy_score = Column(Float)
    consistency_score = Column(Float)
    weakness_mapping = Column(JSONB)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())