# app.py
# FastAPI 應用程式與 WebSocket 處理

import json
import logging
import asyncio
from typing import Dict, Any, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.clients.gemini_client import GeminiClient
from src.clients.ollama_client import OllamaClient
from src.config import AI_SERVICE

from src.core.prompt_builder import PromptBuilder
from src.config import WS_HOST, WS_PORT, LOG_LEVEL, LOG_FORMAT

# 設定日誌
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="Slime Simulation Backend",
    description="AI-powered backend for interactive slime simulation",
    version="0.1.0"
)

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源，生產環境中應該限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
if AI_SERVICE == "ollama":
    ai_client = OllamaClient()
    logger.info("Using Ollama AI service")
else:
    ai_client = GeminiClient()
    logger.info("Using Gemini AI service")
prompt_builder = PromptBuilder()

# Store active connections
active_connections: List[WebSocket] = []

@app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 連接處理"""
    await websocket.accept()
    active_connections.append(websocket)
    logger.info(f"WebSocket client connected. Active connections: {len(active_connections)}")
    
    try:
        while True:
            # 接收來自客戶端的消息
            data = await websocket.receive_text()
            logger.debug(f"Received data: {data}")
            
            try:
                state_data = json.loads(data)
                
                # 處理狀態數據
                prompt = prompt_builder.build_prompt(state_data)
                ai_response = await ai_client.generate_response(prompt)
                
                # 返回處理後的回應
                await websocket.send_text(json.dumps(ai_response))
                logger.debug(f"Sent response: {ai_response}")
                
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON received: {e}")
                await websocket.send_text(json.dumps({"error": "Invalid JSON format"}))
            
            except Exception as e:
                logger.error(f"Error processing request: {e}")
                await websocket.send_text(json.dumps({"error": str(e)}))
    
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info(f"WebSocket client disconnected. Active connections: {len(active_connections)}")

@app.post("/api/test")
async def test_endpoint(state_data: Dict[str, Any]):
    """
    測試 API 端點，模擬 WebSocket 通訊
    用於在沒有 Godot 客戶端的情況下測試
    """
    try:
        (prompt, user_input) = prompt_builder.build_prompt(state_data)
        ai_response = await ai_client.generate_response(prompt)
        logger.info(f"AI response received: {ai_response}")
        prompt_builder.update_dialogue_history(user_input, ai_response)
        return ai_response
    
    except Exception as e:
        logger.error(f"Error in test endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
async def startup_event():
    """應用程式啟動時執行"""
    logger.info("Starting Slime Simulation Backend")

@app.on_event("shutdown")
async def shutdown_event():
    """應用程式關閉時執行"""
    logger.info("Shutting down Slime Simulation Backend")

def start():
    """啟動應用程式"""
    uvicorn.run(app, host=WS_HOST, port=WS_PORT)

if __name__ == "__main__":
    start()