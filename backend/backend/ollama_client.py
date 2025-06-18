# ollama_client.py
# 處理與本地 Ollama API 的通訊

import json
import requests
import logging
from typing import Dict, Any, Optional

from config import (
    OLLAMA_API_URL,
    OLLAMA_MODEL,
    OLLAMA_TEMPERATURE,
    OLLAMA_MAX_TOKENS,
    DEFAULT_RESPONSE,
    TEST_MODE
)

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self):
        self.api_url = OLLAMA_API_URL
        self.model = OLLAMA_MODEL
        self.temperature = OLLAMA_TEMPERATURE
        self.max_tokens = OLLAMA_MAX_TOKENS
        
        # 檢查 Ollama 連線
        if not TEST_MODE:
            try:
                response = requests.get(f"{self.api_url}/api/tags")
                if response.status_code == 200:
                    models = response.json().get("models", [])
                    model_names = [m.get("name") for m in models]
                    if self.model not in model_names:
                        logger.warning(f"Model {self.model} not found in Ollama. Available models: {model_names}")
                    else:
                        logger.info(f"Successfully connected to Ollama. Using model: {self.model}")
                else:
                    logger.warning(f"Could not connect to Ollama API: {response.status_code}")
            except requests.RequestException as e:
                logger.warning(f"Could not connect to Ollama API: {e}")
    
    async def generate_response(self, prompt: str) -> Dict[str, Any]:
        """
        向 Ollama API 發送請求並返回回應
        
        Args:
            prompt: 發送給 Ollama 的提示詞
            
        Returns:
            解析後的 JSON 回應
        """
        if TEST_MODE:
            logger.info("TEST MODE: Using mock response instead of calling Ollama API")
            return self._get_mock_response()
        
        # 構建 API 請求
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
        
        # 重試計數器
        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries:
            try:
                response = requests.post(
                    f"{self.api_url}/api/generate",
                    headers=headers,
                    json=data
                )
                
                if response.status_code == 200:
                    try:
                        response_json = response.json()
                        # 從 Ollama 回應中提取文本
                        text_response = response_json.get('response', '')
                        
                        # 嘗試解析 JSON 回應
                        try:
                            parsed_json = json.loads(text_response)
                            logger.info("Successfully received and parsed Ollama response")
                            return parsed_json
                        except json.JSONDecodeError:
                            logger.error(f"Failed to parse Ollama response as JSON: {text_response}")
                            # 嘗試從文本中提取 JSON 部分
                            extracted_json = self._extract_json_from_text(text_response)
                            if extracted_json:
                                return extracted_json
                            return DEFAULT_RESPONSE
                    except (KeyError, IndexError) as e:
                        logger.error(f"Error parsing Ollama response structure: {e}")
                        
                else:
                    logger.error(f"Ollama API request failed with status code {response.status_code}: {response.text}")
                
                retry_count += 1
                
            except requests.RequestException as e:
                logger.error(f"Request to Ollama API failed: {e}")
                retry_count += 1
        
        logger.warning("All retries failed, using default response")
        return DEFAULT_RESPONSE
    
    def _extract_json_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """嘗試從文本中提取 JSON 部分"""
        try:
            # 嘗試找出文本中的 JSON 部分 (通常在 ```json 和 ``` 之間)
            if "```json" in text and "```" in text.split("```json", 1)[1]:
                json_text = text.split("```json", 1)[1].split("```", 1)[0].strip()
                return json.loads(json_text)
            
            # 尋找 { 開頭和 } 結尾的部分
            elif "{" in text and "}" in text:
                start = text.find("{")
                end = text.rfind("}") + 1
                if start < end:
                    json_text = text[start:end]
                    return json.loads(json_text)
                
        except (json.JSONDecodeError, IndexError):
            pass
        
        return None
    
    def _get_mock_response(self) -> Dict[str, Any]:
        """
        在測試模式中返回模擬回應
        """
        import random
        
        # 隨機選擇一個行為
        actions = ["idle", "walk", "jump", "eat"]
        action = random.choice(actions)
        
        if action == "idle":
            return {
                "action": "idle",
                "params": {
                    "duration": random.randint(5, 20)
                },
                "narration": "史萊姆感到疲倦，決定休息一下..."
            }
        elif action == "walk":
            return {
                "action": "walk",
                "params": {
                    "target_x": random.randint(10, 40),
                    "target_z": random.randint(10, 40),
                    "speed": random.choice(["slow", "medium", "fast"])
                },
                "narration": "史萊姆想探索周圍環境，開始移動..."
            }
        elif action == "jump":
            return {
                "action": "jump",
                "params": {
                    "height": random.choice(["low", "medium", "high"])
                },
                "narration": "史萊姆感到興奮，跳了起來！"
            }
        elif action == "eat":
            return {
                "action": "eat",
                "params": {},
                "narration": "史萊姆看到食物，決定吃一些補充能量..."
            }