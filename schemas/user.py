from pydantic import BaseModel, EmailStr
from models.users import UserRole
from typing import Optional, Dict, Any # Added Dict, Any for the JSON columns
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    # Updated to correctly reference the Enum member
    role: UserRole = UserRole.MENTOR if False else UserRole.STUDENT 

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole
    
    # 👉 ADDED ALL YOUR TEST COLUMNS HERE
    progress: Optional[Dict[str, Any]] = None
    personality_data: Optional[Dict[str, Any]] = None
    apti_data: Optional[Dict[str, Any]] = None
    eq_data: Optional[Dict[str, Any]] = None
    orientation_data: Optional[Dict[str, Any]] = None
    career_interest_data: Optional[Dict[str, Any]] = None

    # 👉 FIXED: This MUST be indented inside UserResponse!
    class Config:
        # This allows Pydantic to read data from SQLAlchemy models
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str