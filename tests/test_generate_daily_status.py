from scripts.generate_daily_status import render_daily_status


def test_render_daily_status_includes_jira_and_github_metrics() -> None:
    metrics = {
        "jira_total_issues": 11,
        "jira_unassigned_issues": 10,
        "github_total_prs": 0,
        "github_open_prs": 0,
        "github_merged_prs": 0,
    }

    markdown = render_daily_status(metrics, "Engineering Workflow Dashboard")

    assert "# Engineering Workflow Dashboard" in markdown
    assert "- Total issues: 11" in markdown
    assert "- Unassigned issues: 10" in markdown
    assert "- Total pull requests: 0" in markdown
    assert "- Open pull requests: 0" in markdown
    assert "- Merged pull requests: 0" in markdown


def test_render_daily_status_defaults_missing_metrics_to_zero() -> None:
    markdown = render_daily_status({}, "Engineering Workflow Dashboard")

    assert "- Total issues: 0" in markdown
    assert "- Unassigned issues: 0" in markdown
    assert "- Total pull requests: 0" in markdown

