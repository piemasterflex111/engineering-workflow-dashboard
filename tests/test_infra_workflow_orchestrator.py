"""
Tests for InfraWorkflowOrchestrator.
"""
import pytest
from unittest.mock import Mock, patch
from scripts.infra_workflow_orchestrator import InfraWorkflowOrchestrator
from scripts.jira_client import JiraClient


@pytest.fixture
def client():
    return Mock(spec=JiraClient)


def test_dry_run_does_not_call_client(client):
    orchestrator = InfraWorkflowOrchestrator(client, dry_run=True)
    issues = [
        {
            "key": "TEST-1",
            "fields": {
                "summary": "Linux disk full",
                "description": "Disk is full."
            }
        }
    ]
    
    orchestrator.process_issues(issues)
    
    # Ensure no Jira API calls were made
    client.add_comment.assert_not_called()
    client.update_issue.assert_not_called()
    client.transition_issue.assert_not_called()


def test_live_mode_calls_client(client):
    # Mock the client methods to return expected data
    client.get_issue.return_value = {
        "fields": {
            "labels": []
        }
    }
    client.get_transitions.return_value = [
        {"id": 1, "to": {"name": "In Progress"}}
    ]
    
    orchestrator = InfraWorkflowOrchestrator(client, dry_run=False)
    issues = [
        {
            "key": "TEST-1",
            "fields": {
                "summary": "Linux disk full",
                "description": "Disk is full."
            }
        }
    ]
    
    orchestrator.process_issues(issues)
    
    # Ensure Jira API calls were made
    client.add_comment.assert_called()
    client.update_issue.assert_called()
    client.transition_issue.assert_called()
