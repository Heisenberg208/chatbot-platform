import asyncio
from typing import Any
import httpx

from app.services.llm.base import LLMProvider
from app.core.config import get_settings


class GroqProvider(LLMProvider):
    """Groq LLM provider implementation.
    
    Groq offers free-tier access to fast LLM inference with models like:
    - llama-3.3-70b-versatile
    - llama-3.1-8b-instant
    - mixtral-8x7b-32768
    - gemma2-9b-it
    
    Get your free API key at: https://console.groq.com/keys
    """
    
    def __init__(self):
        settings = get_settings()
        
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required for Groq provider")
        
        self.api_key = settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1"
        
        # Default to fast llama model if not specified
        default_model = "llama-3.3-70b-versatile"
        self.model = settings.LLM_MODEL if settings.LLM_MODEL != "gpt-3.5-turbo" else default_model
        
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.timeout = settings.LLM_TIMEOUT
    
    async def generate(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """
        Generate a response using Groq's API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
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
            raise Exception(f"Groq API timeout: {str(e)}")
        except httpx.HTTPStatusError as e:
            error_detail = e.response.text
            raise Exception(f"Groq API error: {e.response.status_code} - {error_detail}")
        except KeyError as e:
            raise Exception(f"Unexpected Groq API response format: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error calling Groq: {str(e)}")
    
    async def validate_connection(self) -> bool:
        """Validate Groq API connection."""
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
