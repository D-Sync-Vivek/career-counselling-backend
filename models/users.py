import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from core.database import Base
from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
class UserRole(str, enum.Enum):
    STUDENT = "student"
    MENTOR = "mentor"
    ADMIN = "admin"
    PARENT = "parent"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, nullable=False, default="student")
    invite_code = Column(String(6), nullable=True, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    mentor_profile = relationship("Mentor", back_populates="user", uselist=False)

    # --- Career Engine JSONB Blocks ---
    academic_data = Column(JSONB, nullable=True)
    apti_data = Column(JSONB, nullable=True)
    personality_data = Column(JSONB, nullable=True)
    lifestyle_data = Column(JSONB, nullable=True)
    financial_data = Column(JSONB, nullable=True)
    passion_strength_data = Column(JSONB, nullable=True)
    aspiration_data = Column(JSONB, nullable=True)
    career_interest_data = Column(JSONB, nullable=True)
    eq_data = Column(JSONB, nullable=True)
    orientation_data = Column(JSONB, nullable=True)
    def __repr__(self):
        return f"<User {self.email}>"
class CareerDiscoveryReport(Base):
    __tablename__ = "career_discovery_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="pending")
    
    five_dimensions_data = Column(JSONB, nullable=True)
    career_matches_data = Column(JSONB, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Create a relationship back to the user
    user = relationship("User", backref="career_reports")