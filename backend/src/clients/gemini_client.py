# gemini_client.py
import logging
from google import genai
from typing import Dict, Any

from src.config import (
    GEMINI_API_KEY,
    GEMINI_TEMPERATURE,
    GEMINI_MAX_TOKENS,
    DEFAULT_RESPONSE,
    DEBUG_MODE
)
from src.models.slime_state import AIResponse

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.temperature = GEMINI_TEMPERATURE
        self.max_tokens = GEMINI_MAX_TOKENS
        
        if not self.api_key:
            logger.warning("Gemini API key not found. Please set GEMINI_API_KEY in .env file.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)
    
    async def generate_response(self, prompt: str) -> Dict[str, Any]:
        """Send request to Gemini API and return structured response"""
        if not self.client:
            logger.error("No API key available")
            return DEFAULT_RESPONSE
        
        logger.info("Sending user prompt to Gemini API...")
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": AIResponse,
                    "temperature": self.temperature,
                    "max_output_tokens": self.max_tokens,
                }
            )
            
            # Use the parsed structured response
            structured_response: AIResponse = response.parsed
            result = structured_response.model_dump()
            
            logger.info(f"Slime says: {result['narration']}")
            return result
                
        except Exception as e:
            logger.error(f"Request failed: {e}")
            if DEBUG_MODE:
                logger.debug(f"Full error details: {str(e)}")
            return DEFAULT_RESPONSE