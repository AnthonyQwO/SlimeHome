# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"
GEMINI_TEMPERATURE = 0.3
GEMINI_MAX_TOKENS = 500

# Ollama API settings
OLLAMA_API_URL = "http://localhost:11434"
OLLAMA_MODEL = "gemma3:12b"
OLLAMA_TEMPERATURE = 0.3
OLLAMA_MAX_TOKENS = 1000

# Server settings
WS_HOST = "0.0.0.0"
WS_PORT = 8000
LOG_LEVEL = "INFO"

# AI service selection ("gemini" or "ollama")
AI_SERVICE = "gemini"

# Default response for API failures
DEFAULT_RESPONSE = {
    "params": {
        "targetX": 0,
        "targetZ": 0
    },
    "narration": "Slime is resting... (THIS IS A DEFAULT_RESPONSE)"
}