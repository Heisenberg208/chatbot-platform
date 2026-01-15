from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.schemas.prompt import PromptCreate, PromptResponse, PromptListResponse
from app.models.prompt import Prompt
from app.models.project import Project
from app.core.dependencies import CurrentUser
from app.db.session import get_db

router = APIRouter()


@router.post("/{project_id}/prompts", response_model=PromptResponse, status_code=status.HTTP_201_CREATED)
async def create_prompt(
    project_id: UUID,
    prompt_data: PromptCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Create a new prompt for a project."""
    # Verify project ownership
    result = await db.execute(
        select(Project)
        .where(Project.id == project_id)
        .where(Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    prompt = Prompt(
        project_id=project_id,
        content=prompt_data.content,
    )
    
    db.add(prompt)
    await db.commit()
    await db.refresh(prompt)
    
    return prompt


@router.get("/{project_id}/prompts", response_model=PromptListResponse)
async def list_prompts(
    project_id: UUID,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """List all prompts for a project."""
    # Verify project ownership
    result = await db.execute(
        select(Project)
        .where(Project.id == project_id)
        .where(Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    # Get total count
    count_result = await db.execute(
        select(func.count(Prompt.id)).where(Prompt.project_id == project_id)
    )
    total = count_result.scalar_one()
    
    # Get prompts
    result = await db.execute(
        select(Prompt)
        .where(Prompt.project_id == project_id)
        .order_by(Prompt.created_at)
    )
    prompts = result.scalars().all()
    
    return {"prompts": prompts, "total": total}
