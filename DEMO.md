# Demo

## 1. Safe demo

```powershell
python src/main.py --demo
```

Show:
- current selected tech story
- source URL
- duplicate similarity
- validation result
- final LinkedIn-ready post

## 2. Live publish

Set:

```env
PUBLISH_ENABLED=true
```

Then:

```powershell
python src/main.py
```

The agent only records a post in `data/history.json` after LinkedIn confirms a successful publish.

## 3. Scheduled run

GitHub Actions:
- Actions tab
- Morning LinkedIn Tech Post
- Run workflow

The same workflow also runs daily on its schedule.
