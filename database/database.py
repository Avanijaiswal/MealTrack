import os
import json
from datetime import datetime

HISTORY_FILE = "meal_history.json"

def log_meal_json(dish_name, nutrients_dict, calories, flags):
    def get_qty(key):
        return nutrients_dict.get(key, {}).get("quantity", 0)

    now = datetime.now()
    new_entry = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "dish_name": dish_name.title(),
        "calories": round(calories, 1) if calories is not None else None,
        "macros": {
            "protein_g": round(get_qty("PROCNT"), 1),
            "carbs_g": round(get_qty("CHOCDF"), 1),
            "fat_g": round(get_qty("FAT"), 1),
            "sodium_mg": round(get_qty("NA"), 1)
        },
        "flags": flags
    }

    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
                if not isinstance(history, list): history = []
        except (json.JSONDecodeError, ValueError):
            history = []
    else:
        history = []

    history.append(new_entry)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

    print(f"Saved entry to {HISTORY_FILE}")