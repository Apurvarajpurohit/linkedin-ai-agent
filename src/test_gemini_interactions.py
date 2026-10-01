import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ------------------------------------------------------------
# Load API key
# ------------------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing")


# ------------------------------------------------------------
# Gemini client
# ------------------------------------------------------------

http_options = types.HttpOptions(
    timeout=30000,
    retry_options=types.HttpRetryOptions(
        attempts=1
    ),
)

client = genai.Client(
    api_key=api_key,
    http_options=http_options,
)


# ------------------------------------------------------------
# Test Interactions API
# ------------------------------------------------------------

print("Testing Gemini Interactions API...")
print("Timeout: 30 seconds")
print()

try:
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input="Reply with exactly: INTERACTIONS TEST OK",
        generation_config={
            "thinking_level": "low"
        },
        timeout=30,
    )

    print("RESULT:")
    print(interaction.output_text)

except Exception as error:

    print()
    print("❌ INTERACTIONS TEST FAILED")
    print(type(error).__name__)
    print(error)