# app/srs_scheduler.py
import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any

STATE_FILE = "srs_state.json"

def schedule_task(topic: str, quality: int = 3, state_file: str = STATE_FILE) -> Dict[str, Any]:
    """
    quality: 0-5 where higher means better recall. returns next review date.
    """
    try:
        state = {}
        if os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
    except Exception:
        state = {}

    # simple scheduling: next_review = now + days where days = max(1, 2^(5-quality))
    days = max(1, 2 ** max(0, 5 - quality))
    next_review = (datetime.utcnow() + timedelta(days=days)).isoformat()
    state[topic] = {"last_quality": quality, "next_review": next_review, "scheduled_at": datetime.utcnow().isoformat()}
    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception:
        pass
    return {"topic": topic, "next_review": next_review, "quality": quality}
