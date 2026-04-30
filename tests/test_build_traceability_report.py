from pathlib import Path

from scripts.build_traceability_report import (
    index_issues_by_key,
    load_issues,
    module_to_traceability_row,
)


def test_load_issues_reads_sample_traceability_records() -> None:
    sample_path = Path("sample_data/sample_jira_traceability.json")

    issues = load_issues(sample_path)

    assert len(issues) == 5
    assert issues[0]["key"] == "MOD-101"
    assert issues[0]["type"] == "MODULE"


def test_index_issues_by_key_creates_lookup_by_issue_key() -> None:
    issues = [
        {"key": "MOD-101", "type": "MODULE"},
        {"key": "PART-201", "type": "PART"},
    ]

    indexed = index_issues_by_key(issues)

    assert indexed["MOD-101"]["type"] == "MODULE"
    assert indexed["PART-201"]["type"] == "PART"


def test_module_to_traceability_row_follows_linked_issues() -> None:
    sample_path = Path("sample_data/sample_jira_traceability.json")
    issues = load_issues(sample_path)
    issues_by_key = index_issues_by_key(issues)

    module_issue = issues_by_key["MOD-101"]

    row = module_to_traceability_row(module_issue, issues_by_key)

    assert row == {
        "module_key": "MOD-101",
        "module_name": "power_control_module",
        "configuration": "CFG-A-REV-2",
        "part_count": 2,
        "nc_count": 1,
        "rework_count": 1,
        "linked_parts": "P-1001|P-1002",
    }