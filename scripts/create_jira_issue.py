"""
This script creates a real Jira issue in the configured Jira project.
"""
import requests
from requests.auth import HTTPBasicAuth

from .config import ENV_SETTINGS, APP_CONFIG


def create_jira_issue(summary: str, issue_type: str = "Task") -> str:
    """
    Create a real Jira issue in the configured Jira project and return its issue key.
    """
    url = f"{ENV_SETTINGS.jira_base_url}/rest/api/3/issue"

    payload = {
        "fields": {
            "project": {
                "key": APP_CONFIG.jira.project_key,
            },
            "summary": summary,
            "issuetype": {
                "name": issue_type,
            },
        }
    }

    response = requests.post(
        url,
        auth=HTTPBasicAuth(
            ENV_SETTINGS.jira_email,
            ENV_SETTINGS.jira_api_token,
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=10,
    )

    if response.status_code not in (200, 201):
        print("Issue creation failed.")
        print("Status Code:", response.status_code)
        print(response.text)
        raise SystemExit(1)

    data = response.json()
    issue_key = data.get("key")

    if issue_key is None:
        raise ValueError(f"Jira create response did not include issue key: {data}")

    return issue_key


def main() -> None:
    summary = input("Enter Jira issue summary: ").strip()
    issue_type = "Task"
    if not summary:
        raise SystemExit("Summary cannot be blank.")
    print("Project:", APP_CONFIG.jira.project_key)
    print("Issue type:", issue_type)
    print("Summary:", summary)
    confirm = input("Create this Jira issue? y/N:").strip().lower()
    if confirm == "y":
        created_issue_key = create_jira_issue(
            summary=summary,
            issue_type=issue_type,
        )
        print("Created Jira issue:", created_issue_key)
    else:
        print("Issue creation canceled")
        return
   

if __name__ == "__main__":
    main()
    