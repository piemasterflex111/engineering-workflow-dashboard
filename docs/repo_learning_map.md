# Engineering Workflow Dashboard — Learning Map

## What this repo does

This repo has two workflows:

1. Dashboard/reporting pipeline:
   Jira/GitHub data -> CSV -> transforms -> reports/dashboard

2. BMO-style Jira routing automation:
   Jira issues -> classifier -> orchestrator -> dry-run/live Jira updates

## Main routing flow

python -m scripts.route_jira_issues

1. route_jira_issues.py starts the CLI.
2. JiraClient connects to Jira using .env credentials.
3. JiraClient searches issues from project PW.
4. InfraWorkflowOrchestrator loops through issues.
5. InfraTicketClassifier reads summary/description and picks a category.
6. Orchestrator builds an action:
   - issue_key
   - category
   - comment
   - jira-safe label
7. Dry-run prints actions only.
8. Live mode:
   - adds comment
   - updates labels
   - transitions issue if allowed

## Important files

- scripts/jira_client.py: Jira REST calls
- scripts/infra_ticket_classifier.py: category decision logic
- scripts/infra_workflow_orchestrator.py: action planning/execution
- scripts/route_jira_issues.py: command-line entry point
- tests/test_jira_client.py: mocked API behavior tests
- tests/test_infra_ticket_classifier.py: classification tests
- tests/test_infra_workflow_orchestrator.py: orchestration tests

## Important lessons learned

- Jira API token auth must use a valid token.
- Base URL must include https://.
- Jira Cloud comments require ADF format.
- Jira labels cannot contain spaces.
- Dry-run should be the default before live updates.
- Human-readable names and machine-safe API values should be separate.

## Commands

Read-only:
python -m scripts.connect_to_jira
python -m scripts.fetch_jira_issues

Dry-run:
python -m scripts.route_jira_issues

Live:
python -m scripts.route_jira_issues --live

Tests:
python -m pytest -q tests/test_jira_client.py
python -m pytest -q tests/test_infra_ticket_classifier.py
python -m pytest -q tests/test_infra_workflow_orchestrator.py
