import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class SessionLog(Base):
    __tablename__ = "sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    mentor_id = Column(UUID(as_uuid=True), ForeignKey("mentors.id"))
    scheduled_at = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer)
    status = Column(String)
    payment_status = Column(String)
    meeting_url = Column(String)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"))
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    message = Column(Text)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

class MentorFeedback(Base):
    __tablename__ = "mentor_feedback"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"))
    mentor_id = Column(UUID(as_uuid=True), ForeignKey("mentors.id"))
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    notes = Column(Text)
    action_items = Column(Text)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

class ParentFeedback(Base):
    __tablename__ = "parent_feedback"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    behavior_insights = Column(Text)
    study_habits = Column(Text)
    logged_at = Column(DateTime(timezone=True), server_default=func.now())