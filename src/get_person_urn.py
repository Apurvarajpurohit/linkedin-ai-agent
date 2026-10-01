from pathlib import Path
import requests


# ------------------------------------------------------------
# Load LinkedIn access token
# ------------------------------------------------------------

token_file = Path("linkedin_token.txt")

if not token_file.exists():
    raise FileNotFoundError(
        "linkedin_token.txt not found in project root."
    )

access_token = token_file.read_text(
    encoding="utf-8"
).strip()

if not access_token:
    raise RuntimeError(
        "linkedin_token.txt is empty."
    )


# ------------------------------------------------------------
# Get LinkedIn user information
# ------------------------------------------------------------

response = requests.get(
    "https://api.linkedin.com/v2/userinfo",
    headers={
        "Authorization": f"Bearer {access_token}"
    },
    timeout=30,
)


print("Status:", response.status_code)

if response.status_code != 200:
    print("LinkedIn response:")
    print(response.text)
    raise SystemExit(1)


data = response.json()

print("Name:", data.get("name"))

member_id = data.get("sub")

if not member_id:
    raise RuntimeError(
        "LinkedIn did not return a member ID."
    )

person_urn = f"urn:li:person:{member_id}"

print("Person URN:", person_urn)