# ollama_client.py
import json
import requests
import logging
from typing import Dict, Any, Optional

from config import (
    OLLAMA_API_URL,
    OLLAMA_MODEL,
    OLLAMA_TEMPERATURE,
    OLLAMA_MAX_TOKENS,
    DEFAULT_RESPONSE
)

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self):
        self.api_url = OLLAMA_API_URL
        self.model = OLLAMA_MODEL
        self.temperature = OLLAMA_TEMPERATURE
        self.max_tokens = OLLAMA_MAX_TOKENS
        
        # Check Ollama connection
        try:
            response = requests.get(f"{self.api_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m.get("name") for m in models]
                if self.model not in model_names:
                    logger.warning(f"Model {self.model} not found. Available: {model_names}")
                else:
                    logger.info(f"Connected to Ollama. Using model: {self.model}")
            else:
                logger.warning(f"Could not connect to Ollama: {response.status_code}")
        except requests.RequestException as e:
            logger.warning(f"Could not connect to Ollama: {e}")
    
    async def generate_response(self, prompt: str) -> Dict[str, Any]:
        """Send request to Ollama API and return response"""
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/api/generate",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                response_json = response.json()
                text_response = response_json.get('response', '')
                
                # Try to parse as JSON
                try:
                    parsed_json = json.loads(text_response)
                    logger.info("Successfully received Ollama response")
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