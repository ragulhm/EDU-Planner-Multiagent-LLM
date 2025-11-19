"""
OS evaluation prompt templates (clean, error-free)
Provides three helper functions that return ready-to-use prompt strings for
an evaluator, an optimizer, and an analyst agent. Each function accepts the
lesson_plan and skill_summary and returns a formatted prompt that asks the
agent to evaluate using CIDDP criteria: Clarity, Integrity, Depth,
Practicality, Pertinence.
"""
from typing import Literal


def _format_scores_instructions() -> str:
    """Common output format instructions used by all prompts."""
    return (
        "Output ONLY using these five short bracketed labels and a one-line comment for each:\n"
        "[C]:<score 1-5>; short comment  — Clarity\n"
        "[I]:<score 1-5>; short comment  — Integrity\n"
        "[D]:<score 1-5>; short comment  — Depth\n"
        "[P]:<score 1-5>; short comment  — Practicality\n"
        "[P]:<score 1-5>; short comment  — Pertinence\n"
        "Example output:\n"
        "[C]:3; Clear but too brief\n"
        "[I]:4; Good structure\n"
        "[D]:2; Lacks virtual memory details\n"
        "[P]:5; Uses real shell examples\n"
        "[P]:4; Matches beginner level"
    )


def get_evaluator_prompt(lesson_plan: str, skill_summary: str, sample_questions=None) -> str:
    """Return a clean evaluator prompt for assessing an OS lesson plan, skill tree, and sample questions.

    Args:
        lesson_plan: The full lesson plan text to evaluate.
        skill_summary: A one- to three-sentence summary of the student's current skill level and prior knowledge.
        sample_questions: List of sample questions (dicts) to include in the evaluation.

    Returns:
        A formatted prompt string ready to feed to an evaluator LLM agent.
    """
    instructions = _format_scores_instructions()
    questions_section = ""
    if sample_questions:
        questions_section = "Sample Questions for Evaluation:\n"
        for q in sample_questions:
            questions_section += f"Q: {q.get('question')}\nOptions: {', '.join(q.get('options', []))}\nCorrect: {q.get('answer')}\n\n"

    return (
        f"You are an expert Operating Systems instructor. Evaluate the following lesson plan using the CIDDP criteria (Clarity, Integrity, Depth, Practicality, Pertinence).\n\n"
        f"Student Skill Profile: {skill_summary}\n\n"
        f"Lesson Plan:\n{lesson_plan}\n\n"
        f"{questions_section}"
        f"Evaluate on the five CIDDP areas (Clarity, Integrity, Depth, Practicality, Pertinence).\n"
        f"Return a single JSON object (no extra text) with this schema:\n"
        f"{{\n  \"scores\": {{\"Clarity\": int(1-5), \"Integrity\": int, \"Depth\": int, \"Practicality\": int, \"Pertinence\": int}},\n  \"comments\": {{\"Clarity\": str, ...}},\n  \"summary\": str  // short human summary\n}}\n"
        f"If you cannot provide values, set them to null, but always return valid JSON.\n"
        f"Do NOT output any other text besides the JSON object."
    )


def get_optimizer_prompt(lesson_plan: str, skill_summary: str, feedback: str = "",
                      focus_areas: list[str] = None,
                      history: list[dict] = None) -> str:
    """Return a prompt guiding an optimizer agent to suggest concrete improvements.
    
    Args:
        lesson_plan: Current lesson plan text
        skill_summary: Student skill profile summary
        feedback: Latest feedback to address (optional)
        focus_areas: List of specific topics/areas to focus on (e.g., from low scores)
        history: Previous improvement attempts and their outcomes
    """
    focus_section = ""
    if focus_areas:
        focus_section = "Focus Areas (prioritize these):\n- " + "\n- ".join(focus_areas) + "\n\n"

    history_section = ""
    if history:
        history_section = "Previous Improvements:\n"
        for h in history:
            outcome = h.get("outcome", "unknown")
            history_section += f"- {h.get('text', '')} -> {outcome}\n"
        history_section += "\n"

    feedback_section = ""
    if feedback and feedback.strip():
        feedback_section = f"Recent Feedback:\n{feedback}\n\n"

    # Build a more targeted prompt that encourages incremental, focused updates
    return (
        f"You are an expert curriculum optimizer for Operating Systems courses. Update the lesson plan considering:\n"
        f"1. The student's current level and needs\n"
        f"2. Any specific focus areas that need improvement\n"
        f"3. What worked/didn't work in previous iterations\n\n"
        f"Student Profile: {skill_summary}\n\n"
        f"{focus_section}"
        f"{history_section}"
        f"{feedback_section}"
        f"Current Plan:\n{lesson_plan}\n\n"
        f"Return a single JSON object with this schema:\n"
        "{\n"
        '  "plan": "updated lesson plan text",\n'
        '  "improvements": [\n'
        '    {"text": "what changed", "area": "topic area", "priority": 1-5}\n'
        "  ],\n"
        '  "focus_next": ["topic1", "topic2"],  // areas to focus on next\n'
        '  "exercise": {"title": "string", "steps": ["step1", ...]}\n'
        "}\n\n"
        f"Rules:\n"
        f"1. Only suggest substantive changes that clearly improve the plan\n"
        f"2. Focus on the specified areas if provided\n"
        f"3. Build on what worked in history, avoid repeating failed approaches\n"
        f"4. Keep changes minimal but impactful\n"
        f"5. Output ONLY the JSON object\n"
    )


def get_analyst_prompt(example: str, skill_summary: str, focus_areas: list[str] | None = None, max_items: int = 5) -> str:
    """Prompt to extract common misconceptions from a given OS example or explanation and return JSON.

    If `focus_areas` is provided, the analyst should prioritize those topics and return concise items.
    """
    focus_section = ""
    if focus_areas:
        focus_section = "Focus areas (prioritize these):\n- " + "\n- ".join(focus_areas) + "\n\n"

    return (
        f"You are an instructional analyst for Operating Systems. Given the following short context or example, identify the top likely misconceptions students may have. Be concise and return at most {max_items} items.\n\n"
        f"Student Skill Profile: {skill_summary}\n\n"
        f"{focus_section}"
        f"Context:\n{example}\n\n"
        f"Return a JSON object exactly in this form (no extra text): {{\"misconceptions\": [\"...\", ...]}}."
    )


def get_question_generation_prompt(lesson_plan: str, level: Literal["easy", "intermediate", "hard"], n: int = 10) -> str:
    """Return a prompt that asks the LLM to generate `n` DB-formatted multiple-choice questions.

    Each question must be a JSON object with the following fields:
      - id: unique string id (e.g., q1, q2, or uuid)
      - topic: short topic string (derived from the lesson plan)
      - level: one of 'easy', 'intermediate', 'hard'
      - question: the question text
      - options: an array of 3-5 answer option strings
      - answer: the exact option string that is correct
      - explanation: a brief explanation of the correct answer

    The LLM MUST return only a JSON array (no surrounding prose) containing `n` such objects.
    If it cannot produce exactly `n`, it should produce as many as it can, but still return a JSON array.
    """

    return (
        "You are an expert Operating Systems question-writer.\n\n"
        f"Generate {n} multiple-choice questions suitable for the following lesson plan and student level.\n\n"
        f"Lesson Plan:\n{lesson_plan}\n\n"
        f"Target Level: {level}\n\n"
        "Output format requirements:\n"
        "- Return ONLY a single JSON array (no extra text).\n"
        "- Each item in the array must be an object with exactly these fields: id, topic, level, question, options, answer, explanation.\n"
        "- `options` should contain 3 to 5 distinct strings.\n"
        "- `answer` must exactly equal one of the strings in `options`.\n"
        "- Keep the language concise and clear, suitable for learners.\n\n"
        "Example of one item (for clarity, do not include trailing comments in actual output):\n"
        "{"
        "\"id\": \"q1\", \"topic\": \"Processes\", \"level\": \"easy\", \"question\": \"What is a process?\", \"options\": [\"A program in execution\", \"An instruction\", \"A file\"], \"answer\": \"A program in execution\", \"explanation\": \"A process is an instance of a program in execution.\"}"
        "\n\n"
        "Return ONLY the JSON array."
    )

# if _name_ == "_main_":
#     # quick sanity check example
#     example_lesson = "Intro to processes, context switching, simple round-robin scheduling."
#     example_skill = "Beginner: understands basic programming and threads, not OS internals."
#     print(get_evaluator_prompt(example_lesson, example_skill))