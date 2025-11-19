from utils.io import load_questions

if __name__ == '__main__':
    try:
        qs = load_questions(n=10)
        print(f"Loaded {len(qs)} questions (requested 10).\nPreview:")
        for i, q in enumerate(qs[:3], start=1):
            print(f"{i}. question keys: {list(q.keys())}")
    except Exception as e:
        print("Error loading questions:", e)
