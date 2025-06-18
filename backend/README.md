# SlimeHome Backend

AI-powered backend for the Slime Terrarium Simulator.

## Quick Start

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```

4. **Test the backend:**
   ```bash
   python run_tests.py
   ```

## Project Structure

```
backend/
├── main.py                 # Server entry point
├── run_tests.py           # Test runner
├── requirements.txt       # Dependencies  
├── .env.example          # Environment template
└── src/                  # Source code
    ├── config.py         # Configuration
    ├── api/              # FastAPI routes
    ├── clients/          # AI service clients
    ├── core/             # Business logic
    └── models/           # Data structures
```

## API Endpoints

- `GET /health` - Health check
- `POST /api/test` - Test endpoint for Godot client
- `WebSocket /ws` - Real-time communication (future)