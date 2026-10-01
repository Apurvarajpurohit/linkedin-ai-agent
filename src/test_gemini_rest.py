import os
from pathlib import Path

import requests
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing from .env")


MODEL = "gemini-3.8-flash"

URL = (
    f"https://generativelanguage.googleapis.com/"
    f"v1beta/models/{MODEL}:generateContent"
)


# ============================================================
# REQUEST
# ============================================================

payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": (
                        "Reply with exactly: "
                        "GEMINI REST TEST OK"
                    )
                }
            ]
        }
    ],
    "generationConfig": {
        "temperature": 0.2,
        "maxOutputTokens": 50
    }
}


headers = {
    "x-goog-api-key": API_KEY,
    "Content-Type": "application/json",
}


print("=" * 60)
print("🧪 GEMINI REST API TEST")
print("=" * 60)
print()
print(f"Model: {MODEL}")
print()
print("Sending request...")
print()


try:

    response = requests.post(
        URL,
        headers=headers,
        json=payload,
        timeout=30,
    )

    print(f"HTTP Status: {response.status_code}")
    print()

    if response.status_code != 200:
        print("❌ GEMINI REQUEST FAILED")
        print()
        print(response.text)
        raise SystemExit(1)

    data = response.json()

    text = (
        data["candidates"][0]
        ["content"]["parts"][0]
        ["text"]
    )

    print("✅ GEMINI RESPONSE")
    print()
    print(text)
    print()
    print("=" * 60)


except requests.Timeout:

    print("❌ Request timed out.")


except requests.RequestException as error:

    print("❌ Network error:")
    print(error)


except (KeyError, IndexError, TypeError) as error:

    print("❌ Unexpected Gemini response:")
    print(error)
    print(response.text)