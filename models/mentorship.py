import uuid
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime, Integer, Text, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from core.database import Base

class Mentor(Base):
    __tablename__ = "mentors"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    expertise = Column(String, nullable=False)
    expertise_vector = Column(Vector(384)) 
    bio = Column(Text, nullable=True)
    years_experience = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    is_verified = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="mentor_profile")
    availability = relationship("MentorAvailability", backref="mentor", cascade="all, delete-orphan")

class MentorAvailability(Base):
    __tablename__ = "mentor_availability"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mentor_id = Column(UUID(as_uuid=True), ForeignKey("mentors.id", ondelete="CASCADE"))
    day_of_week = Column(Integer, nullable=False) # 1=Mon, 7=Sun
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_booked = Column(Boolean, default=False)

class MentorshipRequest(Base):
    __tablename__ = "mentorship_requests"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    mentor_id = Column(UUID(as_uuid=True), ForeignKey("mentors.id", ondelete="CASCADE"), nullable=False)
    availability_id = Column(UUID(as_uuid=True), ForeignKey("mentor_availability.id", ondelete="CASCADE"), nullable=True)
    message = Column(Text, nullable=True)
    status = Column(String, default="pending", nullable=False)
    request_type = Column(String, default="session", nullable=False)  # 'session' or 'connection'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class SessionLog(Base):
    __tablename__ = "sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),nullable=True)
    mentor_id = Column(UUID(as_uuid=True), ForeignKey("mentors.id", ondelete="CASCADE"))
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, default=60)
    status = Column(String, default="scheduled")
    meeting_url = Column(String, nullable=True)
    dyte_meeting_id = Column(String, nullable=True)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    mentor_id = Column(UUID(as_uuid=True), ForeignKey("mentors.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message = Column(Text, nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

class MentorFeedback(Base):
    __tablename__ = "mentor_feedback"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"))
    mentor_id = Column(UUID(as_uuid=True), ForeignKey("mentors.id", ondelete="CASCADE"))
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    notes = Column(Text)
    action_items = Column(Text)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

class ParentFeedback(Base):
    __tablename__ = "parent_feedback"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    behavior_insights = Column(Text)
    study_habits = Column(Text)
    logged_at = Column(DateTime(timezone=True), server_default=func.now())

class ParentStudentLink(Base):
    __tablename__ = "parent_student_links"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    linked_at = Column(DateTime(timezone=True), server_default=func.now())