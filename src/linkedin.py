import os
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

POST_URL = "https://api.linkedin.com/rest/posts"
TOKEN_FILE = ROOT / "linkedin_token.txt"


def _get_token():
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if token:
        return token

    if TOKEN_FILE.exists():
        token = TOKEN_FILE.read_text(encoding="utf-8").strip()
        if token:
            return token

    raise RuntimeError("LinkedIn access token not found.")


def publish_post(post):
    person_urn = os.getenv("LINKEDIN_PERSON_URN")
    if not person_urn:
        raise RuntimeError("LINKEDIN_PERSON_URN is missing from .env")

    token = _get_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "Linkedin-Version": "202609",
    }

    payload = {
        "author": person_urn,
        "commentary": post,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }

    response = requests.post(
        POST_URL,
        headers=headers,
        json=payload,
        timeout=30,
    )

    if response.status_code not in (200, 201):
        raise RuntimeError(
            f"LinkedIn publish failed: HTTP {response.status_code}: {response.text}"
        )

    return response.headers.get("x-restli-id")
