# SlimeHome

![SlimeHome Example](./image/example.gif)

## 專案簡介

**SlimeHome** 是一個結合 LLM API 與 Godot 引擎開發的互動式可愛史萊姆小遊戲。使用者可以透過自然語言與史萊姆互動。

## 專案展示影片

[觀看 YouTube 示範影片](https://www.youtube.com/watch?v=AZt7r733Zic)

## 🔧 使用技術

* **Godot Engine 4.x**：跨平台遊戲開發引擎
* **Python FastAPI**：後端 API 架構
* **LLM API（gemini 或 ollama）**：自然語言處理

## 專案結構簡述

```
SlimeHome/
├── assets/                # 遊戲圖像與素材
│   ├── icons/
│   └── images/
├── backend/              # Python FastAPI 後端
│   └── src/
│       ├── api/
│       ├── clients/
│       ├── core/
│       ├── models/
├── image/                # 專案展示圖像與 GIF
│   └── example.gif
├── scenes/               # Godot 遊戲場景
│   ├── characters/
│   ├── environment/
│   ├── main/
│   ├── network/
│   └── ui/
└── scripts/              # GDScript 腳本
    ├── characters/
    ├── components/
    ├── controllers/
    ├── network/
    └── ui/
```

## 系統架構

```mermaid
graph TB
    %% User Interaction
    User[User]
    
    %% Frontend - Godot 4.4
    subgraph "Frontend - Godot 4.4"
        direction TB
        
        subgraph "Game Engine"
            Character[Slime Character<br/>Navigation + Manual Control]
            UI[UI System<br/>Text Input/Output]
            World[3D Environment<br/>Navigation Mesh]
        end
        
        HttpClient[HTTP Client<br/>Backend Communication]
    end
    
    %% Backend Python Architecture
    subgraph "Backend - Python 3.11+ FastAPI"
        direction TB
        
        MainEntry[main.py<br/>Entry Point]
        
        subgraph "FastAPI Application: app.py"
            
            subgraph "API Endpoints"
                HealthAPI[GET /health<br/>Health Check]
                WebSocketAPI[WebSocket /ws<br/>Real-time Comm]
                TestAPI[POST /api/test<br/>Main Godot Endpoint]
            end

            FastAPIApp[FastAPI Server<br/>localhost:8000]
        end
        
        subgraph "Core Business Logic"
            PromptBuilder[prompt_builder.py<br/>Dialogue History<br/>Template Building]
            AIOrchestrator[AI Client Management<br/>Response Processing]
        end
        
        subgraph "AI Client Layer"
            GeminiClient[gemini_client.py<br/>google-genai SDK<br/>Structured Output]
            OllamaClient[ollama_client.py<br/>Local Alternative]
        end
        
        subgraph "Data Models"
            SlimeStateModel[slime_state.py<br/>SlimeState<br/>Position, AIResponse]
            PydanticValidation[Pydantic v2<br/>Type Validation]
        end
        
        subgraph "Configuration"
            ConfigModule[config.py<br/>Environment Variables<br/>API Keys, Debug Mode]
            EnvFile[.env<br/>GEMINI_API_KEY<br/>DEBUG_MODE]
        end
    end
    
    %% External AI Services
    subgraph "AI Services"
        GeminiAPI[Gemini 2.0 Flash Lite<br/>Structured JSON Output<br/>Chinese Language Support]
        OllamaAPI[Ollama<br/>Local LLM Models]
        GoogleAIStudio[Google AI Studio<br/>API Key Management]
    end
    
    %% Data Flow
    User -->|Manual Input<br/>WASD/Mouse| Character
    User -->|Text Commands| UI
    
    UI -->|User Message<br/>Character State| HttpClient
    HttpClient -->|HTTP POST<br/>JSON Payload| TestAPI
    
    TestAPI --> PromptBuilder
    PromptBuilder --> AIOrchestrator
    AIOrchestrator --> GeminiClient
    AIOrchestrator --> OllamaClient
    
    GeminiClient -->|Structured Output| GeminiAPI
    OllamaClient --> OllamaAPI
    GeminiAPI -.->|API Keys| GoogleAIStudio
    
    GeminiAPI -->|Navigation + Narration| TestAPI
    TestAPI -->|AI Response| HttpClient
    HttpClient -->|Commands + Text| Character
    HttpClient -->|Display Text| UI
    
    %% Styling
    classDef frontend fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef backend fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef ai fill:#fff8e1,stroke:#f57c00,stroke-width:2px
    classDef config fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    
    class Character,UI,World,HttpClient frontend
    class FastAPIApp,HealthAPI,TestAPI,WebSocketAPI,PromptBuilder,AIOrchestrator,SlimeStateModel,PydanticValidation backend
    class GeminiClient,OllamaClient,GeminiAPI,OllamaAPI ai
    class ConfigModule,EnvFile,GoogleAIStudio config
```

### Architecture Overview

**Frontend (Godot 4.4)**
- Character system with dual control (manual + AI navigation)
- UI system for text input/output
- 3D environment with navigation mesh
- HTTP client for backend communication

**Backend (Python FastAPI)**
- API gateway with REST endpoints and WebSocket support
- AI orchestration managing multiple services (Gemini/Ollama)
- Context-aware dialogue system with conversation history
- Pydantic v2 data validation for type safety

**AI Services**
- Primary: Gemini 2.0 Flash Lite with structured JSON output
- Fallback: Ollama for local processing
- Features: Guaranteed response format, multilingual support

### Data Flow

```
User Input → UI System → HTTP Request → AI Processing → Structured Response → Character Action + UI Update
```


## 快速開始

1. 安裝 [Godot Engine](https://godotengine.org/)
2. 開啟本專案後開啟 `scenes/main/Main.tscn`
3. 在 `backend` 中設定你的 LLM API 金鑰，詳見 `backend/README.md`
4. 啟動後端 FastAPI Sever
5. 點擊執行，開始與可愛的史萊姆互動！

