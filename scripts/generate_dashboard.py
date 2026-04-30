"""Generate an HTML dashboard from processed workflow metrics."""

from pathlib import Path

from .config import APP_CONFIG
from .generate_daily_status import load_metrics, metric_value


def render_dashboard_html(metrics: dict[str, int], title: str) -> str:
    """Render workflow metrics as a simple HTML dashboard."""
    jira_total = metric_value(metrics, "jira_total_issues")
    jira_unassigned = metric_value(metrics, "jira_unassigned_issues")
    github_total = metric_value(metrics, "github_total_prs")
    github_open = metric_value(metrics, "github_open_prs")
    github_merged = metric_value(metrics, "github_merged_prs")

    return f"""<!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>

        <h2>Jira</h2>
        <ul>
        <li>Total issues: {jira_total}</li>
        <li>Unassigned issues: {jira_unassigned}</li>
        </ul>

        <h2>GitHub</h2>
        <ul>
        <li>Total pull requests: {github_total}</li>
        <li>Open pull requests: {github_open}</li>
        <li>Merged pull requests: {github_merged}</li>
        </ul>
    </body>
    </html>
    """

def save_html_dashboard(html: str, output_path: Path) -> None:
    """Write an HTML dashboard to disk."""
    file = Path(output_path)
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(html, encoding="utf-8")
    print(f"HTML dashboard written to {file}")


def main() -> None:
    """Generate the configured HTML dashboard."""
    metrics = load_metrics(Path(APP_CONFIG.outputs.processed_workflow_csv))
    html = render_dashboard_html(metrics, APP_CONFIG.dashboard.title)
    save_html_dashboard(html, Path(APP_CONFIG.outputs.dashboard_html))


if __name__ == "__main__":
    main()