import asyncio
from typing import Any
import httpx
from openai import AsyncOpenAI, OpenAIError, APITimeoutError

from app.services.llm.base import LLMProvider
from app.core.config import get_settings


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation."""
    
    def __init__(self):
        settings = get_settings()
        
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for OpenAI provider")
        
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=httpx.Timeout(settings.LLM_TIMEOUT, connect=5.0),
        )
        self.model = settings.LLM_MODEL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS
    
    async def generate(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """
        Generate a response using OpenAI's API.
        
        Args:
            messages: List of message dictionaries
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
            
        Returns:
            Generated response text
            
        Raises:
            Exception: If API call fails
        """
        try:
            # Override defaults with kwargs
            temperature = kwargs.get("temperature", self.temperature)
            max_tokens = kwargs.get("max_tokens", self.max_tokens)
            model = kwargs.get("model", self.model)
            
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            return response.choices[0].message.content or ""
            
        except APITimeoutError as e:
            raise Exception(f"OpenAI API timeout: {str(e)}")
        except OpenAIError as e:
            raise Exception(f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error calling OpenAI: {str(e)}")
    
    async def validate_connection(self) -> bool:
        """Validate OpenAI API connection."""
        try:
            # Make a minimal API call to verify connection
            await self.client.models.list()
            return True
        except Exception:
            return False
