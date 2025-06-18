# gemini_client.py
# 處理與 Gemini API 的通訊

import json
import requests
import logging
from typing import Dict, Any, Optional

from config import (
    GEMINI_API_KEY,
    GEMINI_API_URL,
    GEMINI_TEMPERATURE,
    GEMINI_MAX_TOKENS,
    DEFAULT_RESPONSE,
    TEST_MODE
)

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.api_url = GEMINI_API_URL
        self.temperature = GEMINI_TEMPERATURE
        self.max_tokens = GEMINI_MAX_TOKENS
        
        # 檢查 API 金鑰
        if not self.api_key and not TEST_MODE:
            logger.warning("Gemini API key not found. Set TEST_MODE=True or provide API key.")
    
    async def generate_response(self, prompt: str) -> Dict[str, Any]:
        """
        向 Gemini API 發送請求並返回回應
        
        Args:
            prompt: 發送給 Gemini 的提示詞
            
        Returns:
            解析後的 JSON 回應
        """
        if TEST_MODE:
            logger.info("TEST MODE: Using mock response instead of calling Gemini API")
            return self._get_mock_response()
        
        # 構建 API 請求
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
        
        # 重試計數器
        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries:
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=data
                )
                
                if response.status_code == 200:
                    try:
                        response_json = response.json()
                        # 從 Gemini 回應中提取文本
                        text_response = response_json['candidates'][0]['content']['parts'][0]['text']
                        
                        # 嘗試解析 JSON 回應
                        try:
                            parsed_json = json.loads(text_response)
                            logger.info("Successfully received and parsed Gemini response")
                            return parsed_json
                        except json.JSONDecodeError:
                            logger.error(f"Failed to parse Gemini response as JSON: {text_response}")
                            # 嘗試從文本中提取 JSON 部分
                            extracted_json = self._extract_json_from_text(text_response)
                            if extracted_json:
                                return extracted_json
                            return DEFAULT_RESPONSE
                    except (KeyError, IndexError) as e:
                        logger.error(f"Error parsing Gemini response structure: {e}")
                        
                else:
                    logger.error(f"Gemini API request failed with status code {response.status_code}: {response.text}")
                
                retry_count += 1
                
            except requests.RequestException as e:
                logger.error(f"Request to Gemini API failed: {e}")
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