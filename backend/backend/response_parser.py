# response_parser.py
# 處理並驗證 AI 回應

import json
import logging
from typing import Dict, Any, Optional

from config import DEFAULT_RESPONSE

logger = logging.getLogger(__name__)

class ResponseParser:
    def __init__(self):
        # 有效的行為列表
        self.valid_actions = ["idle", "walk", "jump", "eat", "frightened"]
        
        # 各行為所需的參數
        self.required_params = {
            "idle": ["duration"],
            "walk": ["target_x", "target_z", "speed"],
            "jump": ["height"],
            "eat": [],
            "frightened": []
        }
        
        # 參數的有效值範圍
        self.param_constraints = {
            "duration": (2, 30),  # 範圍: 2-30 秒
            "target_x": (0, 100),  # 範圍: 0-100
            "target_z": (0, 100),  # 範圍: 0-100
            "speed": ["slow", "medium", "fast"],  # 列舉值
            "height": ["low", "medium", "high"]   # 列舉值
        }
    
    def parse_and_validate(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析並驗證 AI 回應
        
        Args:
            response_data: 從 AI 獲得的回應
            
        Returns:
            驗證過的回應 (如有必要會修正)
        """
        # 檢查基本結構
        if not isinstance(response_data, dict):
            logger.error(f"Response is not a dictionary: {response_data}")
            return DEFAULT_RESPONSE
        
        # 提取主要字段
        action = response_data.get("action")
        params = response_data.get("params", {})
        narration = response_data.get("narration", "")
        
        # 檢查行為是否有效
        if action not in self.valid_actions:
            logger.warning(f"Invalid action: {action}, using default")
            return DEFAULT_RESPONSE
        
        # 檢查是否包含所需參數
        valid_params = {}
        for param in self.required_params[action]:
            if param not in params:
                logger.warning(f"Missing required parameter {param} for action {action}")
                # 使用預設值
                if param == "duration":
                    valid_params[param] = 10  # 預設持續 10 秒
                elif param == "target_x" or param == "target_z":
                    valid_params[param] = 20  # 預設位置 20
                elif param == "speed":
                    valid_params[param] = "medium"  # 預設中速
                elif param == "height":
                    valid_params[param] = "medium"  # 預設中高度
            else:
                param_value = params[param]
                # 驗證並修正參數值
                if param in self.param_constraints:
                    constraint = self.param_constraints[param]
                    
                    # 範圍檢查
                    if isinstance(constraint, tuple):
                        min_val, max_val = constraint
                        if not isinstance(param_value, (int, float)):
                            try:
                                param_value = float(param_value)
                                if param in ["duration", "target_x", "target_z"]:
                                    param_value = int(param_value)
                            except (ValueError, TypeError):
                                param_value = (min_val + max_val) // 2  # 使用範圍的中間值
                        
                        param_value = max(min_val, min(max_val, param_value))  # 限制在範圍內
                    
                    # 列舉值檢查
                    elif isinstance(constraint, list):
                        if param_value not in constraint:
                            param_value = constraint[0]  # 使用第一個有效值
                
                valid_params[param] = param_value
        
        # 構建驗證後的回應
        validated_response = {
            "action": action,
            "params": valid_params,
            "narration": narration if narration else f"史萊姆正在{action}..."
        }
        
        return validated_response