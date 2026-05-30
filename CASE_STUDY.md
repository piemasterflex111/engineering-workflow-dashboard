# Engineering Workflow Dashboard and Jira Automation Lab — Case Study

## Problem

Engineering and operations workflows often depend on messy ticket data, inconsistent human-entered strings, and manual reporting. This makes filtering, routing, and status reporting difficult.

## Goal

Build a Python automation project that can:

- fetch workflow data from Jira and GitHub
- normalize nested API payloads
- generate CSV and human-readable reports
- classify infrastructure-style Jira tickets
- dry-run planned actions before live updates
- apply safe Jira sandbox updates only after review

## Architecture

```text
Jira / GitHub APIs
        |
        v
Python API clients
        |
        v
Normalization / transformation
        |
        v
CSV + Markdown + HTML reports

Jira issue search
        |
        v
InfraTicketClassifier
        |
        v
InfraWorkflowOrchestrator
        |
        v
Dry-run action plan
        |
        v
Optional Jira sandbox live update
```

## Implementation

The Jira automation path has four main pieces.

### 1. JiraClient

- handles REST API calls
- authenticates with email/API token
- searches Jira issues
- adds comments
- updates labels
- reads transitions
- transitions issues

### 2. InfraTicketClassifier

- reads issue summary and description
- classifies issues into Linux, Windows, Network, or Human Review

### 3. InfraWorkflowOrchestrator

- loops through issues
- builds action dictionaries
- preserves dry-run safety
- executes Jira updates only in live mode

### 4. route_jira_issues.py

- command-line entry point
- wires the client and orchestrator together

## Real Integration Issues Debugged

- Expired Jira API token caused authentication failure.
- Missing `https://` in the base URL caused URL parsing failure.
- JQL status filter did not match the actual Jira workflow.
- Jira Cloud comment body required Atlassian Document Format.
- Jira labels could not contain spaces.
- Human-readable categories had to be separated from API-safe labels.

## Result

The workflow successfully connected to a personal Jira Cloud sandbox, fetched real issues, classified an infrastructure-style Linux ticket, created a dry-run action plan, and applied sandbox Jira updates after verification.

## Safety Boundaries

- Uses personal sandbox Jira data only.
- No employer, customer, banking, or production data.
- `.env` secrets excluded from Git.
- Dry-run is default.
- Live mode is intentionally explicit.
- This is project-practice automation, not production enterprise deployment.

## Interview Explanation

This project demonstrates how I approach operational automation:

1. Start with read-only visibility.
2. Normalize messy data.
3. Add deterministic classification.
4. Add dry-run action planning.
5. Add tests.
6. Only then enable live updates.
7. Debug real integration failures as they appear.
