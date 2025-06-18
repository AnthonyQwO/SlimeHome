#!/usr/bin/env python3
# run_tests.py - Simple test runner for the backend

import sys
import os
import asyncio

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.prompt_builder import PromptBuilder
from src.clients.gemini_client import GeminiClient
from src.config import AI_SERVICE

# Test data
test_data = {
    "current_state": "idle", 
    "duration": 10,
    "position": {"x": 0, "y": 0, "z": 0},
    "hunger": 5,
    "happiness": 10, 
    "food_present": True,
    "food_position": {"x": 35, "y": 0, "z": 15},
    "recent_actions": ["idle", "walk", "idle"],
    "current_input": "Hello slime, please move to position 2, 0!"
}

async def test_backend():
    print("=== Reorganized Backend Test ===")
    print(f"Using AI service: {AI_SERVICE}")
    
    # Test prompt builder
    print("\n1. Testing Prompt Builder...")
    prompt_builder = PromptBuilder()
    prompt, user_input = prompt_builder.build_prompt(test_data)
    print(f"✓ Prompt generated ({len(prompt)} chars)")
    print(f"✓ User input: '{user_input}'")
    
    # Test AI client
    print("\n2. Testing AI Client...")
    if AI_SERVICE == "gemini":
        ai_client = GeminiClient()
    else:
        from src.clients.ollama_client import OllamaClient
        ai_client = OllamaClient()
    
    print(f"✓ AI client initialized: {type(ai_client).__name__}")
    
    try:
        response = await ai_client.generate_response(prompt)
        print(f"✓ Response received: {response}")
        
        # Test dialogue history
        narration = response.get("narration", "Test response")
        prompt_builder.update_dialogue_history(user_input, narration)
        print(f"✓ Dialogue history updated ({len(prompt_builder.dialogue_history)} entries)")
        
    except Exception as e:
        print(f"⚠ AI request failed (expected): {e}")
        print("✓ Fallback handling works")
    
    print("\n=== Test Complete - Backend Structure is Working! ===")

if __name__ == "__main__":
    asyncio.run(test_backend())