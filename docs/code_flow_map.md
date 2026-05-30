# Code Flow Map

## Command traced

python -m scripts.route_jira_issues

## High-level purpose

Fetch Jira issues, classify them into an operations category, build a routing action, and either print the action in dry-run mode or apply it to Jira in live mode.

## File ownership

- scripts/route_jira_issues.py: command-line entry point
- scripts/jira_client.py: Jira REST API client
- scripts/infra_ticket_classifier.py: classification rules
- scripts/infra_workflow_orchestrator.py: action planning and execution

## Runtime path

1. route_jira_issues.py creates JiraClient.
2. JiraClient searches Jira issues.
3. route_jira_issues.py creates InfraWorkflowOrchestrator.
4. process_issues() loops through each issue.
5. classifier.classify(issue) returns a category.
6. _determine_action(issue, category) creates an action dictionary.
7. dry_run=True skips _execute_action().
8. dry_run=False calls Jira update methods.

## One issue traced

Issue: PW-12

Input:
- key: PW-12
- summary: Linux disk full on Ubuntu host

Decision:
- classifier returns Linux Operations

Action:
- comment: Auto-classified as Linux Operations by BMO Automation.
- label: linux-operations

Safety:
- dry-run prints only
- live mode writes to Jira
