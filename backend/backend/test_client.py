# test_client.py
# 用於手動測試後端功能的腳本

import json
import requests
import logging
import argparse
from typing import Dict, Any

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_test_state():
    """
    生成測試用的狀態數據
    
    Args:
        custom_values: 自定義的值，用於覆蓋默認值
        
    Returns:
        狀態數據字典
    """
    # 默認狀態
    state = {
        "current_state": "idle",
        "duration": 10,
        "position": {"x": -1, "y": 0, "z": 1},
        "hunger": 5,
        "happiness": 10,
        "food_present": True,
        "food_position": {"x": 35, "y": 0, "z": 15},
        "recent_actions": ["idle", "walk", "idle"],
        "current_input": "滾！"
    }
    
    return state

def test_api(state, server_url="http://localhost:8000"):
    """
    測試 API 端點
    
    Args:
        state: 狀態數據
        server_url: 服務器 URL
        
    Returns:
        API 回應
    """
    # 確保 URL 有正確的協議前綴
    endpoint = f"{server_url}/api/test"
    try:
        response = requests.post(
            endpoint,
            json=state,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"API request failed with status code {response.status_code}: {response.text}")
            return None
            
    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
        return None

if __name__ == "__main__":
    
    # 默認測試
    print("進行默認測試 (使用默認狀態)")
    state = generate_test_state()
    response = test_api(state)
    if response:
        print("\n後端回應:")
        print(json.dumps(response, indent=2, ensure_ascii=False))