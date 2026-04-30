# Project Walkthrough

This project is a Python workflow automation pipeline for engineering teams.

The system starts with two live data sources: Jira issues and GitHub pull requests. The export scripts call each API, collect raw records, flatten the nested API payloads, and save CSV files under `data/`.

The processing step reads those raw CSV files and produces summary metrics such as total Jira issues, unassigned Jira issues, total pull requests, open pull requests, and merged pull requests.

The reporting steps then turn the processed metrics into two human-readable artifacts:

- `reports/daily_status.md`
- `reports/dashboard.html`

The full workflow runs with:

```powershell
python -m scripts.run_pipeline
```

The important design choice is that transformation logic is separated from API logic. For example, `jira_transform.py` and `github_transform.py` can be tested with fake dictionaries without contacting Jira or GitHub.

