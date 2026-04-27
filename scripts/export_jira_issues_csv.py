"""
This script takes Jira issue data and saves it as a CSV file.
"""
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from pathlib import Path

from .config import ENV_SETTINGS, APP_CONFIG


def fetch_jira_issues():
    """Fetch Jira issues from the configured project."""
    url = f"{ENV_SETTINGS.jira_base_url}/rest/api/3/search/jql"
    jql = f"project = {APP_CONFIG.jira.project_key} ORDER BY updated DESC"
    fields = ",".join(APP_CONFIG.jira.issue_fields)

    params = {
        "jql": jql,
        "fields": fields,
        "maxResults": APP_CONFIG.jira.max_results,
    }

    response = requests.get(
        url,
        auth=HTTPBasicAuth(
            ENV_SETTINGS.jira_email,
            ENV_SETTINGS.jira_api_token,
        ),
        headers={"Accept": "application/json"},
        params=params,
        timeout=10,
    )

    print("Status Code:", response.status_code)
    if response.status_code != 200:
        print("Jira issue fetch failed")
        print(response.text)
        raise SystemExit(1)
    
    data = response.json()
    issues = data.get("issues", [])
    return issues


def issue_to_row(issue):
    """Convert one Jira issue dictionary into a flat CSV row."""
    row = {}
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
    assignee_data = fields_data.get("assignee", {})

    if assignee_data:
        assignee_name = assignee_data.get("displayName")
    else:
        assignee_name = "Unassigned"

    row["key"] = issue_key
    row["summary"] = summary
    row["status"]  = status_name
    row["created"] = created
    row["updated"] = updated
    row["issue_type"] = issue_type_name
    row["priority"] = priority_name
    row["assignee"] = assignee_name

    return row


def save_rows_to_csv(rows: list[dict], output_path: Path):
    """Save flattened Jira issue rows to a CSV file."""
    file = Path(output_path)
    file.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(file, index=False)
    print(f"Jira rows successfully written to {file}")


def main():
    """Run the Jira issue export workflow."""
    issues = fetch_jira_issues()
    rows = []
    for each_issue in issues:
        row = issue_to_row(each_issue)
        rows.append(row)

    output_path = APP_CONFIG.outputs.raw_jira_issues_csv
    save_rows_to_csv(rows, output_path)


if __name__ == "__main__":
    main()
