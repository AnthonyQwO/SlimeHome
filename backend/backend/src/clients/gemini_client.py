# gemini_client.py
import json
import requests
import logging
from typing import Dict, Any, Optional

from config import (
    GEMINI_API_KEY,
    GEMINI_API_URL,
    GEMINI_TEMPERATURE,
    GEMINI_MAX_TOKENS,
    DEFAULT_RESPONSE
)

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.api_url = GEMINI_API_URL
        self.temperature = GEMINI_TEMPERATURE
        self.max_tokens = GEMINI_MAX_TOKENS
        
        if not self.api_key:
            logger.warning("Gemini API key not found. Please set GEMINI_API_KEY in .env file.")
    
    async def generate_response(self, prompt: str) -> Dict[str, Any]:
        """Send request to Gemini API and return response"""
        if not self.api_key:
            logger.error("No API key available")
            return DEFAULT_RESPONSE
        
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_tokens,
            }
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            
            if response.status_code == 200:
                response_json = response.json()
                text_response = response_json['candidates'][0]['content']['parts'][0]['text']
                
                # Try to parse as JSON
                try:
                    parsed_json = json.loads(text_response)
                    logger.info("Successfully received Gemini response")
                    return parsed_json
                except json.JSONDecodeError:
                    # Try to extract JSON from text
                    extracted_json = self._extract_json_from_text(text_response)
                    if extracted_json:
                        return extracted_json
                    logger.error(f"Failed to parse response: {text_response}")
                    return DEFAULT_RESPONSE
            else:
                logger.error(f"API request failed: {response.status_code} - {response.text}")
                return DEFAULT_RESPONSE
                
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return DEFAULT_RESPONSE
    
    def _extract_json_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from text response"""
        try:
            # Look for JSON in ```json blocks
            if "```json" in text and "```" in text.split("```json", 1)[1]:
                json_text = text.split("```json", 1)[1].split("```", 1)[0].strip()
                return json.loads(json_text)
            
            # Look for { } blocks
            elif "{" in text and "}" in text:
                start = text.find("{")
                end = text.rfind("}") + 1
                if start < end:
                    json_text = text[start:end]
                    return json.loads(json_text)
                    
        except (json.JSONDecodeError, IndexError):
            pass
        
        return None