# scripts/status.py

import json
import os
from datetime import datetime

STATUS_DIR = os.path.join("data", "status")


def _path(chapter_id):
    return os.path.join(STATUS_DIR, f"chapter_{chapter_id}.json")


def update_status(chapter_id, state, step=None, message=None):
    os.makedirs(STATUS_DIR, exist_ok=True)

    payload = {
        "chapter_id": chapter_id,
        "state": state,
        "step": step,
        "message": message,
        "updated_at": datetime.utcnow().isoformat()
    }

    with open(_path(chapter_id), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def read_status(chapter_id):
    path = _path(chapter_id)
    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
