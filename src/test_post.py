import os
from pathlib import Path

import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

TOKEN_FILE = PROJECT_ROOT / "linkedin_token.txt"

ACCESS_TOKEN = TOKEN_FILE.read_text(encoding="utf-8").strip()

# IMPORTANT:
# Copy ONLY the member ID printed by your previous successful run here.
MEMBER_ID = "ZV5fP1L27n"

PERSON_URN = f"urn:li:person:{MEMBER_ID}"

POST_TEXT = """Testing my LinkedIn AI Agent 🚀

This is a test post published through the official LinkedIn API.

The goal of this project is to build an AI agent that finds useful trending technology topics and creates relevant LinkedIn content.

#AI #React #JavaScript #LinkedInAPI
"""

url = "https://api.linkedin.com/rest/posts"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0",
    "Linkedin-Version": "202609",
}

payload = {
    "author": PERSON_URN,
    "commentary": POST_TEXT,
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
    url,
    headers=headers,
    json=payload,
    timeout=30,
)

print("Status:", response.status_code)
print("Response:", response.text)

if response.status_code == 201:
    print("🎉 TEST POST PUBLISHED SUCCESSFULLY!")
    print("Post ID:", response.headers.get("x-restli-id"))
else:
    print("❌ Post was not published.")