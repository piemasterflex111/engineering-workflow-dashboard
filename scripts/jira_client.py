"""
Jira client abstraction for BMO automation.
"""
import requests
from requests.auth import HTTPBasicAuth
from typing import List, Dict, Any, Optional
from .config import ENV_SETTINGS


class JiraError(Exception):
    """Base exception for Jira errors."""
    pass


class PermissionError(JiraError):
    """Raised when Jira returns 401 or 403."""
    pass


class RetryableError(JiraError):
    """Raised when Jira returns 429 or 5xx."""
    pass


class JiraClient:
    """Client for interacting with Jira API."""

    def __init__(self, base_url: str = None, email: str = None, api_token: str = None):
        self.base_url = base_url or ENV_SETTINGS.jira_base_url
        self.email = email or ENV_SETTINGS.jira_email
        self.api_token = api_token or ENV_SETTINGS.jira_api_token
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(self.email, self.api_token)
        self.session.headers.update({"Accept": "application/json"})

    def _handle_response(self, response: requests.Response) -> Any:
        """Handle HTTP response and raise appropriate exceptions."""
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 201:
            return response.json()
        elif response.status_code in (401, 403):
            raise PermissionError(f"Permission denied: {response.status_code} {response.text}")
        elif response.status_code == 429 or response.status_code >= 500:
            raise RetryableError(f"Retryable error: {response.status_code} {response.text}")
        else:
            raise JiraError(f"Unexpected error: {response.status_code} {response.text}")

    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """Fetch a single issue by key."""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        response = self.session.get(url, timeout=10)
        return self._handle_response(response)

    def search_issues(self, jql: str, fields: List[str] = None, max_results: int = 50) -> List[Dict[str, Any]]:
        """Search for issues using JQL."""
        url = f"{self.base_url}/rest/api/3/search/jql"
        params = {
            "jql": jql,
            "maxResults": max_results,
        }
        if fields:
            params["fields"] = ",".join(fields)
        
        response = self.session.get(url, params=params, timeout=10)
        data = self._handle_response(response)
        return data.get("issues", [])

    def add_comment(self, issue_key: str, body: str) -> Dict[str, Any]:
        """Add a comment to an issue."""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/comment"
        payload = {"body": body}
        response = self.session.post(url, json=payload, timeout=10)
        return self._handle_response(response)

    def update_issue(self, issue_key: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Update issue fields."""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        payload = {"fields": fields}
        response = self.session.put(url, json=payload, timeout=10)
        return self._handle_response(response)

    def get_transitions(self, issue_key: str) -> List[Dict[str, Any]]:
        """Get available transitions for an issue."""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions"
        response = self.session.get(url, timeout=10)
        data = self._handle_response(response)
        return data.get("transitions", [])

    def transition_issue(self, issue_key: str, transition_id: int) -> None:
        """Transition an issue to a new status."""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions"
        payload = {"transition": {"id": transition_id}}
        response = self.session.post(url, json=payload, timeout=10)
        self._handle_response(response)
