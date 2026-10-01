from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "generated_posts"


def generate_linkedin_post(topic, source, source_url):

    topic_lower = topic.lower()

    if any(
        word in topic_lower
        for word in [
            "ai",
            "openai",
            "anthropic",
            "gemini",
            "react",
            "javascript",
            "typescript",
            "python",
            "aws",
            "docker",
            "kubernetes",
            "cloud",
            "github",
            "cybersecurity",
        ]
    ):
        hashtags = (
            "#Technology #SoftwareEngineering "
            "#AI #Developer #Tech"
        )
    else:
        hashtags = (
            "#Technology #SoftwareEngineering "
            "#Developer #Tech"
        )

    post = f"""A technology story worth checking out today:

{topic}

Why it matters:
This is part of the fast-moving technology landscape that developers and engineering teams need to keep an eye on.

My takeaway:
The useful part isn't simply following every new announcement. It's understanding what changed, checking the original source, and deciding whether it has a practical use case.

Before adopting a new tool, API, framework, or platform, I'd verify the original documentation and test it in a small example first.

Discovered via: {source}

Original source:
{source_url}

{hashtags}
"""

    return post.strip()


def save_post_to_file(post):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = OUTPUT_DIR / "latest_post.txt"

    output_file.write_text(
        post,
        encoding="utf-8",
    )

    return output_file