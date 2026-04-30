# Engineering Workflow Dashboard

Python automation pipeline that pulls engineering workflow data from Jira and GitHub, normalizes it into CSV files, builds summary metrics, and generates Markdown and HTML reports.

This project is intentionally small, but it follows the same structure used in real engineering automation work: secrets are separated from runtime config, API calls are isolated from transformation logic, outputs are reproducible, and pure logic is covered by pytest tests.

## What It Does

The pipeline:

1. Loads credentials from `.env` and runtime settings from `config.toml`.
2. Fetches Jira issues from a configured Jira project.
3. Fetches GitHub pull requests from a configured repository.
4. Flattens nested API responses into CSV-friendly rows.
5. Writes raw CSV exports under `data/`.
6. Builds processed workflow metrics.
7. Generates a Markdown daily status report.
8. Generates a static HTML dashboard.

The repo also includes a synthetic Jira traceability workflow inspired by hardware module, part, nonconformance, and rework tracking. That sample mode demonstrates how messy Jira-style strings and linked tickets can be normalized into clean traceability records without exposing real company data.

Current generated report example:

```text
Jira total issues: 11
Jira unassigned issues: 10
GitHub total PRs: 0
GitHub open PRs: 0
GitHub merged PRs: 0
```

## Architecture

```text
Jira API        GitHub API
   |                |
   v                v
raw Jira CSV    raw GitHub CSV
   |                |
   +-------> processed workflow metrics
                    |
                    +--> reports/daily_status.md
                    |
                    +--> reports/dashboard.html
```

Synthetic traceability mode:

```text
sample Jira-style module/part/NC/rework records
        |
        v
normalize messy strings and linked tickets
        |
        v
clean module traceability row
```

## Important Files

```text
scripts/config.py                    Load and validate .env + config.toml
scripts/export_jira_issues_csv.py    Fetch Jira issues and write raw CSV
scripts/export_github_prs_csv.py     Fetch GitHub PRs and write raw CSV
scripts/jira_transform.py            Flatten one Jira issue payload
scripts/github_transform.py          Flatten one GitHub PR payload
scripts/build_workflow_summary.py    Build processed metrics
scripts/generate_daily_status.py     Generate Markdown report
scripts/generate_dashboard.py        Generate HTML dashboard
scripts/run_pipeline.py              Run the full workflow
scripts/traceability_transform.py    Normalize messy part/config/module strings
scripts/build_traceability_report.py Build clean traceability rows from linked issues
sample_data/                         Synthetic Jira-style traceability records
tests/                               Pytest coverage for pure logic and pipeline order
```

## Project Structure

```text
engineering-workflow-dashboard/
  data/                  Generated CSV outputs, ignored by git
  docs/                  Project walkthrough and tradeoff notes
  reports/               Committed sample reports
  sample_data/           Safe synthetic Jira-style data
  scripts/               Pipeline scripts and transformation logic
  tests/                 Pytest tests
  .env.example           Credential template
  .gitignore
  config.toml            Non-secret runtime settings
  README.md
  requirements.txt
```

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a local `.env` file using `.env.example` as the template:

```text
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your_email@example.com
JIRA_API_TOKEN=your_jira_api_token_here

GITHUB_TOKEN=your_github_token_here
GITHUB_OWNER=your_github_username
GITHUB_REPO=your_repo_name
```

Do not commit `.env`.

## Configuration

Secrets and local account identity live in `.env`.

Non-secret runtime behavior lives in `config.toml`, including:

- Jira project key
- Jira issue fields
- maximum Jira results
- output file paths
- dashboard title

Validate config loading:

```powershell
python -c "from scripts.config import ENV_SETTINGS, APP_CONFIG; print('config loaded')"
```

## Run The Pipeline

Run the full workflow:

```powershell
python -m scripts.run_pipeline
```

Run individual steps:

```powershell
python -m scripts.export_jira_issues_csv
python -m scripts.export_github_prs_csv
python -m scripts.build_workflow_summary
python -m scripts.generate_daily_status
python -m scripts.generate_dashboard
```

## Outputs

Generated raw and processed data:

```text
data/raw_jira_issues.csv
data/raw_github_prs.csv
data/processed_workflow.csv
```

Report artifacts:

```text
reports/daily_status.md
reports/dashboard.html
```

`data/*.csv` is ignored because those files can contain live project data. The report files are committed as sample outputs.

## Tests

Run all tests:

```powershell
python -m pytest tests
```

Current coverage includes:

- Jira issue transformation
- GitHub PR transformation
- Markdown report rendering
- HTML dashboard rendering
- pipeline step ordering without calling live APIs
- traceability string normalization
- linked Jira-style issue traceability row generation

## What Is Real vs Simplified

Real:

- Jira Cloud API integration
- GitHub REST API integration
- environment-based secrets
- config-driven output paths
- CSV exports
- processed metrics
- Markdown and HTML report generation
- pytest tests for pure logic
- synthetic traceability logic based on real hardware workflow problems

Simplified:

- dashboard styling is intentionally basic
- metrics are intentionally small in scope
- API error handling is still simple
- no scheduled automation or CI pipeline yet
- traceability data is synthetic and sanitized

## Engineering Lessons Demonstrated

- Separate API access from data transformation.
- Keep secrets out of source control.
- Use config files for runtime behavior.
- Make empty outputs deterministic with known CSV columns.
- Test pure logic without depending on live APIs.
- Provide human-readable artifacts, not only raw data dumps.
- Normalize messy operational strings before reporting on them.
- Model linked Jira-style data as traceable records.

## Next Improvements

- Add richer dashboard styling.
- Add Jira status breakdown metrics.
- Add GitHub review/merge-time metrics.
- Export synthetic traceability rows to `data/traceability.csv`.
- Add retry and clearer error categories for API failures.
- Add CI to run pytest on every push.
- Add screenshots to the README.
