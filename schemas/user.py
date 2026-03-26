from pydantic import BaseModel, EmailStr
from models.users import UserRole
from typing import Optional
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole = UserRole.student

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str