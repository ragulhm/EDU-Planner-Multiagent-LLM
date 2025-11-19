from llm import call_llm
from utils.prompts import get_evaluator_prompt
from utils.io import load_questions
import json


class EvaluatorAgent:
    def evaluate(self, lesson_plan: str, skill_tree, sample_questions=None) -> tuple[dict, str]:
        """Call the LLM evaluator and parse CIDDP-style bracketed scores.

        The evaluator expects lines like:
          [C]:3; comment
          [I]:4; comment
          [D]:2; comment
          [P]:5; comment
          [P]:4; comment  # second P maps to Pertinence

        This method normalizes tags and returns a dict of scores plus the raw response.
        """
        skill_summary = skill_tree.get_summary()

        # If caller didn't provide sample_questions, load 10 random ones from
        # the repository data file. This keeps the evaluator self-contained
        # and ensures the prompt includes representative questions.
        if sample_questions is None:
            try:
                sample_questions = load_questions(n=10)
            except FileNotFoundError:
                # fallback to empty list if file not found
                sample_questions = []

        prompt = get_evaluator_prompt(lesson_plan, skill_summary, sample_questions=sample_questions)
        response = call_llm(prompt, temp=0.0)

        # Try to extract JSON object from the LLM response first
        try:
            # crude bounding of JSON object
            start = response.find('{')
            end = response.rfind('}')
            if start != -1 and end != -1 and end > start:
                json_text = response[start:end+1]
                parsed = json.loads(json_text)
                if isinstance(parsed, dict) and 'scores' in parsed:
                    return parsed.get('scores', {}), response
        except Exception:
            # fall back to legacy parsing
            pass

        # Legacy bracketed-line parsing fallback
        scores = {}
        p_count = 0

        for line in response.split('\n'):
            line = line.strip()
            if not line:
                continue

            try:
                if not line.startswith('[') or ']' not in line:
                    continue

                start = line.find('[')
                end = line.find(']')
                if start == -1 or end == -1 or end <= start:
                    continue

                tag = line[start + 1:end].strip()
                rest = line[end + 1:].strip()

                if not rest.startswith(':'):
                    continue

                # Extract score: everything after ':' until ';' or end
                score_str = rest[1:].split(';')[0].strip()
                score = int(score_str)

                # Normalize tags: C, I, D map to names. Handle multiple P tags and Pt.
                key_map = {'C': 'Clarity', 'I': 'Integrity', 'D': 'Depth'}
                if tag in key_map:
                    key = key_map[tag]
                else:
                    t_lower = tag.lower()
                    if t_lower in ('pt', 'pertinence'):
                        key = 'Pertinence'
                    elif tag == 'P':
                        p_count += 1
                        if p_count == 1:
                            key = 'Practicality'
                        elif p_count == 2:
                            key = 'Pertinence'
                        else:
                            key = f'P_{p_count}'
                    else:
                        # unknown tag: keep as-is
                        key = tag

                scores[key] = score

            except (ValueError, IndexError, AttributeError):
                # ignore unparsable lines
                continue

        return scores, response