from pathlib import Path
import sys
import traceback

repo_root = Path(__file__).resolve().parents[1]
src_path = str(repo_root / 'src')
print(f"Adding '{src_path}' to sys.path")
sys.path.insert(0, src_path)

try:
    import main
    print('imported main OK')
except Exception:
    traceback.print_exc()
    sys.exit(1)
