from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging
logger = logging.getLogger(__name__)

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.core.dependencies import CurrentUser
from app.db.session import get_db

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Send a message and receive a response from the LLM.
    
    This endpoint:
    1. Loads the project and its prompts
    2. Builds the message context (system prompts + chat history)
    3. Calls the configured LLM provider
    4. Persists both user and assistant messages
    5. Returns the assistant's response
    """
    chat_service = ChatService(db)
    
    try:
        session, user_msg, assistant_msg = await chat_service.generate_response(
            project_id=chat_request.project_id,
            user_id=current_user.id,
            user_message=chat_request.message,
            session_id=chat_request.session_id,
        )
        
        await db.commit()
        
        return ChatResponse(
            session_id=session.id,
            message=user_msg,
            assistant_message=assistant_msg,
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        await db.rollback()
        logger.exception("CHAT ENDPOINT CRASHED")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate response: {str(e)}",
        )
