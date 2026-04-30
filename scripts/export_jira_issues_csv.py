"""
This script takes Jira issue data and saves it as a CSV file.
"""
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from pathlib import Path

from .config import ENV_SETTINGS, APP_CONFIG
from .jira_transform import issue_to_row


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
