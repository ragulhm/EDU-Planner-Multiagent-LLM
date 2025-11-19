from __future__ import annotations

import json
import random
from pathlib import Path
from typing import List, Dict, Any, Optional


def load_questions(file_path: Optional[str | Path] = None, n: int = 10) -> List[Dict[str, Any]]:
	"""Load questions from a JSON file and return up to `n` random questions.

	Behavior:
	- If file_path is None, uses the repository's `data/os_questions.json` file.
	- Accepts either an absolute path, or a path relative to the repo root.
	- Handles JSON that is a list of question dicts or a dict with a list under
	  common keys like 'questions' or 'items'.
	- If the file contains fewer than `n` questions, returns all of them in
	  random order.

	Returns an empty list if no questions can be found or parsed.
	"""
	repo_root = Path(__file__).resolve().parents[2]

	if file_path is None:
		file_path = repo_root / "data" / "os_questions.json"
	else:
		file_path = Path(file_path)
		if not file_path.is_absolute():
			file_path = repo_root / file_path

	if not file_path.exists():
		raise FileNotFoundError(f"Questions file not found: {file_path}")

	with file_path.open("r", encoding="utf-8") as fh:
		data = json.load(fh)

	items: List[Dict[str, Any]] = []
	if isinstance(data, list):
		items = data
	elif isinstance(data, dict):
		# common keys that might hold lists of questions
		for key in ("questions", "items", "data", "questions_list"):
			if key in data and isinstance(data[key], list):
				items = data[key]
				break
		else:
			# fallback: first list value in the dict
			lists = [v for v in data.values() if isinstance(v, list)]
			items = lists[0] if lists else []

	# Ensure items are dict-like
	items = [it for it in items if isinstance(it, dict)]

	if not items:
		return []

	# If requested n is greater than available, shuffle and return all
	if n >= len(items):
		random.shuffle(items)
		return items

	return random.sample(items, n)


__all__ = ["load_questions"]

import json
from typing import Dict, Any, List


def _repo_root() -> Path:
	return Path(__file__).resolve().parents[2]


def _queues_path() -> Path:
	return _repo_root() / 'data' / 'user_queues.json'


def load_user_queue(user_id: str) -> List[Dict[str, Any]]:
	"""Load per-user lesson plan queue from data/user_queues.json."""
	p = _queues_path()
	if not p.exists():
		return []
	try:
		data = json.loads(p.read_text(encoding='utf-8'))
		return data.get(user_id, []) if isinstance(data, dict) else []
	except Exception:
		return []


def push_user_queue(user_id: str, entry: Dict[str, Any]) -> None:
	"""Append an entry to a user's queue and persist to disk.

	entry example: {"plan": str, "score": float, "scores": {...}, "iteration": int}
	"""
	p = _queues_path()
	try:
		if p.exists():
			allq = json.loads(p.read_text(encoding='utf-8'))
			if not isinstance(allq, dict):
				allq = {}
		else:
			allq = {}
	except Exception:
		allq = {}

	user_list = allq.get(user_id, [])
	user_list.append(entry)
	allq[user_id] = user_list

	p.parent.mkdir(parents=True, exist_ok=True)
	p.write_text(json.dumps(allq, indent=2), encoding='utf-8')


def get_user_top_plan(user_id: str) -> Dict[str, Any] | None:
	"""Return the highest scored plan entry for the user, or None."""
	q = load_user_queue(user_id)
	if not q:
		return None
	try:
		return max(q, key=lambda x: x.get('score', 0))
	except Exception:
		return None


def save_generated_questions(filename: str, questions: List[Dict[str, Any]]) -> None:
	"""Save a list of generated questions to the given filename under data/."""
	p = _repo_root() / 'data' / filename
	p.parent.mkdir(parents=True, exist_ok=True)
	p.write_text(json.dumps(questions, indent=2), encoding='utf-8')


def append_questions_to_level(level: str, questions: List[Dict[str, Any]]) -> int:
	"""Append generated questions to the canonical level file (os_questions_<level>.json).

	Returns the number of questions appended (skips duplicates by id or exact question text).
	"""
	if not level:
		return 0
	filename = _repo_root() / 'data' / f"os_questions_{level}.json"
	existing: List[Dict[str, Any]] = []
	try:
		if filename.exists():
			existing = json.loads(filename.read_text(encoding='utf-8'))
			if not isinstance(existing, list):
				existing = []
	except Exception:
		existing = []

	# build sets for quick dedupe
	existing_ids = {str(it.get('id')) for it in existing if it.get('id')}
	existing_texts = {str(it.get('question')).strip() for it in existing if it.get('question')}

	to_add: List[Dict[str, Any]] = []
	for q in questions:
		qid = str(q.get('id', ''))
		qtext = str(q.get('question', '')).strip()
		if qid and qid not in existing_ids and qtext and qtext not in existing_texts:
			to_add.append(q)
			existing_ids.add(qid)
			existing_texts.add(qtext)

	if not to_add:
		return 0

	new_list = existing + to_add
	try:
		filename.write_text(json.dumps(new_list, indent=2, ensure_ascii=False), encoding='utf-8')
		return len(to_add)
	except Exception:
		return 0


def _user_history_dir() -> Path:
	"""Directory for per-user plan histories."""
	p = _repo_root() / 'data' / 'user_plans'
	p.mkdir(parents=True, exist_ok=True)
	return p


def _user_best_dir() -> Path:
	p = _repo_root() / 'data' / 'user_best'
	p.mkdir(parents=True, exist_ok=True)
	return p


def save_user_iteration(user_id: str, entry: Dict[str, Any]) -> None:
	"""Append a plan iteration entry to a per-user history file.

	The file is stored at data/user_plans/<user_id>.json as a JSON array of entries.
	Each entry should include: plan (str), score (float), scores (dict), iteration (int), timestamp (optional).
	"""
	p = _user_history_dir() / f"{user_id}.json"
	try:
		if p.exists():
			data = json.loads(p.read_text(encoding='utf-8'))
			if not isinstance(data, list):
				data = []
		else:
			data = []
	except Exception:
		data = []

	data.append(entry)
	p.write_text(json.dumps(data, indent=2), encoding='utf-8')


def load_user_history(user_id: str) -> List[Dict[str, Any]]:
	p = _user_history_dir() / f"{user_id}.json"
	if not p.exists():
		return []
	try:
		data = json.loads(p.read_text(encoding='utf-8'))
		return data if isinstance(data, list) else []
	except Exception:
		return []


def get_user_best_plan(user_id: str) -> Dict[str, Any] | None:
	"""Return the best (highest score) entry for the user from history, or None."""
	history = load_user_history(user_id)
	if not history:
		return None
	try:
		return max(history, key=lambda x: x.get('score', 0))
	except Exception:
		return None


def update_user_best_plan_if_higher(user_id: str, entry: Dict[str, Any]) -> bool:
	"""Update the persisted best-plan file for the user if `entry['score']` is higher.

	Returns True if the best plan was updated, False otherwise.
	"""
	best_dir = _user_best_dir()
	best_path = best_dir / f"{user_id}.json"
	try:
		current = None
		if best_path.exists():
			current = json.loads(best_path.read_text(encoding='utf-8'))
		current_score = current.get('score', 0) if isinstance(current, dict) else 0
		new_score = entry.get('score', 0)
		if new_score > current_score:
			best_path.write_text(json.dumps(entry, indent=2), encoding='utf-8')
			return True
	except Exception:
		pass
	return False


