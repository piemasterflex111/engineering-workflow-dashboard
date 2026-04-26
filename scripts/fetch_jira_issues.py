import requests
from requests.auth import HTTPBasicAuth

from .config import ENV_SETTINGS, APP_CONFIG


def main():
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
        print("Jira issue fetch failed.")
        print(response.text)
        raise SystemExit(1)
    
    data = response.json()
    issues = data.get("issues", [])
    print(f"Fetched {len(issues)} Jira issues.")

    for issue in issues[:5]:
        key = issue.get("key", "NO-KEY")
        fields_data = issue.get("fields", {})
        summary = fields_data.get("summary", "No summary")
        
        status_data = fields_data.get("status", {})
        status = status_data.get("name", "No status")

        print(f"{key} | {status} | {summary}")

if __name__ == "__main__":
    main()