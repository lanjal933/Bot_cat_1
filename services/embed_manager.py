import os
import json

EMBED_DB = "data/embeds.json"


# =========================
# LOAD EMBEDS
# =========================

def load_embeds():

    if not os.path.exists(EMBED_DB):

        with open(EMBED_DB, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)

        return {}

    try:
        with open(EMBED_DB, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        return {}


# =========================
# SAVE EMBEDS
# =========================

def save_embeds(data):

    with open(EMBED_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)