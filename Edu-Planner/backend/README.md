Edu-Planner backend
===================

This is a small FastAPI backend that exposes endpoints used by a web frontend. It interacts with the existing code in `src/` (agents, utils, llm).

How to run (development)

1. Install dependencies (preferably in a virtualenv):

```powershell
pip install -r requirements.txt
```

2. Set your OpenRouter API key (if using cloud LLM):

```powershell
$env:OPENROUTER_API_KEY = "sk-or-..."
```

3. Run the backend (from repo root):

```powershell
$env:PYTHONPATH = "${PWD}\src"
python .\backend\app.py
```

- The backend listens on port 8000 by default. Endpoints:
- GET /api/questions?level=1&n=10  (level can be 1,2,3 or the names 'easy','intermediate','hard')
- POST /api/evaluate  { user_id, plan, sample_questions }
- POST /api/optimize  { user_id, plan, feedback, scores }
- GET  /api/user/{user_id}/history
- GET  /api/user/{user_id}/best
- POST /api/user/{user_id}/generate_questions { user_id, level, n }

Note: The backend accepts level as number or name: pass 1 (easy), 2 (intermediate), 3 (hard), or the strings 'easy','intermediate','hard'. The server maps numeric values to the corresponding dataset and will return 400 for invalid values.
