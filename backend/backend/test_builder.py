# test_builder.py
from prompt_builder import PromptBuilder
import json

# 創建測試資料
test_data = {
    "current_state": "idle",
    "duration": 10,
    "position": {"x": 20, "y": 0, "z": 15},
    "hunger": 65,
    "happiness": 70,
    "food_present": True,
    "food_position": {"x": 35, "y": 0, "z": 15},
    "recent_actions": ["idle", "walk", "idle"]
}

# 初始化 PromptBuilder
builder = PromptBuilder()

# 嘗試建構提示詞
try:
    prompt = builder.build_prompt(test_data)
    print("成功建構提示詞！前 200 字元：")
    print(prompt[:200] + "...")
    
    # 嘗試從提示詞中提取 JSON 示例
    if "```json" in prompt and "```" in prompt.split("```json", 1)[1]:
        json_text = prompt.split("```json", 1)[1].split("```", 1)[0].strip()
        print("\n嘗試解析 JSON 示例：")
        json_obj = json.loads(json_text)
        print("JSON 有效！")
    
except Exception as e:
    print(f"錯誤：{e}")
    import traceback
    traceback.print_exc()