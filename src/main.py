import json
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from trend_finder import find_trends
from content_generator import generate_linkedin_post, save_post_to_file
from duplicate_checker import check_duplicate, record_published_post
from validator import validate_post
from linkedin import publish_post

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

LOG_FILE = ROOT / "logs" / "agent.log"
PUBLISH_ENABLED = (
    __import__("os").getenv("PUBLISH_ENABLED", "false").lower() == "true"
)


def log(message):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def main():
    demo = "--demo" in sys.argv

    print()
    print("=" * 64)
    print("🚀 LINKEDIN TECH TREND AGENT")
    print("=" * 64)
    print()

    trends = find_trends()
    selected = trends[0]

    topic = selected["topic"]
    source = selected["source"]
    source_url = selected["source_url"]

    print(f"🎯 Selected: {topic}")
    print(f"   Source: {source}")
    print(f"   URL: {source_url}")
    print()

    post = generate_linkedin_post(
        topic,
        source,
        source_url,
    )

    path = save_post_to_file(post)
    print(f"✅ Post saved: {path}")
    print()

    similarity, duplicate = check_duplicate(post)
    print("🔁 Duplicate check")
    print(f"   Similarity: {similarity:.0%}")

    if duplicate:
        log("POST BLOCKED: duplicate detected.")
        return 2

    validation = validate_post(
        topic,
        post,
        source_url,
    )

    print()
    print("🔍 Validation")
    print(json.dumps(validation, indent=2))

    if not validation["publishable"]:
        log("POST BLOCKED: validation failed.")
        return 2

    print()
    print("-" * 64)
    print("📝 FINAL LINKEDIN POST")
    print("-" * 64)
    print(post)
    print("-" * 64)

    if demo or not PUBLISH_ENABLED:
        print("✅ DEMO COMPLETE — LinkedIn publish skipped.")
        return 0

    print()
    print("🔗 Publishing to LinkedIn...")

    post_id = publish_post(post)

    record_published_post(
        topic,
        source_url,
        post,
        post_id,
    )

    print()
    print("=" * 64)
    print("🎉 POST PUBLISHED SUCCESSFULLY")
    print("=" * 64)

    if post_id:
        print("Post ID:", post_id)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
