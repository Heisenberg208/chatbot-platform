from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class PromptBase(BaseModel):
    """Base prompt schema."""
    content: str = Field(..., min_length=1)


class PromptCreate(PromptBase):
    """Schema for creating a prompt."""
    pass


class PromptUpdate(BaseModel):
    """Schema for updating a prompt."""
    content: str | None = Field(None, min_length=1)


class PromptResponse(PromptBase):
    """Schema for prompt response."""
    id: UUID
    project_id: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PromptListResponse(BaseModel):
    """Schema for list of prompts."""
    prompts: list[PromptResponse]
    total: int
