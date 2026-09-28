# PocketSmart AI

Complete FastAPI/Jinja2 implementation of the supplied PocketSmart AI documentation.

## Run in VS Code

Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

Optional Gemini setup: put your API key in `.env` as `GEMINI_API_KEY=...`.
Without a key, the app uses deterministic local fallback recommendations so every planner remains testable.

API docs: http://127.0.0.1:8000/docs
Health: http://127.0.0.1:8000/api/health
Tests: `pytest`

The source document mentions both Flask and FastAPI; the later milestones explicitly specify FastAPI, Uvicorn, Jinja2 and FastAPI routes, so this implementation standardizes on FastAPI.
The named Amazon/Flipkart/IKEA/Swiggy/Zomato/OYO integrations are represented as search links rather than fake live prices or scraping.
