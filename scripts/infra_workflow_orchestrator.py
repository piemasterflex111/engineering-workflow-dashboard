"""
Orchestrates the routing of Jira issues based on classification.
"""

from typing import Any, Dict, List

from .infra_ticket_classifier import InfraTicketClassifier
from .jira_client import JiraClient, PermissionError, RetryableError


def jira_safe_label(value: str) -> str:
    """
    Convert human-readable routing text into a Jira-safe label.

    Example:
    Linux Operations -> linux-operations
    Human Review -> human-review
    """
    return value.strip().lower().replace(" ", "-")


class InfraWorkflowOrchestrator:
    """Orchestrates Jira issue routing."""

    def __init__(self, client: JiraClient, dry_run: bool = True):
        self.client = client
        self.dry_run = dry_run
        self.classifier = InfraTicketClassifier()
        self.actions: List[Dict[str, Any]] = []
        self.exceptions: List[Dict[str, Any]] = []

    def process_issues(self, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a list of issues and return planned or executed actions."""
        self.actions = []
        self.exceptions = []

        for issue in issues:
            try:
                category = self.classifier.classify(issue)
                action = self._determine_action(issue, category)
                self.actions.append(action)

                if not self.dry_run:
                    self._execute_action(action)

            except (PermissionError, RetryableError) as error:
                self.exceptions.append(
                    {
                        "issue_key": issue.get("key", "Unknown"),
                        "error": str(error),
                    }
                )

        return self.actions

    def _determine_action(self, issue: Dict[str, Any], category: str) -> Dict[str, Any]:
        """Determine the action to take for an issue."""
        issue_key = issue.get("key", "Unknown")
        safe_label = jira_safe_label(category)

        action = {
            "issue_key": issue_key,
            "category": category,
            "jira_label": safe_label,
            "comment": f"Auto-classified as {category} by BMO Automation.",
            "labels": [safe_label],
            "transition": None,
        }

        if category == "Human Review":
            action["comment"] += " Requires manual review."

        return action

    def _execute_action(self, action: Dict[str, Any]) -> None:
        """Execute the determined action on Jira."""
        issue_key = action["issue_key"]

        # Add audit comment.
        self.client.add_comment(issue_key, action["comment"])

        # Update labels with Jira-safe values only.
        current_issue = self.client.get_issue(issue_key)
        current_labels = current_issue.get("fields", {}).get("labels", []) or []

        new_labels = sorted(set(current_labels + action["labels"]))
        self.client.update_issue(issue_key, {"labels": new_labels})

        # Transition only auto-routed issues. Human Review should remain manual.
        if action["category"] != "Human Review":
            transitions = self.client.get_transitions(issue_key)
            for transition in transitions:
                if transition.get("to", {}).get("name") == "In Progress":
                    self.client.transition_issue(issue_key, transition["id"])
                    break