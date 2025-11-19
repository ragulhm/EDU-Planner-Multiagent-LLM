from core.skill_tree import OSSkillTree
from agents.evaluator import EvaluatorAgent
from agents.optimizer import OptimizerAgent
from agents.analyst_v2 import AnalystAgent
from core.ciddp import compute_ciddp_score
# try to import a python module that provides `lessonplan` (optional)
try:
    from data.lessonplan import lessonplan as lessonplan_text
except Exception:
    lessonplan_text = None
from pathlib import Path
import json
import random
import time
from utils.io import (
    save_user_iteration,
    update_user_best_plan_if_higher,
    get_user_best_plan,
    save_generated_questions,
    append_questions_to_level,
)
from llm import call_llm
from utils.prompts import get_question_generation_prompt
import uuid

def main():

    # Step 1: Choose level
    print("Choose your level:")
    print("1. Easy\n2. Intermediate\n3. Hard")
    level_map = {"1": "easy", "2": "intermediate", "3": "hard"}
    level_choice = input("Enter 1, 2, or 3: ").strip()
    level = level_map.get(level_choice, "easy")

    # Step 2: Load questions (resolve path relative to project root)
    repo_root = Path(__file__).resolve().parents[1]
    questions_file = repo_root / 'data' / f"os_questions_{level}.json"
    with open(questions_file, "r", encoding="utf-8") as f:
        questions = json.load(f)

    # Step 3: Select 10 random (unordered) MCQs and collect answers
    # Normalize loaded JSON to a list of question dicts if needed
    questions_list = []
    if isinstance(questions, list):
        questions_list = questions
    elif isinstance(questions, dict):
        for key in ("questions", "items", "data"):
            if key in questions and isinstance(questions[key], list):
                questions_list = questions[key]
                break
        else:
            lists = [v for v in questions.values() if isinstance(v, list)]
            questions_list = lists[0] if lists else []

    if not questions_list:
        print("No questions found in the selected file.")
        return

    # Sample 10 random questions (or shuffle all if fewer than 10)
    if len(questions_list) <= 10:
        sampled_questions = questions_list.copy()
        random.shuffle(sampled_questions)
    else:
        sampled_questions = random.sample(questions_list, 10)

    print(f"\nAnswer the following {len(sampled_questions)} {level.capitalize()} OS questions:")
    user_answers = []
    for idx, q in enumerate(sampled_questions, 1):
        print(f"\nQ{idx}: {q['question']}")
        # Shuffle the options for display, but track the correct answer
        options = q.get('options', []).copy()
        random.shuffle(options)
        for opt_idx, opt in enumerate(options, 1):
            print(f"  {opt_idx}. {opt}")
        ans = input(f"Your answer (1-{len(options)}): ").strip()
        user_answer = options[int(ans)-1] if ans.isdigit() and 1 <= int(ans) <= len(options) else ""
        user_answers.append({
            "question": q.get('question'),
            "correct": q.get('answer'),
            "options": options,
            "user_choice": ans,
            "user_answer": user_answer
        })

    # Step 4: Evaluate answers
    correct_count = sum(ua['user_answer'] == ua['correct'] for ua in user_answers)
    print(f"\nYou answered {correct_count} out of 10 questions correctly.")

    # Step 5: Prepare for further evaluation (lesson plan, skill tree, sample questions)
    skill_tree = OSSkillTree()
    skill_tree.set_level("Processes_and_Threads", 2)
    skill_tree.set_level("Memory_Management", 3)

    # Get user ID first
    user_id = input("Enter your user id [default=user1]: ").strip() or "user1"
    
    # Check if this user has a saved plan from previous iteration
    user_best_path = repo_root / 'data' / 'user_best' / f"{user_id}.json"
    
    if user_best_path.exists():
        # User has previous iteration - load their specific plan
        try:
            with open(user_best_path, 'r', encoding='utf-8') as f:
                user_data = json.loads(f.read())
                if user_data and isinstance(user_data, dict) and user_data.get('plan'):
                    initial_plan = user_data['plan']
                    print(f"Loading your previous lesson plan for user {user_id}")
                else:
                    raise ValueError("Invalid user plan data")
        except Exception as e:
            print(f"Error loading user plan: {e}")
            initial_plan = None
    else:
        # First iteration - use default initial plan
        print(f"First iteration for user {user_id} - using initial lesson plan")
        initial_plan = None

    # If no user plan loaded, use default initialization priority:
    # 1) lessonplan_text from module
    # 2) lessonplan.txt file
    # 3) built-in default
    if initial_plan is None:
        if lessonplan_text:
            initial_plan = lessonplan_text
            print("Using lesson plan from data.lessonplan module")
        else:
            lp_path = repo_root / 'data' / 'lessonplan.txt'
            if lp_path.exists():
                try:
                    initial_plan = lp_path.read_text(encoding='utf-8')
                    print("Loaded lesson plan from lessonplan.txt")
                except Exception:
                    initial_plan = ""
            else:
                initial_plan = """
    Operating Systems Lesson Plan:
    1. Introduction to Operating Systems
    2. Processes and Threads
    3. Memory Management
    4. File Systems
    5. Device Management
    6. Scheduling and Multitasking
    7. Deadlocks and Synchronization
    8. Security and Protection
    9. Virtual Memory
    10. OS Architectures (Monolithic, Microkernel)
    """

    evaluator = EvaluatorAgent()
    optimizer = OptimizerAgent()
    analyst = AnalystAgent()

    best_plan = initial_plan
    best_score = 0
    score_queue = []
    best_plan_snapshot = initial_plan
    collected_pitfalls = []
    seen_pitfalls = set()

    for iteration in range(3):
        print(f"\n--- Evaluator Agent (Iteration {iteration+1}) ---")
        avg_score = 0.0
        try:
            scores, feedback = evaluator.evaluate(best_plan, skill_tree, sample_questions=user_answers)
        except ConnectionError as e:
            print(f"[Iter {iteration+1}] Ollama connection error: {e}")
            print("Skipping evaluation for this iteration.")
            score_queue.append({"score": 0.0, "scores": {}, "plan": best_plan})
            continue

        # Get or estimate scores
        if not scores or not isinstance(scores, dict):
            print("Estimating scores from quiz performance...")
            total_q = len(user_answers) if user_answers else 10
            correct = sum(ua['user_answer'] == ua['correct'] for ua in user_answers)
            pct = correct / total_q if total_q else 0.0
            # Map to 1-5 scale
            est_val = max(1, min(5, int(round(pct * 4)) + 1))
            scores = {
                'Clarity': est_val,
                'Integrity': est_val,
                'Depth': est_val,
                'Practicality': est_val,
                'Pertinence': est_val
            }
            feedback = f"Quiz performance: {correct}/{total_q} correct"

        # Compute CIDDP score
        avg_score = compute_ciddp_score(scores)
        print(f" CIDDP Score: {avg_score:.2f}")

        # User ID is already obtained at the start

        # Save plan snapshot (persist per-user history) and keep runtime queue
        plan_entry = {
            "plan": best_plan,
            "score": avg_score,
            "scores": scores,
            "iteration": iteration + 1
        }
        save_user_iteration(user_id, plan_entry)
        # also update the user's best plan file if this iteration improved the score
        try:
            update_user_best_plan_if_higher(user_id, plan_entry)
        except Exception:
            pass
        # keep an in-memory session list for quick runtime reporting
        score_queue.append(plan_entry)

        # Optimize plan (cached if recently done)
        print("\n--- Optimizer Agent ---")
        
        # Get current user's best plan path
        user_best_path = repo_root / 'data' / 'user_best' / f"{user_id}.json"
        
        # Get the current score for comparison if user has previous iteration
        current_best_score = 0
        focus_next = None
        if user_best_path.exists():
            try:
                with open(user_best_path, 'r', encoding='utf-8') as f:
                    user_data = json.loads(f.read())
                    if isinstance(user_data, dict):
                        current_best_score = user_data.get('score', 0)
                        # Get focus areas from last optimization if available
                        last_opt = user_data.get('last_optimization', {})
                        if isinstance(last_opt, dict):
                            focus_next = last_opt.get('focus_next')
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not read previous optimization data: {e}")

        opt_result = optimizer.optimize(best_plan, feedback, skill_tree)
        
        if isinstance(opt_result, dict) and opt_result.get('plan'):
            best_plan = opt_result['plan']
            if opt_result.get('improvements'):
                print("\nImprovements made:")
                for imp in opt_result['improvements']:
                    print(f"- {imp.get('text', '')}")
                print(f"\nCurrent iteration score: {avg_score:.2f}")
                print(f"Previous best score: {current_best_score:.2f}")
        
        # Store last optimization result for next iteration
        plan_entry['last_optimization'] = opt_result
        
        # Short delay to avoid overwhelming the LLM
        time.sleep(1)

        # Analyst step: get misconceptions as JSON (focused)
        print("\n--- Analyst Agent ---")
        # Determine focus areas from optimizer output if available
        focus_areas = None
        if isinstance(opt_result, dict):
            focus_areas = opt_result.get('focus_next') or [imp.get('area') for imp in opt_result.get('improvements', []) if imp.get('area')][:3]
            # normalize focus_areas to list of strings
            if isinstance(focus_areas, (list, tuple)):
                focus_areas = [str(f).strip() for f in focus_areas if f]
            else:
                focus_areas = None

        analyst_result = analyst.analyze_errors(best_plan, skill_tree, focus_areas=focus_areas)
        misconceptions = analyst_result.get('misconceptions') if isinstance(analyst_result, dict) else [analyst_result]
        print("Common Pitfalls Suggested:")
        print(misconceptions)
        if misconceptions and json.dumps(misconceptions) not in seen_pitfalls:
            collected_pitfalls.append(misconceptions)
            seen_pitfalls.add(json.dumps(misconceptions))

    # Show max CIDPP score and corresponding lesson plan
    max_score_entry = max(score_queue, key=lambda x: x["score"], default=None)
    if max_score_entry:
        print(f"\n Max CIDPP Score: {max_score_entry['score']:.2f}")
        print("\n======================================")
        print(" Your Personalized OS Lesson Plan ")
        print("========================================\n")
        # Split and format the lesson plan for clarity
        plan_lines = [line.strip() for line in max_score_entry["plan"].split('\n') if line.strip()]
        for line in plan_lines:
            # Skip previously appended common pitfalls in the plan body
            if line.startswith("Common Pitfalls:"):
                continue
            if line and line[0].isdigit() and line[1] == '.':
                print(f"  {line}")
            else:
                print(line)
        # Finally print collected pitfalls once
        if collected_pitfalls:
            print("\n\n Common Pitfalls and Misconceptions to Address:\n")
            for notes in collected_pitfalls:
                print(notes)
        print("\n=====================================")
        print("Ready to start your OS study journey! 🚀")
        print("=======================================\n")
    else:
        print("No valid scores computed.")

    # Also show the top plan from the persisted per-user queue (if any)
    try:
        top_plan = get_user_best_plan(user_id)
        if top_plan:
            print("\nTop plan from your saved queue (per-user):")
            print(json.dumps(top_plan, indent=2, ensure_ascii=False))
    except Exception:
        # non-fatal
        pass

    # Offer to generate DB-formatted questions from the selected optimized plan
    try:
        gen_choice = input("Generate DB-formatted questions from the optimized plan? (y/N): ").strip().lower()
        if gen_choice == 'y':
            # default to the runtime-chosen level unless user overrides
            gen_level = input(f"Which level to generate for? (easy/intermediate/hard) [default={level}]: ").strip().lower() or level
            try:
                n_q = int(input("How many questions to generate? [default=10]: ").strip() or "10")
            except Exception:
                n_q = 10

            plan_text = None
            if max_score_entry and max_score_entry.get('plan'):
                plan_text = max_score_entry['plan']
            elif top_plan and isinstance(top_plan, dict):
                plan_text = top_plan.get('plan') or top_plan.get('raw') or best_plan
            else:
                plan_text = best_plan

            prompt = get_question_generation_prompt(plan_text, gen_level, n_q)
            print("Requesting LLM to generate questions... (this may take a moment)")
            resp = call_llm(prompt)

            # crude JSON array extraction
            try:
                start = resp.find('[')
                end = resp.rfind(']')
                if start == -1 or end == -1:
                    raise ValueError("No JSON array found in LLM response")
                arr_text = resp[start:end+1]
                generated = json.loads(arr_text)
                # validate items
                valid = []
                for i, it in enumerate(generated):
                    if not isinstance(it, dict):
                        continue
                    # ensure required keys
                    for k in ("id", "topic", "level", "question", "options", "answer", "explanation"):
                        if k not in it:
                            it[k] = None
                    # normalize id if missing
                    if not it.get('id'):
                        it['id'] = f"gen-{gen_level}-{uuid.uuid4().hex[:8]}"
                    # ensure level matches requested
                    it['level'] = gen_level
                    # ensure options is a list
                    if not isinstance(it.get('options'), list):
                        it['options'] = [str(it.get('answer'))] if it.get('answer') else []
                    valid.append(it)

                if not valid:
                    print("LLM returned no valid question objects.")
                else:
                    filename = f"generated_questions_{gen_level}_{user_id}.json"
                    save_generated_questions(filename, valid)

                    # Append generated questions to the canonical level dataset (os_questions_<level>.json)
                    try:
                        appended = append_questions_to_level(gen_level, valid)
                    except Exception as e:
                        appended = 0
                        print(f"Warning: failed to append to level dataset: {e}")

                    print(f"Saved {len(valid)} questions to data/{filename}. Appended {appended} to os_questions_{gen_level}.json.")

                    # Offer the user to attempt the generated questions now
                    try:
                        attempt_now = input("Attempt generated questions now? (y/N): ").strip().lower()
                    except Exception:
                        attempt_now = 'n'

                    user_answers = []
                    if attempt_now == 'y':
                        for q in valid:
                            options = q.get('options', []) or []
                            # Ensure options is a list and contains the answer if possible
                            if not isinstance(options, list):
                                options = [str(options)]
                            if not options and q.get('answer'):
                                options = [q.get('answer')]
                            random.shuffle(options)
                            print("\nQuestion:", q.get('question'))
                            for opt_idx, opt in enumerate(options, 1):
                                print(f"  {opt_idx}. {opt}")
                            ans = input(f"Your answer (1-{len(options)}): ").strip()
                            user_answer = ""
                            if ans.isdigit() and 1 <= int(ans) <= len(options):
                                user_answer = options[int(ans) - 1]
                            user_answers.append({
                                "question": q.get('question'),
                                "correct": q.get('answer'),
                                "options": options,
                                "user_choice": ans,
                                "user_answer": user_answer,
                            })

                    # Evaluate generated questions to get feedback and scores
                    try:
                        if user_answers:
                            correct = sum(ua['user_answer'] == ua['correct'] for ua in user_answers)
                            total_q = len(user_answers)
                            pct = correct / total_q if total_q else 0.0
                            est_val = max(1, min(5, int(round(pct * 4)) + 1))
                            scores = {"Clarity": est_val, "Integrity": est_val, "Depth": est_val, "Practicality": est_val, "Pertinence": est_val}
                            feedback_text = f"Quiz performance: {correct}/{total_q} correct"
                        else:
                            # Use evaluator agent to evaluate the plan with sample questions
                            try:
                                scores, feedback_text = evaluator.evaluate(plan_text, skill_tree, sample_questions=valid)
                            except Exception as ee:
                                scores = {"Clarity": 0, "Integrity": 0, "Depth": 0, "Practicality": 0, "Pertinence": 0}
                                feedback_text = f"Evaluator failed: {ee}"

                        avg_score_questions = compute_ciddp_score(scores) if scores else 0.0
                        print(f"\nQuestions evaluation CIDDP score: {avg_score_questions:.2f}")
                        print("Evaluator feedback:\n", feedback_text)
                    except Exception as e:
                        print(f"Failed to evaluate generated questions: {e}")
                        scores = {"Clarity": 0, "Integrity": 0, "Depth": 0, "Practicality": 0, "Pertinence": 0}
                        feedback_text = ""

                    # Use optimizer to produce a personalized lesson plan from the feedback
                    try:
                        print("\nGenerating personalized lesson plan from generated-question feedback...")
                        opt2 = optimizer.optimize(plan_text, feedback_text or "", skill_tree)
                        if isinstance(opt2, dict) and opt2.get('plan'):
                            personal_plan = opt2['plan']
                            print("Personalized lesson plan generated.")
                            # Persist this as an iteration for the user
                            entry = {
                                "plan": personal_plan,
                                "score": avg_score_questions,
                                "scores": scores,
                                "iteration": (max_score_entry.get('iteration', 0) + 1) if max_score_entry else 1
                            }
                            try:
                                save_user_iteration(user_id, entry)
                                update_user_best_plan_if_higher(user_id, entry)
                            except Exception as e:
                                print(f"Warning: failed to save personalized plan: {e}")
                        else:
                            print("Optimizer did not return a personalized plan.")
                    except Exception as e:
                        print(f"Failed to generate personalized plan: {e}")
            except Exception as e:
                print(f"Failed to parse generated questions: {e}\nRaw response:\n{resp}")
    except Exception:
        pass

if __name__ == "__main__":
    main()