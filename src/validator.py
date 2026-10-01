def validate_post(topic, post, source_url):
    issues = []
    lower = post.lower()

    if len(post) < 80:
        issues.append("Post is too short.")

    if len(post) > 3000:
        issues.append("Post is too long.")

    if not topic.strip():
        issues.append("Topic is empty.")

    if not source_url:
        issues.append("Source URL is missing.")

    elif source_url not in post:
        issues.append("Original source URL is missing from post.")

    clickbait = [
        "this changes everything",
        "you won't believe",
        "guaranteed",
        "shocking",
        "secret",
        "insane",
    ]

    if any(phrase in lower for phrase in clickbait):
        issues.append("Clickbait language detected.")

    return {
        "publishable": len(issues) == 0,
        "technical_accuracy": "LIMITED",
        "issues": issues,
        "summary": (
            "Deterministic validation completed. "
            "The agent does not perform deep factual verification "
            "without an external AI model."
        ),
    }