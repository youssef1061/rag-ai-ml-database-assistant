from pathlib import Path
from urllib.request import urlretrieve

BASE_URL = "https://raw.githubusercontent.com/ahmedm0ssad/RAG-Optimization-System/main/data/raw"
FILES = ["AI.txt", "Machine_Learning.txt", "Database.txt"]

output_dir = Path(__file__).resolve().parents[1] / "data" / "raw"
output_dir.mkdir(parents=True, exist_ok=True)
for name in FILES:
    destination = output_dir / name
    urlretrieve(f"{BASE_URL}/{name}", destination)
    print(f"Downloaded: {destination}")
