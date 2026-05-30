"""
Tests for JiraClient.
"""
import pytest
from unittest.mock import Mock, patch
from scripts.jira_client import JiraClient, PermissionError, RetryableError, JiraError


@pytest.fixture
def client():
    return JiraClient(base_url="http://test.jira.com", email="test@test.com", api_token="token")


def test_permission_error_401(client):
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    
    with patch.object(client.session, 'get', return_value=mock_response):
        with pytest.raises(PermissionError):
            client.get_issue("TEST-1")


def test_permission_error_403(client):
    mock_response = Mock()
    mock_response.status_code = 403
    mock_response.text = "Forbidden"
    
    with patch.object(client.session, 'get', return_value=mock_response):
        with pytest.raises(PermissionError):
            client.get_issue("TEST-1")


def test_retryable_error_429(client):
    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.text = "Too Many Requests"
    
    with patch.object(client.session, 'get', return_value=mock_response):
        with pytest.raises(RetryableError):
            client.get_issue("TEST-1")


def test_retryable_error_500(client):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    
    with patch.object(client.session, 'get', return_value=mock_response):
        with pytest.raises(RetryableError):
            client.get_issue("TEST-1")


def test_successful_get_issue(client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "TEST-1", "fields": {"summary": "Test"}}
    
    with patch.object(client.session, 'get', return_value=mock_response):
        result = client.get_issue("TEST-1")
        assert result["key"] == "TEST-1"
