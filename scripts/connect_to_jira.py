import requests
from requests.auth import HTTPBasicAuth

from .config import ENV_SETTINGS

def main():
    url = f"{ENV_SETTINGS.jira_base_url}/rest/api/3/myself"
    response = requests.get(
        url,
        auth=HTTPBasicAuth(ENV_SETTINGS.jira_email, ENV_SETTINGS.jira_api_token),
        headers={"Accept": "application/json"},
        timeout=10,
    )
    print("Status Code:", response.status_code)

    if response.status_code != 200:
        print("Jira connection failed.")
        print(response.text)
        raise SystemExit(1)
    
    data = response.json()

    print("Connected to Jira successfully.")
    print("Display name:", data.get("displayName"))
    print("AccountID:", data.get("accountId"))

if __name__ == "__main__":
    main()