# Engineering Workflow Dashboard and Jira Automation Lab

Python automation project for engineering workflow reporting and Jira-based infrastructure ticket routing.

This project demonstrates how Python can connect to workflow tools, normalize messy operational data, generate human-readable reports, and safely plan or apply Jira workflow updates in a sandbox.

## What This Project Does

The repo has two related workflows.

### 1. Workflow reporting pipeline

- connects to Jira Cloud and GitHub REST APIs
- exports workflow data to CSV
- normalizes nested API payloads
- computes summary metrics
- generates Markdown and HTML reports
- keeps runtime settings in `config.toml`
- keeps secrets out of Git through `.env`

### 2. Jira infrastructure routing automation

- fetches real Jira issues from a personal sandbox project
- classifies tickets into:
  - Linux Operations
  - Windows Operations
  - Network Operations
  - Human Review
- builds a dry-run action plan by default
- optionally applies live Jira sandbox updates
- adds audit comments
- applies Jira-safe labels such as `linux-operations`
- attempts workflow transition when the Jira workflow allows it

## Why This Matters

Engineering and operations teams often work across messy tickets, inconsistent human-entered strings, and disconnected tools.

This project explores a practical pattern:

```text
raw workflow data
→ normalized records
→ classification
→ dry-run action plan
→ safe live update only after review
```

The goal is not to create a production enterprise Jira app. The goal is to demonstrate practical Python automation patterns for operational workflows.

## Key Lessons Learned

During live Jira sandbox integration, the workflow exposed real integration issues:

- expired Jira API token
- missing `https://` in the base URL
- JQL status mismatch
- Jira description fields returning unexpected shapes
- Jira Cloud comments requiring Atlassian Document Format
- Jira labels rejecting spaces
- need to separate human-readable names from API-safe machine values
- need for dry-run mode before live updates

## Main Files

- `scripts/jira_client.py` — Jira REST API boundary. Handles authentication, issue search, comments, labels, transitions, and response/error handling.
- `scripts/infra_ticket_classifier.py` — Deterministic classification logic for routing tickets into Linux, Windows, Network, or Human Review categories.
- `scripts/infra_workflow_orchestrator.py` — Coordinates classification, action planning, dry-run behavior, and live execution.
- `scripts/route_jira_issues.py` — Command-line entry point for the Jira routing workflow.
- `tests/` — Pytest coverage for the Jira client, classifier, and orchestrator behavior.
- `docs/` — Learning maps, code-flow maps, and project documentation.

## Sequential Code Flow

```text
python -m scripts.route_jira_issues

1. route_jira_issues.py starts the command.
2. JiraClient searches Jira issues.
3. InfraWorkflowOrchestrator receives the issue list.
4. InfraTicketClassifier classifies each issue.
5. The orchestrator builds an action dictionary.
6. Dry-run mode prints the action only.
7. Live mode calls JiraClient to add comments, update labels, and transition issues.
```

## Safety Boundaries

- This project uses a personal Jira Cloud sandbox.
- `.env` secrets are not committed.
- Dry-run is the default.
- Live mode should only be used after dry-run output is reviewed.
- No employer, customer, banking, or production data is used.
- This is project-practice automation, not production enterprise deployment.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

Expected `.env` shape:

```bash
JIRA_BASE_URL=https://your-site.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-token
GITHUB_TOKEN=optional-token
```

Do not commit `.env`.

## Run Tests

```bash
python -m pytest -q
```

Run focused tests:

```bash
python -m pytest -q tests/test_jira_client.py
python -m pytest -q tests/test_infra_ticket_classifier.py
python -m pytest -q tests/test_infra_workflow_orchestrator.py
```

## Run Read-Only Jira Checks

```bash
python -m scripts.connect_to_jira
python -m scripts.fetch_jira_issues
```

## Run Jira Routing in Dry-Run Mode

```bash
python -m scripts.route_jira_issues
```

Dry-run mode prints planned actions and does not modify Jira.

## Run Live Mode

Only use live mode against a sandbox project after reviewing dry-run output:

```bash
python -m scripts.route_jira_issues --live
```

## Example Dry-Run Output

```text
Processing 12 issues...
Dry-run mode: No changes made.
- PW-11: Human Review
- PW-10: Human Review
- PW-13: Linux Operations
```

## What This Demonstrates

- Python automation
- Jira REST API integration
- workflow orchestration
- deterministic ticket classification
- dry-run/live execution safety
- API error debugging
- structured operational reporting
- pytest-tested automation logic
- practical infrastructure workflow automation
