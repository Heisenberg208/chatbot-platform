from fastapi import APIRouter

from app.schemas.user import UserResponse
from app.core.dependencies import CurrentUser

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentUser):
    """Get current authenticated user information."""
    return current_user
