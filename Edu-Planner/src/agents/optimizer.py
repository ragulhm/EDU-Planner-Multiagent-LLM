from utils.prompts import get_optimizer_prompt
from llm import call_llm
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
import time

class OptimizerAgent:
    def __init__(self):
        # Simple in-memory cache with timestamp
        self._cache: Dict[str, Dict[str, Any]] = {}
        # Conservative temperature for stability
        self._temperature = 0.7
        # Load prior successful improvements if available
        self._load_improvements()

    def _load_improvements(self) -> None:
        """Load cached successful improvements from disk."""
        try:
            cache_file = Path(__file__).resolve().parents[2] / 'cache' / 'improvements.json'
            if cache_file.exists():
                data = json.loads(cache_file.read_text(encoding='utf-8'))
                if isinstance(data, dict):
                    self._cache = data
        except Exception:
            pass

    def _save_improvements(self) -> None:
        """Save successful improvements to disk."""
        try:
            cache_file = Path(__file__).resolve().parents[2] / 'cache' / 'improvements.json'
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            # Only save recent entries (last 24h)
            now = time.time()
            fresh = {
                k: v for k, v in self._cache.items()
                if v.get('timestamp', 0) + 86400 > now
            }
            cache_file.write_text(json.dumps(fresh, indent=2), encoding='utf-8')
        except Exception:
            pass

    def _parse_response(self, response: str) -> Optional[dict]:
        """Safely extract JSON from LLM response."""
        if not response:
            return None
        
        try:
            # First try: whole response as JSON
            return json.loads(response)
        except json.JSONDecodeError:
            try:
                # Second try: find JSON object markers
                start = response.find('{')
                end = response.rfind('}')
                if start != -1 and end != -1 and end > start:
                    return json.loads(response[start:end+1])
            except json.JSONDecodeError:
                pass
        return None

    def optimize(self, lesson_plan: str, feedback: str, skill_tree) -> dict:
        """Optimize lesson plan with caching for stability.
        
        Returns a dict with:
        - plan: improved lesson plan text
        - improvements: list of specific changes
        - exercise: practice exercise dict
        """
        skill_summary = skill_tree.get_summary()

        # Check cache first
        cache_key = f"{lesson_plan[:100]}:{feedback[:100]}"
        cached = self._cache.get(cache_key)
        if cached:
            # Use cached result if less than 1 hour old
            if cached.get('timestamp', 0) + 3600 > time.time():
                return cached['result']

        # Get improvements from LLM
        prompt = get_optimizer_prompt(
            lesson_plan=lesson_plan,
            skill_summary=skill_summary,
            feedback=feedback
        )
        
        response = call_llm(prompt, temp=self._temperature)
        result = self._parse_response(response)
        
        if result and isinstance(result, dict):
            # Cache successful result
            self._cache[cache_key] = {
                'result': result,
                'timestamp': time.time()
            }
            self._save_improvements()
            return result

        # Safe fallback
        return {
            "plan": lesson_plan,
            "improvements": [],
            "exercise": {}
        }