import concurrent.futures
import requests

HEADERS = {"User-Agent": "LinkedIn-Tech-Trend-Agent/1.0"}

HN_TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

MAX_STORIES = 50

TECH_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "llm",
    "openai", "anthropic", "gemini", "claude", "deepseek",
    "javascript", "typescript", "python", "java", "rust",
    "golang", "go ", "react", "next.js", "nextjs", "vue",
    "angular", "vite", "frontend", "backend", "web development",
    "aws", "azure", "google cloud", "gcp", "docker", "kubernetes",
    "terraform", "devops", "serverless", "cloud",
    "database", "postgres", "postgresql", "mysql", "mongodb",
    "redis", "graphql", "api", "sdk", "github", "gitlab",
    "open source", "cybersecurity", "cyber security", "vulnerability",
    "zero day", "oauth", "authentication", "gpu", "cpu", "chip",
    "semiconductor", "datacenter", "data center", "developer tools",
    "compiler", "programming", "software"
]

BLOCKED_KEYWORDS = [
    "election", "politics", "politician", "president", "senate",
    "congress", "tax", "taxes", "war", "military", "crime",
    "court", "lawsuit", "real estate", "medical", "medicine",
    "hospital", "football", "cricket", "basketball"
]


def _get_story_ids():
    response = requests.get(
        HN_TOP_URL,
        headers=HEADERS,
        timeout=(3, 8),
    )
    response.raise_for_status()
    return response.json()[:MAX_STORIES]


def _get_story(story_id):
    try:
        response = requests.get(
            HN_ITEM_URL.format(story_id),
            headers=HEADERS,
            timeout=(3, 5),
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def _score_story(story):
    title = (story.get("title") or "").strip()
    if not title:
        return None

    title_lower = title.lower()

    if any(word in title_lower for word in BLOCKED_KEYWORDS):
        return None

    matches = [k for k in TECH_KEYWORDS if k in title_lower]
    if not matches:
        return None

    points = int(story.get("score") or 0)
    comments = int(story.get("descendants") or 0)

    score = (len(matches) * 50) + (min(points, 500) * 0.10) + (min(comments, 500) * 0.05)

    external_url = story.get("url")
    story_url = external_url or f"https://news.ycombinator.com/item?id={story.get('id')}"

    return {
        "topic": title,
        "source": "Hacker News",
        "source_url": story_url,
        "score": round(score, 2),
        "matches": matches,
        "hn_points": points,
        "comments": comments,
    }


def find_trends():
    print("=" * 64)
    print("🔎 FINDING TRENDING TECH NEWS")
    print("=" * 64)
    print()

    try:
        story_ids = _get_story_ids()
    except requests.RequestException as exc:
        print(f"⚠️ Hacker News unavailable: {exc}")
        return [{
            "topic": "Latest technology stories",
            "source": "Hacker News",
            "source_url": "https://news.ycombinator.com/",
            "score": 1,
            "matches": ["technology"],
            "hn_points": 0,
            "comments": 0,
        }]

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        stories = list(executor.map(_get_story, story_ids))

    candidates = []
    seen = set()

    for story in stories:
        if not story or story.get("type") != "story":
            continue
        item = _score_story(story)
        if not item:
            continue

        key = item["topic"].lower()
        if key in seen:
            continue

        seen.add(key)
        candidates.append(item)

    candidates.sort(key=lambda x: x["score"], reverse=True)

    print(f"✅ Found {len(candidates)} technology candidates.")
    print()

    for i, item in enumerate(candidates[:10], 1):
        print(f"{i}. {item['topic']} | Score: {item['score']}")
        print(f"   Topics: {', '.join(item['matches'])}")
        print(f"   Points: {item['hn_points']}")

    print()

    if not candidates:
        return [{
            "topic": "Latest technology stories",
            "source": "Hacker News",
            "source_url": "https://news.ycombinator.com/",
            "score": 1,
            "matches": ["technology"],
            "hn_points": 0,
            "comments": 0,
        }]

    return candidates


if __name__ == "__main__":
    trends = find_trends()
    print("🎯 Selected:", trends[0]["topic"])
    print("🔗 Source:", trends[0]["source_url"])
