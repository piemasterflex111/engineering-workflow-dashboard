"""Helpers for converting Jira API issue payloads into flat report rows."""


def issue_to_row(issue: dict) -> dict:
    """Convert one Jira issue dictionary into a flat CSV-friendly row."""
    issue_key = issue.get("key")
    fields_data = issue.get("fields", {})
    summary = fields_data.get("summary")

    status_data = fields_data.get("status", {})
    status_name = status_data.get("name", "No status")

    created = fields_data.get("created")
    updated = fields_data.get("updated")

    issue_type_data = fields_data.get("issuetype", {})
    issue_type_name = issue_type_data.get("name", "No issue type")

    priority_data = fields_data.get("priority", {})
    priority_name = priority_data.get("name", "No priority")

    assignee_data = fields_data.get("assignee")
    if assignee_data:
        assignee_name = assignee_data.get("displayName", "Unknown assignee")
    else:
        assignee_name = "Unassigned"

    return {
        "key": issue_key,
        "summary": summary,
        "status": status_name,
        "created": created,
        "updated": updated,
        "issue_type": issue_type_name,
        "priority": priority_name,
        "assignee": assignee_name,
    }

