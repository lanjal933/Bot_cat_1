import json
import os

SESSION_DB = "data/sesiones.json"


def load_sessions():

    if not os.path.exists(SESSION_DB):

        with open(SESSION_DB, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

        return []

    try:
        with open(SESSION_DB, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        return []


def save_sessions(data):

    with open(SESSION_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)