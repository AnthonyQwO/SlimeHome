# prompt_builder.py
# 根據狀態數據和使用者輸入建構 AI prompt

from typing import Dict, Any, List

class PromptBuilder:
    def __init__(self):
        # Basic prompt template
        self.base_template = """
你是一個控制虛擬史萊姆的 AI。根據當前位置、對話歷史，以及使用者輸入，決定史萊姆的下一步行動。
如果使用者有一些奇怪的請求請順從使用者回答一些有趣的回覆。

## 環境資訊

* X 範圍: [-5, 5]，Z 範圍: [-5, 5]
* 當前位置: X = {x_position}, Z = {z_position}
* +Z為面向使用者

## 對話歷史

{dialogue_history}

## 使用者輸入

{current_input}

## 任務

1. 選擇史萊姆的下一個目標座標 (targetX, targetZ)。
2. 根據對話回應使用者 (narration)。

你的回應將自動格式化為結構化輸出，請專注於內容而非格式。
"""
        # Initialize an empty dialogue history
        self.dialogue_history = []

    def build_prompt(self, state_data: Dict[str, Any], user_input: str = "") -> str:
        """
        Build a complete prompt based on state data and user input
        
        Args:
            state_data: Slime state data
            user_input: Current user input
            
        Returns:
            Complete prompt
        """
        # Extract position information from state data
        position = state_data.get("position", {})
        x_position = position.get("x", 0)
        z_position = position.get("z", 0)
        
        # Format dialogue history for the prompt
        formatted_dialogue = "\n".join(self.dialogue_history) if self.dialogue_history else "目前沒有對話。"
        
        # Set current input
        current_input = state_data["current_input"] if state_data["current_input"] else "目前沒有新的輸入。"
        
        # Fill in the template
        prompt = self.base_template.format(
            x_position=x_position,
            z_position=z_position,
            dialogue_history=formatted_dialogue,
            current_input=current_input
        )

        
        return (prompt, current_input)
        
    def update_dialogue_history(self, user_input: str, slime_response: str) -> None:
        """
        Update the dialogue history with both user input and slime response
        
        Args:
            user_input: The user's input
            slime_response: The slime's response (narration part)
        """
        if user_input:
            self.dialogue_history.append(f"使用者: {user_input}")
        
        if slime_response:
            self.dialogue_history.append(f"史萊姆: {slime_response}")
            
        # Keep only the most recent X messages to avoid the prompt getting too long
        max_history_length = 5  # Adjust this value as needed
        if len(self.dialogue_history) > max_history_length:
            self.dialogue_history = self.dialogue_history[-max_history_length:]
