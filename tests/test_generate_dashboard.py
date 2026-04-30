from scripts.generate_dashboard import render_dashboard_html


def test_render_dashboard_html_includes_jira_and_github_metrics() -> None:
      metrics = {
          "jira_total_issues": 11,
          "jira_unassigned_issues": 10,
          "github_total_prs": 0,
          "github_open_prs": 0,
          "github_merged_prs": 0,
      }

      html = render_dashboard_html(metrics, "Engineering Workflow Dashboard")

      assert "<h1>Engineering Workflow Dashboard</h1>" in html
      assert "<li>Total issues: 11</li>" in html
      assert "<li>Unassigned issues: 10</li>" in html
      assert "<li>Total pull requests: 0</li>" in html
      assert "<li>Open pull requests: 0</li>" in html
      assert "<li>Merged pull requests: 0</li>" in html