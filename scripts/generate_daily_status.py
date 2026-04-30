"""Generate a Markdown status report from processed workflow metrics."""

from pathlib import Path

import pandas as pd

from .config import APP_CONFIG


def load_metrics(summary_csv_path: Path) -> dict[str, int]:
    """Load metric/value rows from a processed workflow CSV file."""
    if not summary_csv_path.exists():
        return {}

    df = pd.read_csv(summary_csv_path)

    if "metric" not in df.columns or "value" not in df.columns:
        return {}

    metrics: dict[str, int] = {}
    for _, row in df.iterrows():
        metric_name = str(row["metric"])
        metric_value = int(row["value"])
        metrics[metric_name] = metric_value

    return metrics


def metric_value(metrics: dict[str, int], name: str) -> int:
    """Return a metric value, defaulting to zero when the metric is missing."""
    return metrics.get(name, 0)


def render_daily_status(metrics: dict[str, int], title: str) -> str:
    """Render workflow metrics as a human-readable Markdown report."""
    jira_total = metric_value(metrics, "jira_total_issues")
    jira_unassigned = metric_value(metrics, "jira_unassigned_issues")
    github_total = metric_value(metrics, "github_total_prs")
    github_open = metric_value(metrics, "github_open_prs")
    github_merged = metric_value(metrics, "github_merged_prs")

    return "\n".join(
        [
            f"# {title}",
            "",
            "## Jira",
            "",
            f"- Total issues: {jira_total}",
            f"- Unassigned issues: {jira_unassigned}",
            "",
            "## GitHub",
            "",
            f"- Total pull requests: {github_total}",
            f"- Open pull requests: {github_open}",
            f"- Merged pull requests: {github_merged}",
            "",
        ]
    )


def save_markdown_report(markdown: str, output_path: Path) -> None:
    """Write a Markdown report to disk."""
    file = Path(output_path)
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(markdown, encoding="utf-8")
    print(f"Daily status report written to {file}")


def main() -> None:
    """Generate the configured daily status report."""
    metrics = load_metrics(Path(APP_CONFIG.outputs.processed_workflow_csv))
    markdown = render_daily_status(metrics, APP_CONFIG.dashboard.title)
    save_markdown_report(markdown, Path(APP_CONFIG.outputs.daily_status_md))


if __name__ == "__main__":
    main()

