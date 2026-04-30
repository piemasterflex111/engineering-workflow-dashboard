# Case Study: Engineering Workflow Dashboard

## Problem

Engineering teams often track work across tools such as Jira and GitHub, then manually copy data into spreadsheets or status reports. That creates repeat work, inconsistent reporting, and weak traceability.

In hardware-adjacent environments, Jira can also become a traceability system for modules, parts, nonconformances, and rework records. Those records often contain inconsistent human-entered strings that are difficult to filter or export cleanly.

## Goal

Build a small Python automation pipeline that demonstrates how raw engineering workflow data can become repeatable reports:

- fetch Jira issue data
- fetch GitHub pull request data
- normalize nested API responses
- compute summary metrics
- generate Markdown and HTML reports
- test transformation logic without relying on live APIs

## Constraints

- credentials must not be committed
- generated CSVs may contain live project data and should stay out of git
- tests should not require Jira, GitHub, or network access
- outputs should be inspectable by non-developers
- synthetic traceability data must not expose real company data

## Solution

The project separates responsibilities into small scripts:

- `scripts/config.py` loads `.env` and `config.toml`
- export scripts call Jira and GitHub APIs
- transform modules flatten raw API records
- summary/report scripts produce processed metrics and human-readable artifacts
- traceability modules normalize synthetic hardware-style Jira records

The pipeline can be run with:

```powershell
python -m scripts.run_pipeline
```

## Evidence Artifacts

The repo produces:

- `data/raw_jira_issues.csv`
- `data/raw_github_prs.csv`
- `data/processed_workflow.csv`
- `reports/daily_status.md`
- `reports/dashboard.html`

The committed report artifacts show the shape of the output without exposing private CSV data.

## Testing Strategy

Tests focus on pure logic:

- Jira issue transformation
- GitHub pull request transformation
- Markdown rendering
- HTML rendering
- pipeline step order
- traceability normalization
- linked issue traceability row generation

This keeps tests reliable because they do not call live APIs.

## What This Demonstrates

- API integration
- configuration and secret separation
- CSV/report generation
- pytest-based verification
- workflow orchestration
- synthetic traceability modeling
- practical automation for engineering data

## Next Improvements

- add richer dashboard styling
- export synthetic traceability rows to CSV
- add GitHub Actions CI badge to the README
- add screenshots of the HTML dashboard
- add more workflow metrics such as Jira status counts and PR age

