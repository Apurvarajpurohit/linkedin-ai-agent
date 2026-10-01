# LinkedIn Tech Trend Agent

A simple Python automation agent that finds a current technology story, creates a LinkedIn-ready post with the original source link, checks for duplicates, validates basic quality rules, and publishes through LinkedIn's official Posts API.

## Flow

Hacker News
→ Tech topic selection
→ Source-linked post
→ Duplicate check
→ Safety validation
→ LinkedIn official API
→ History + logs

## Local demo

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src/main.py --demo
```

`--demo` never publishes to LinkedIn.

## Real publish

Put these in `.env`:

```env
LINKEDIN_PERSON_URN=urn:li:person:...
PUBLISH_ENABLED=true
```

Keep `linkedin_token.txt` in the project root, or set `LINKEDIN_ACCESS_TOKEN`.

Then:

```powershell
python src/main.py
```

## 9 AM automation

GitHub Actions runs the workflow every day at 9:00 AM Asia/Kolkata using the repository workflow:

`.github/workflows/morning_post.yml`

GitHub supports scheduled workflows with cron and IANA time zones. Scheduled runs can occasionally be delayed during GitHub Actions load spikes.

Add these repository secrets:

- `LINKEDIN_PERSON_URN`
- `LINKEDIN_ACCESS_TOKEN`

Never commit `.env` or `linkedin_token.txt`.

## Resume description

**LinkedIn Tech Trend Agent | Python, REST APIs, LinkedIn API, Automation**

Built a Python automation agent that discovers current technology stories, generates source-linked LinkedIn content, prevents duplicate posts, performs deterministic safety checks, publishes approved posts through LinkedIn's official API, and runs on a daily GitHub Actions schedule.
