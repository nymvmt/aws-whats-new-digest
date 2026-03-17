import json
import os

HISTORY_FILE = "data/history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE) as f:
        return json.load(f)

def save_history(items: list):
    os.makedirs("data", exist_ok=True)
    data = {item["id"]: item for item in items}
    with open(HISTORY_FILE, "w") as f:
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