from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.project import Project
from app.models.chat import ChatSession, Message, MessageRole
from app.models.prompt import Prompt
from app.services.llm.base import LLMProvider
from app.services.llm.openai import OpenAIProvider
from app.services.llm.openrouter import OpenRouterProvider
from app.services.llm.groq import GroqProvider
from app.core.config import get_settings


class ChatService:
    """Service for handling chat operations with LLM integration."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.llm_provider = self._get_llm_provider()
    
    def _get_llm_provider(self) -> LLMProvider:
        """Get the configured LLM provider."""
        settings = get_settings()
        
        if settings.LLM_PROVIDER == "openai":
            return OpenAIProvider()
        elif settings.LLM_PROVIDER == "openrouter":
            return OpenRouterProvider()
        elif settings.LLM_PROVIDER == "groq":
            return GroqProvider()
        else:
            raise ValueError(f"Unknown LLM provider: {settings.LLM_PROVIDER}")
    
    async def get_or_create_session(
        self,
        project_id: UUID,
        session_id: UUID | None = None
    ) -> ChatSession:
        """Get existing session or create a new one."""
        if session_id:
            result = await self.db.execute(
                select(ChatSession)
                .where(ChatSession.id == session_id)
                .where(ChatSession.project_id == project_id)
                .options(selectinload(ChatSession.messages))
            )
            session = result.scalar_one_or_none()
            
            if session:
                return session
        
        # Create new session
        session = ChatSession(project_id=project_id)
        self.db.add(session)
        await self.db.flush()
        
        return session
    
    async def build_messages(
        self,
        project: Project,
        chat_session: ChatSession,
        user_message: str
    ) -> list[dict[str, str]]:
        """Build message list for LLM from project prompts and chat history."""
        messages = []
        
        # Load prompts for the project
        result = await self.db.execute(
            select(Prompt)
            .where(Prompt.project_id == project.id)
            .order_by(Prompt.created_at)
        )
        prompts = result.scalars().all()
        
        # Add system prompts
        for prompt in prompts:
            messages.append({
                "role": "system",
                "content": prompt.content
            })
        
        # If no prompts, add default system message
        if not prompts:
            messages.append({
                "role": "system",
                "content": f"You are a helpful assistant for {project.name}."
            })
        
        # Add chat history (load messages if not already loaded)
        # Load chat history explicitly (never touch lazy relationships)
        result = await self.db.execute(
            select(Message)
            .where(Message.chat_session_id == chat_session.id)
            .order_by(Message.timestamp)
        )
        history_messages = result.scalars().all()

        for msg in history_messages:
            if msg.role != MessageRole.SYSTEM:
                messages.append({
                    "role": msg.role.value,
                    "content": msg.content
                })

        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return messages
    
    async def generate_response(
        self,
        project_id: UUID,
        user_id: UUID,
        user_message: str,
        session_id: UUID | None = None
    ) -> tuple[ChatSession, Message, Message]:
        """
        Generate a response from the LLM.
        
        Returns:
            Tuple of (chat_session, user_message, assistant_message)
        """
        # Verify project ownership
        result = await self.db.execute(
            select(Project)
            .where(Project.id == project_id)
            .where(Project.user_id == user_id)
        )
        project = result.scalar_one_or_none()
        
        if not project:
            raise ValueError("Project not found or access denied")
        
        # Get or create session
        chat_session = await self.get_or_create_session(project_id, session_id)
        
        # Build messages for LLM
        messages = await self.build_messages(project, chat_session, user_message)
        
        # Save user message
        user_msg = Message(
            chat_session_id=chat_session.id,
            role=MessageRole.USER,
            content=user_message
        )
        self.db.add(user_msg)
        await self.db.flush()
        
        # Generate response from LLM
        try:
            assistant_content = await self.llm_provider.generate(messages)
        except Exception as e:
            # Log error and provide fallback response
            assistant_content = f"I apologize, but I encountered an error: {str(e)}"
        
        # Save assistant message
        assistant_msg = Message(
            chat_session_id=chat_session.id,
            role=MessageRole.ASSISTANT,
            content=assistant_content
        )
        self.db.add(assistant_msg)
        await self.db.flush()
        
        return chat_session, user_msg, assistant_msg
