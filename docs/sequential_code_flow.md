# Sequential Code Flow

## Command

python -m scripts.route_jira_issues

## File order

1. scripts/route_jira_issues.py
   Starts the command. Creates JiraClient. Searches Jira. Creates orchestrator.

2. scripts/jira_client.py
   Handles Jira REST API calls. Fetches issues from Jira.

3. scripts/infra_workflow_orchestrator.py
   Receives the issues list. Loops through each issue.

4. scripts/infra_ticket_classifier.py
   Reads issue summary and description. Returns a category.

5. scripts/infra_workflow_orchestrator.py
   Builds the action dictionary:
   - issue_key
   - category
   - comment
   - jira-safe label
   - transition intent

6. scripts/infra_workflow_orchestrator.py
   Checks dry_run.
   - If dry_run=True, no Jira writes happen.
   - If dry_run=False, executes the action.

7. scripts/jira_client.py
   In live mode only, performs Jira writes:
   - add_comment
   - get_issue
   - update_issue
   - get_transitions
   - transition_issue

## One traced issue

PW-12:
- summary: Linux disk full on Ubuntu host
- classifier result: Linux Operations
- Jira-safe label: linux-operations
- dry-run: prints action only
- live: writes comment/label/transition to Jira

## Rule

Do not debug by reading random files.
Debug by following the call chain:
entry file -> client -> orchestrator -> classifier -> orchestrator -> client writes.
