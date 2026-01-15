from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str


class UserResponse(UserBase):
    """Schema for user response."""
    id: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserBase):
    """Schema for user in database."""
    id: UUID
    hashed_password: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
