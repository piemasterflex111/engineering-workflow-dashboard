"""
Jira client abstraction for OpsRoute-style workflow automation.

This client is intentionally small:
- authenticate with Jira Cloud using email + API token
- search issues
- add ADF-formatted comments
- update issue fields
- read transitions
- transition issues by transition id
- map common HTTP failures to clear Python exceptions
"""

from typing import Any, Dict, List, Optional

import requests
from requests.auth import HTTPBasicAuth

from .config import ENV_SETTINGS


class JiraError(Exception):
    """Base exception for Jira errors."""


class JiraPermissionError(JiraError):
    """Raised when Jira returns 401 or 403."""


class JiraRetryableError(JiraError):
    """Raised when Jira returns 429 or 5xx."""

# Backward-compatible names used by existing tests and orchestrator.
PermissionError = JiraPermissionError
RetryableError = JiraRetryableError


def plain_text_to_adf(text: str) -> Dict[str, Any]:
    """
    Convert a plain text string into Atlassian Document Format.

    Jira Cloud REST API v3 expects comment bodies as ADF, not raw strings.
    """
    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": text,
                    }
                ],
            }
        ],
    }


class JiraClient:
    """Client for interacting with the Jira Cloud REST API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        email: Optional[str] = None,
        api_token: Optional[str] = None,
    ):
        self.base_url = (base_url or ENV_SETTINGS.jira_base_url).rstrip("/")
        self.email = email or ENV_SETTINGS.jira_email
        self.api_token = api_token or ENV_SETTINGS.jira_api_token

        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(self.email, self.api_token)
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def _handle_response(self, response: requests.Response):
        if response.status_code == 204:
            return None

        if response.status_code in (200, 201):
            return response.json()

        if response.status_code in (401, 403):
            raise JiraPermissionError(response.text)

        if response.status_code == 404:
            raise LookupError(response.text)

        if response.status_code in (429, 500, 502, 503, 504):
            raise JiraRetryableError(response.text)

        raise JiraError(f"Unexpected error: {response.status_code} {response.text}")

    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """Fetch a single issue by key."""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        response = self.session.get(url, timeout=10)
        return self._handle_response(response)

    def search_issues(
        self,
        jql: str,
        fields: Optional[List[str]] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
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
        """Add an ADF-formatted comment to an issue."""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/comment"
        payload = {
            "body": plain_text_to_adf(body),
        }
        response = self.session.post(url, json=payload, timeout=10)
        return self._handle_response(response)

    def update_issue(self, issue_key: str, fields: Dict[str, Any]):
        """Update issue fields."""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        payload = {"fields": fields}
        response = self.session.put(url, json=payload, timeout=10)
        return self._handle_response(response)

    def get_transitions(self, issue_key: str) -> List[Dict[str, Any]]:
        """Get available workflow transitions for an issue."""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions"
        response = self.session.get(url, timeout=10)
        data = self._handle_response(response)
        return data.get("transitions", [])

    def transition_issue(self, issue_key: str, transition_id: str) -> None:
        """Transition an issue using a Jira transition id."""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions"
        payload = {"transition": {"id": str(transition_id)}}
        response = self.session.post(url, json=payload, timeout=10)
        self._handle_response(response)