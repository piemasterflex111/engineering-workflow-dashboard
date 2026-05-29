"""
Orchestrates the routing of Jira issues based on classification.
"""
from typing import List, Dict, Any, Optional
from .jira_client import JiraClient, PermissionError, RetryableError
from .infra_ticket_classifier import InfraTicketClassifier


class InfraWorkflowOrchestrator:
    """Orchestrates Jira issue routing."""

    def __init__(self, client: JiraClient, dry_run: bool = True):
        self.client = client
        self.dry_run = dry_run
        self.classifier = InfraTicketClassifier()
        self.actions: List[Dict[str, Any]] = []
        self.exceptions: List[Dict[str, Any]] = []

    def process_issues(self, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a list of issues and return actions taken."""
        self.actions = []
        self.exceptions = []

        for issue in issues:
            try:
                category = self.classifier.classify(issue)
                action = self._determine_action(issue, category)
                self.actions.append(action)
                
                if not self.dry_run:
                    self._execute_action(action)
            except (PermissionError, RetryableError) as e:
                self.exceptions.append({
                    "issue_key": issue.get("key", "Unknown"),
                    "error": str(e)
                })

        return self.actions

    def _determine_action(self, issue: Dict[str, Any], category: str) -> Dict[str, Any]:
        """Determine the action to take for an issue."""
        issue_key = issue.get("key", "Unknown")
        summary = issue.get("fields", {}).get("summary", "")
        
        action = {
            "issue_key": issue_key,
            "category": category,
            "comment": f"Auto-classified as {category} by BMO Automation.",
            "labels": [category],
            "transition": None
        }

        # Example: If category is Human Review, don't auto-transition
        if category == "Human Review":
            action["comment"] += " Requires manual review."
        
        return action

    def _execute_action(self, action: Dict[str, Any]) -> None:
        """Execute the determined action on Jira."""
        issue_key = action["issue_key"]
        
        # Add comment
        self.client.add_comment(issue_key, action["comment"])
        
        # Update labels
        current_issue = self.client.get_issue(issue_key)
        current_labels = current_issue.get("fields", {}).get("labels", [])
        new_labels = list(set(current_labels + action["labels"]))
        self.client.update_issue(issue_key, {"labels": new_labels})

        # Transition if applicable (example: move to 'In Progress' for auto-routed)
        if action["category"] != "Human Review":
            transitions = self.client.get_transitions(issue_key)
            for t in transitions:
                if t.get("to", {}).get("name") == "In Progress":
                    self.client.transition_issue(issue_key, t["id"])
                    break
