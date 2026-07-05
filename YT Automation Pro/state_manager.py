import json
import os
from config import DATA_DIR

DEFAULT_STATE = {
    "song_index": 0,      # kaunsa song agli baar use hoga
    "cycle_count": 0,     # kitni baar sabhi songs khatam ho chuke
    "used_pixabay_ids": []  # already used pixabay video ids (repeat na ho)
}


def _state_file(account):
    return os.path.join(DATA_DIR, f"state_{account}.json")


def load_state(account):
    os.makedirs(DATA_DIR, exist_ok=True)
    path = _state_file(account)
    if not os.path.exists(path):
        save_state(account, DEFAULT_STATE)
        return dict(DEFAULT_STATE)
    with open(path, "r") as f:
        return json.load(f)


def save_state(account, state):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(_state_file(account), "w") as f:
        json.dump(state, f, indent=2)


def get_next_song(state, songs_list):
    """Songs cycle: 1 -> 2 -> ... -> N -> 1 -> 2 ..."""
    if not songs_list:
        raise RuntimeError("Songs folder khali hai! Kuch mp3/wav daal do.")

    idx = state["song_index"] % len(songs_list)
    song_path = songs_list[idx]

    next_idx = idx + 1
    if next_idx >= len(songs_list):
        next_idx = 0
        state["cycle_count"] += 1  # ek pura cycle complete hua

    state["song_index"] = next_idx
    return song_path


def mark_video_used(state, video_id, keep_last=500):
    state["used_pixabay_ids"].append(video_id)
    # zyada purana history na badhe isliye trim kar dete hai
    state["used_pixabay_ids"] = state["used_pixabay_ids"][-keep_last:]
