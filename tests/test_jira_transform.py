from scripts.jira_transform import issue_to_row


def test_issue_to_row_flattens_common_jira_fields() -> None:
    issue = {
        "key": "PW-123",
        "fields": {
            "summary": "Validate telemetry export",
            "status": {"name": "In Progress"},
            "created": "2026-04-20T10:00:00.000-0700",
            "updated": "2026-04-21T12:00:00.000-0700",
            "issuetype": {"name": "Task"},
            "priority": {"name": "High"},
            "assignee": {"displayName": "Payam"},
        },
    }

    row = issue_to_row(issue)

    assert row == {
        "key": "PW-123",
        "summary": "Validate telemetry export",
        "status": "In Progress",
        "created": "2026-04-20T10:00:00.000-0700",
        "updated": "2026-04-21T12:00:00.000-0700",
        "issue_type": "Task",
        "priority": "High",
        "assignee": "Payam",
    }


def test_issue_to_row_marks_missing_assignee_as_unassigned() -> None:
    issue = {
        "key": "PW-124",
        "fields": {
            "summary": "Unassigned work item",
            "status": {"name": "To Do"},
        },
    }

    row = issue_to_row(issue)

    assert row["assignee"] == "Unassigned"
    assert row["status"] == "To Do"
    assert row["issue_type"] == "No issue type"
    assert row["priority"] == "No priority"


def test_issue_to_row_handles_missing_fields() -> None:
    issue = {
        "key": "PW-126",
    }

    row = issue_to_row(issue)

    assert row["key"] == "PW-126"
    assert row["summary"] is None
    assert row["status"] == "No status"
    assert row["issue_type"] == "No issue type"
    assert row["priority"] == "No priority"
    assert row["assignee"] == "Unassigned"
