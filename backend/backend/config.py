# config.py
# 設定檔，存放 API 金鑰與其他設定

import os
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()

# Gemini API 設定
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"
GEMINI_TEMPERATURE = 0.3  # 控制隨機性 (0.0-1.0)
GEMINI_MAX_TOKENS = 500  # 最大回應長度

# WebSocket 設定
WS_HOST = "0.0.0.0"
WS_PORT = 8000

# 應用程式設定
DEBUG_MODE = True
LOG_LEVEL = "INFO"

# 預設回應 (當 API 呼叫失敗時使用)
DEFAULT_RESPONSE = {
    "action": "idle",
    "params": {
        "duration": 10
    },
    "narration": "史萊姆正在休息..."
}

# 測試模式 (若為 True，則不實際呼叫 Gemini API，而是使用模擬回應)
TEST_MODE = False

# Ollama API 設定
OLLAMA_API_URL = "http://localhost:11434"  # Ollama 預設運行在 11434 端口
OLLAMA_MODEL = "gemma3:12b"#"llama3.2"  # 使用的模型名稱（確保已下載）
OLLAMA_TEMPERATURE = 0.3
OLLAMA_MAX_TOKENS = 1000

# 選擇使用哪個 AI 服務（"gemini" 或 "ollama"）
AI_SERVICE = "ollama"# config.py 新增以下設定