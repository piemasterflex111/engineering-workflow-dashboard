"""
Tests for InfraTicketClassifier.
"""
import pytest
from scripts.infra_ticket_classifier import InfraTicketClassifier


@pytest.fixture
def classifier():
    return InfraTicketClassifier()


def test_linux_classification(classifier):
    issue = {
        "fields": {
            "summary": "Linux disk full on server",
            "description": "The /var partition is full."
        }
    }
    assert classifier.classify(issue) == "Linux Operations"


def test_windows_classification(classifier):
    issue = {
        "fields": {
            "summary": "Windows service failed",
            "description": "IIS service crashed."
        }
    }
    assert classifier.classify(issue) == "Windows Operations"


def test_network_classification(classifier):
    issue = {
        "fields": {
            "summary": "DNS resolution failure",
            "description": "Packet loss observed on router."
        }
    }
    assert classifier.classify(issue) == "Network Operations"


def test_human_review_classification(classifier):
    issue = {
        "fields": {
            "summary": "General inquiry about project",
            "description": "No specific technical details."
        }
    }
    assert classifier.classify(issue) == "Human Review"
