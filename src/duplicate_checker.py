import json
import re
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HISTORY_FILE = ROOT / "data" / "history.json"
THRESHOLD = 0.85


def _normalize(text):
    text = text.lower()
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_history():
    if not HISTORY_FILE.exists():
        return []
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def save_history(history):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def check_duplicate(post):
    current = _normalize(post)
    best = 0.0

    for item in load_history():
        previous = _normalize(item.get("post", ""))
        if not previous:
            continue
        score = SequenceMatcher(None, current, previous).ratio()
        best = max(best, score)

    return best, best >= THRESHOLD


def record_published_post(topic, source_url, post, post_id=None):
    history = load_history()
    history.append({
        "topic": topic,
        "source_url": source_url,
        "post": post,
        "post_id": post_id,
    })
    save_history(history)
