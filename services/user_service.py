import json
import os

DB_FILE = "data/users.json"


def load_data():

    if not os.path.exists(DB_FILE):

        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)

        return {}

    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        return {}


def save_data(data):

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)