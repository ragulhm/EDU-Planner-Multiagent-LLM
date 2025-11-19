from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
from pathlib import Path
import os
import json

# Ensure src is importable when running backend directly
repo_root = Path(__file__).resolve().parents[1]
src_path = str(repo_root / 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from agents.evaluator import EvaluatorAgent
from agents.optimizer import OptimizerAgent
from agents.analyst_v2 import AnalystAgent
from utils.io import load_questions, save_generated_questions, save_user_iteration, get_user_best_plan
from utils.prompts import get_question_generation_prompt
from llm import call_llm

app = FastAPI(title="Edu-Planner Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    level: Optional[str] = "easy"
    n: Optional[int] = 10


class EvaluateRequest(BaseModel):
    user_id: str
    plan: str
    sample_questions: Optional[List[dict]] = None


class OptimizeRequest(BaseModel):
    user_id: str
    plan: str
    feedback: Optional[str] = ""
    scores: Optional[dict] = None


class GenerateRequest(BaseModel):
    user_id: str
    level: str = "easy"
    n: int = 10


evaluator = EvaluatorAgent()
optimizer = OptimizerAgent()
analyst = AnalystAgent()


@app.get("/api/questions")
def get_questions(level: str = "easy", n: int = 10):
    """Return up to `n` questions for the requested level.

    The frontend may pass level as one of: 1,2,3 or the strings 'easy','intermediate','hard'.
    We normalize numeric values 1->easy, 2->intermediate, 3->hard.
    """
    # normalize level
    lvl = None
    try:
        if isinstance(level, int) or (isinstance(level, str) and level.isdigit()):
            li = int(level)
            if li == 1:
                lvl = 'easy'
            elif li == 2:
                lvl = 'intermediate'
            elif li == 3:
                lvl = 'hard'
            else:
                raise HTTPException(status_code=400, detail="Level must be 1,2,3 or 'easy','intermediate','hard'")
        else:
            if str(level).lower() in ('easy', 'intermediate', 'hard'):
                lvl = str(level).lower()
            else:
                raise HTTPException(status_code=400, detail="Level must be 1,2,3 or 'easy','intermediate','hard'")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid level parameter")

    try:
        repo_root = Path(__file__).resolve().parents[1]
        qfile = repo_root / 'data' / f"os_questions_{lvl}.json"
        questions = load_questions(qfile, n=n)
        return {"questions": questions}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Questions file not found for level {lvl}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/evaluate")
def evaluate(req: EvaluateRequest):
    try:
        scores, feedback = evaluator.evaluate(req.plan, None, sample_questions=req.sample_questions)
        # persist iteration as a placeholder (score summary)
        entry = {"plan": req.plan, "score": sum(scores.values())/len(scores) if scores else 0, "scores": scores}
        save_user_iteration(req.user_id, entry)
        return {"scores": scores, "feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/optimize")
def optimize(req: OptimizeRequest):
    try:
        opt = optimizer.optimize(req.plan, req.feedback or "", None)
        # persist candidate iteration
        entry = {"plan": opt.get('plan', req.plan), "score": opt.get('score', 0), "scores": req.scores or {}}
        save_user_iteration(req.user_id, entry)
        return opt
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/user/{user_id}/history")
def user_history(user_id: str):
    try:
        from utils.io import load_user_history
        return {"history": load_user_history(user_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/user/{user_id}/best")
def user_best(user_id: str):
    try:
        best = get_user_best_plan(user_id)
        return {"best": best}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/user/{user_id}/generate_questions")
def generate_questions(user_id: str, req: GenerateRequest):
    try:
        # normalize and validate level param (support numeric 1/2/3 or strings)
        if isinstance(req.level, int) or (isinstance(req.level, str) and req.level.isdigit()):
            li = int(req.level)
            if li == 1:
                lvl = 'easy'
            elif li == 2:
                lvl = 'intermediate'
            elif li == 3:
                lvl = 'hard'
            else:
                raise HTTPException(status_code=400, detail="Level must be 1,2,3 or 'easy','intermediate','hard'")
        else:
            if str(req.level).lower() in ('easy', 'intermediate', 'hard'):
                lvl = str(req.level).lower()
            else:
                raise HTTPException(status_code=400, detail="Level must be 1,2,3 or 'easy','intermediate','hard'")

        # determine plan context (use best plan if exists)
        best = get_user_best_plan(user_id)
        plan_text = best.get('plan') if best else ""
        if not plan_text:
            plan_text = req.user_id  # minimal fallback

        prompt = get_question_generation_prompt(plan_text, lvl, req.n)
        resp = call_llm(prompt)
        # extract JSON array
        start = resp.find('[')
        end = resp.rfind(']')
        if start == -1 or end == -1:
            raise ValueError("No JSON array in LLM response")
        arr_text = resp[start:end+1]
        questions = json.loads(arr_text)
        filename = f"generated_questions_{req.level}_{user_id}.json"
        save_generated_questions(filename, questions)
        return {"filename": filename, "count": len(questions)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
