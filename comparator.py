import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "data" / "history.json"

def load_history():
    if not HISTORY_FILE.exists():
        return {}
    with HISTORY_FILE.open() as f:
        return json.load(f)

def save_history(items: list):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {item["id"]: item for item in items}
    with HISTORY_FILE.open("w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_changes(current_items: list, history: dict):
    new_items = []
    updated_items = []

    for item in current_items:
        prev = history.get(item["id"])
        if not prev:
            new_items.append(item)
        elif prev["summary"] != item["summary"]:
            item["prev_summary"] = prev["summary"]
            updated_items.append(item)

    return new_items, updated_items