import sys
from pathlib import Path #import a library to handle file paths

src_path = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(src_path))
print("linked src path")