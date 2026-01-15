import asyncio
from typing import Any
import httpx

from app.services.llm.base import LLMProvider
from app.core.config import get_settings


class OpenRouterProvider(LLMProvider):
    """OpenRouter LLM provider implementation."""
    
    def __init__(self):
        settings = get_settings()
        
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is required for OpenRouter provider")
        
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = settings.LLM_MODEL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.timeout = settings.LLM_TIMEOUT
    
    async def generate(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """
        Generate a response using OpenRouter's API.
        
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
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://chatbot-platform.local",
                "X-Title": "Chatbot Platform",
            }
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                
                data = response.json()
                return data["choices"][0]["message"]["content"] or ""
                
        except httpx.TimeoutException as e:
            raise Exception(f"OpenRouter API timeout: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise Exception(f"OpenRouter API error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Unexpected error calling OpenRouter: {str(e)}")
    
    async def validate_connection(self) -> bool:
        """Validate OpenRouter API connection."""
        try:
            # Make a minimal API call to verify connection
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers=headers,
                )
                response.raise_for_status()
                return True
        except Exception:
            return False
