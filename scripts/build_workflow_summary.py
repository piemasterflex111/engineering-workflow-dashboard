"""
Build summary workflow metrics from raw Jira and GitHub CSV exports.
"""

from pathlib import Path
import pandas as pd
from .config import APP_CONFIG


def count_rows(csv_path: Path) -> int:
    """Return the number of data rows in a CSV file."""
    if not csv_path.exists():
        return 0

    df = pd.read_csv(csv_path)
    return len(df)


def count_matching_value(csv_path: Path, column_name: str, expected_value: str) -> int:
    """Count rows where a CSV column matches an expected value."""
    if not csv_path.exists():
        return 0

    df = pd.read_csv(csv_path)

    if column_name not in df.columns:
        return 0

    matches = df[column_name] == expected_value
    return int(matches.sum())


def count_non_empty_value(csv_path: Path, column_name: str) -> int:
    """Count rows where a CSV column has a non-empty value."""
    if not csv_path.exists():
        return 0

    df = pd.read_csv(csv_path)

    if column_name not in df.columns:
        return 0

    non_empty_values = df[column_name].notna()
    return int(non_empty_values.sum())


def build_summary_rows() -> list[dict]:
    """Build high-level workflow summary metrics."""
    jira_csv_path = Path(APP_CONFIG.outputs.raw_jira_issues_csv)
    github_csv_path = Path(APP_CONFIG.outputs.raw_github_prs_csv)

    jira_total = count_rows(jira_csv_path)
    github_total = count_rows(github_csv_path)

    jira_unassigned = count_matching_value(
        jira_csv_path,
        "assignee",
        "Unassigned",
    )
    github_open_prs = count_matching_value(
        github_csv_path,
        "state",
        "open",
    )
    github_merged_prs = count_non_empty_value(
        github_csv_path,
        "merged_at",
    )

    return [
        {
            "metric": "jira_total_issues",
            "value": jira_total,
        },
        {
            "metric": "jira_unassigned_issues",
            "value": jira_unassigned,
        },
        {
            "metric": "github_total_prs",
            "value": github_total,
        },
        {
            "metric": "github_open_prs",
            "value": github_open_prs,
        },
        {
            "metric": "github_merged_prs",
            "value": github_merged_prs,
        },
    ]


def save_summary_rows(rows: list[dict], output_path: Path) -> None:
    """Save workflow summary metrics to a CSV file."""
    file = Path(output_path)
    file.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(rows, columns=["metric", "value"])
    df.to_csv(file, index=False)

    print(f"Workflow summary written to {file}")


def main() -> None:
    """Run the workflow summary build step."""
    rows = build_summary_rows()
    output_path = Path(APP_CONFIG.outputs.processed_workflow_csv)
    save_summary_rows(rows, output_path)


if __name__ == "__main__":
    main()
