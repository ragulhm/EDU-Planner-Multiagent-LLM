from utils.prompts import get_analyst_prompt
from llm import call_llm
import json
from typing import List

class AnalystAgent:
    def analyze_errors(self, example: str, skill_tree, focus_areas: List[str] | None = None) -> dict:
        """Faster, focused analyst that prioritizes small context and focus areas.

        Returns: {"misconceptions": [...], "raw": str}
        """
        skill_summary = skill_tree.get_summary() if skill_tree is not None else ""
        # Truncate very long inputs to keep LLM work small
        excerpt = example
        if isinstance(example, str) and len(example) > 1200:
            excerpt = example[:1200] + "\n..."

        prompt = get_analyst_prompt(example=excerpt, skill_summary=skill_summary, focus_areas=focus_areas, max_items=6)
        response = call_llm(prompt, temp=0.3)

        # Try direct JSON parse, then fallback to object extraction
        try:
            parsed = json.loads(response)
            if isinstance(parsed, dict) and 'misconceptions' in parsed:
                parsed['raw'] = response
                return parsed
        except Exception:
            pass

        try:
            start = response.find('{')
            end = response.rfind('}')
            if start != -1 and end != -1 and end > start:
                parsed = json.loads(response[start:end+1])
                if isinstance(parsed, dict) and 'misconceptions' in parsed:
                    parsed['raw'] = response
                    return parsed
        except Exception:
            pass

        # Last-resort: return the whole response as a single-item misconception
        return {"misconceptions": [response], "raw": response}
