# Engineering Workflow Dashboard

## Purpose

This project demonstrates a Python workflow automation pipeline that connects to Jira and GitHub APIs, retrieves engineering workflow data, saves CSV files, and generates a simple dashboard report.

The goal is to show clean API integration, configuration management, data export, and reporting using Python.

## Data Sources

- Jira Cloud API
- GitHub REST API

## Current Status

- Project structure created
- Virtual environment configured
- Dependencies installed
- Secrets separated into `.env`
- Runtime settings separated into `config.toml`
- Configuration validation implemented with Pydantic
- Jira connection script in progress

## Project Structure

```text
engineering-workflow-dashboard/
  data/
  reports/
  scripts/
    config.py
    connect_to_jira.py
  .env.example
  .gitignore
  config.toml
  README.md
  requirements.txt
```

## Configuration Design

This project separates configuration into two layers:

`.env` stores private or machine-specific values such as API tokens, account identity, and repository information.

`config.toml` stores non-secret application behavior such as Jira project key, issue fields, output paths, and dashboard title.

The Python configuration layer in `scripts/config.py` loads and validates both sources before API code runs.

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

If installing manually from scratch:

```powershell
pip install requests pandas pydantic pydantic-settings python-dotenv
```

Save installed dependencies:

```powershell
pip freeze > requirements.txt
```

## Environment Variables

Create a local `.env` file in the project root.

Use `.env.example` as the template:

```text
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your_email@example.com
JIRA_API_TOKEN=your_jira_api_token_here

GITHUB_TOKEN=your_github_token_here
GITHUB_OWNER=your_github_username
GITHUB_REPO=your_repo_name
```

Do not commit `.env`.

## Runtime Settings

Non-secret runtime settings live in `config.toml`.

Example settings include:

- Jira project key
- Jira issue fields
- Maximum Jira results
- CSV output paths
- Dashboard report title

## Validate Configuration

Run this command from the project root:

```powershell
python -c "from scripts.config import ENV_SETTINGS, APP_CONFIG; print('config loaded')"
```

Expected output:

```text
config loaded
```

## Planned Workflow

1. Load and validate configuration.
2. Connect to Jira API.
3. Retrieve Jira issue workflow data.
4. Save raw Jira data to CSV.
5. Connect to GitHub API.
6. Retrieve pull request or commit activity.
7. Save GitHub data to CSV.
8. Combine processed workflow data.
9. Generate a simple dashboard report.

## Planned Outputs

- `data/jira_issues_raw.csv`
- `data/workflow_summary.csv`
- `reports/dashboard.html`

## Security

Real credentials belong only in `.env`.

The `.env` file is excluded from Git using `.gitignore`.

The committed `.env.example` file documents required variables without exposing real credentials.
