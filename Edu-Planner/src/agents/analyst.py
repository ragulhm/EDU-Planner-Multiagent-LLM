from utils.prompts import get_analyst_prompt
from llm import call_llm
import json

class AnalystAgent:
    def analyze_errors(self, example: str, skill_tree) -> dict:
        """Return parsed JSON from analyst LLM: {"misconceptions": [...]}
        Falls back to returning {"misconceptions": [raw_text]}
        """
        skill_summary = skill_tree.get_summary()
        prompt = get_analyst_prompt(example=example, skill_summary=skill_summary)
        response = call_llm(prompt, temp=0.7)
        try:
            start = response.find('{')
            end = response.rfind('}')
            if start != -1 and end != -1 and end > start:
                parsed = json.loads(response[start:end+1])
                if isinstance(parsed, dict):
                    parsed['raw'] = response
                    return parsed
        except Exception:
            pass
        return {"misconceptions": [response], "raw": response}