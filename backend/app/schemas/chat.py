from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from app.models.chat import MessageRole


class MessageBase(BaseModel):
    """Base message schema."""
    role: MessageRole
    content: str


class MessageCreate(BaseModel):
    """Schema for creating a message."""
    content: str = Field(..., min_length=1)


class MessageResponse(MessageBase):
    """Schema for message response."""
    id: UUID
    chat_session_id: UUID
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ChatSessionResponse(BaseModel):
    """Schema for chat session response."""
    id: UUID
    project_id: UUID
    created_at: datetime
    messages: list[MessageResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


class ChatRequest(BaseModel):
    """Schema for chat request."""
    project_id: UUID
    message: str = Field(..., min_length=1)
    session_id: UUID | None = None


class ChatResponse(BaseModel):
    """Schema for chat response."""
    session_id: UUID
    message: MessageResponse
    assistant_message: MessageResponse
