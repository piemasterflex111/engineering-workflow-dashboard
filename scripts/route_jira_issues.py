"""
CLI script to route Jira issues based on BMO automation rules.
"""
import argparse
from .jira_client import JiraClient
from .infra_workflow_orchestrator import InfraWorkflowOrchestrator
from .config import APP_CONFIG


def main():
    parser = argparse.ArgumentParser(description="Route Jira issues based on classification.")
    parser.add_argument("--live", action="store_true", help="Execute changes in live mode.")
    args = parser.parse_args()

    client = JiraClient()
    orchestrator = InfraWorkflowOrchestrator(client, dry_run=not args.live)

    # Fetch issues to process
    jql = f"project = {APP_CONFIG.jira.project_key} AND status = Open ORDER BY updated DESC"
    issues = client.search_issues(jql, fields=["summary", "description", "labels"], max_results=50)

    print(f"Processing {len(issues)} issues...")
    actions = orchestrator.process_issues(issues)

    if args.live:
        print("Live mode: Actions executed.")
    else:
        print("Dry-run mode: No changes made.")

    for action in actions:
        print(f"- {action['issue_key']}: {action['category']}")

    if orchestrator.exceptions:
        print("\nExceptions encountered:")
        for exc in orchestrator.exceptions:
            print(f"- {exc['issue_key']}: {exc['error']}")


if __name__ == "__main__":
    main()
