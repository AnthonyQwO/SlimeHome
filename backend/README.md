# SlimeHome Backend

AI-powered backend for the Slime Terrarium Simulator.

## Quick Start

1. **Install dependencies:**
   ```bash
   cd backend/backend
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

## API Keys Setup

### Gemini API (Google AI Studio)
1. Go to https://aistudio.google.com/app/apikey
2. Create a new API key
3. Add it to your `.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### Ollama (Local AI)
1. Install Ollama from https://ollama.com/
2. Pull a model: `ollama pull gemma3:12b`
3. Change `AI_SERVICE` to `"ollama"` in `src/config.py`

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

## Security Notes

⚠️ **Never commit `.env` files** - They contain sensitive API keys
✅ **Always use `.env.example`** - Template without real keys
✅ **Regenerate exposed keys** - If accidentally committed

## API Endpoints

- `GET /health` - Health check
- `POST /api/test` - Test endpoint for Godot client
- `WebSocket /ws` - Real-time communication (future)