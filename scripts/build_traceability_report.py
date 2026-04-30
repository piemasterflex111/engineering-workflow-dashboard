"""Build a clean traceability CSV from synthetic Jira-style issue data."""

import json
from pathlib import Path

from .traceability_transform import (
    normalize_configuration,
    normalize_module_name,
    normalize_part_number,
)


def load_issues(json_path: Path) -> list[dict]:
    """Load Jira-style issue records from a JSON file."""
    raw_text = json_path.read_text(encoding="utf-8")
    return json.loads(raw_text)


def index_issues_by_key(issues: list[dict]) -> dict[str, dict]:
    """Return a lookup dictionary of issue key to issue record."""
    indexed_issues = {}

    for issue in issues:
        issue_key = issue.get("key")
        if issue_key:
            indexed_issues[issue_key] = issue

    return indexed_issues


def module_to_traceability_row(module_issue: dict, issues_by_key: dict[str, dict]) -> dict:
    """Convert one module issue and its linked issues into a traceability row."""
    fields = module_issue.get("fields", {})
    linked_issue_keys = fields.get("linked_issues", [])

    linked_parts = []
    nc_count = 0
    rework_count = 0

    for linked_key in linked_issue_keys:
        linked_issue = issues_by_key.get(linked_key)
        if not linked_issue:
            continue

        issue_type = linked_issue.get("type")
        linked_fields = linked_issue.get("fields", {})

        if issue_type == "PART":
            part_number = linked_fields.get("part_number")
            if part_number:
                linked_parts.append(normalize_part_number(part_number))

        elif issue_type == "NONCONFORMANCE":
            nc_count += 1

        elif issue_type == "REWORK":
            rework_count += 1

    return {
        "module_key": module_issue.get("key"),
        "module_name": normalize_module_name(fields.get("module_name", "")),
        "configuration": normalize_configuration(fields.get("configuration", "")),
        "part_count": len(linked_parts),
        "nc_count": nc_count,
        "rework_count": rework_count,
        "linked_parts": "|".join(linked_parts),
    }
