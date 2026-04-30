from scripts import run_pipeline

def test_run_pipeline_calls_steps_in_order(monkeypatch) -> None:
    calls = []

    def fake_export_jira() -> None:
        calls.append("jira")

    def fake_export_github() -> None:
        calls.append("github")


    def fake_build_summary() -> None:
        calls.append("summary")


    def fake_generate_daily_status() -> None:
        calls.append("daily_status")


    def fake_generate_dashboard() -> None:
        calls.append("dashboard")

    monkeypatch.setattr(run_pipeline.export_jira_issues_csv, "main", fake_export_jira)
    monkeypatch.setattr(run_pipeline.export_github_prs_csv, "main", fake_export_github)
    monkeypatch.setattr(run_pipeline.build_workflow_summary, "main", fake_build_summary)
    monkeypatch.setattr(run_pipeline.generate_daily_status, "main", fake_generate_daily_status)
    monkeypatch.setattr(run_pipeline.generate_dashboard, "main", fake_generate_dashboard)

    run_pipeline.main()

    assert calls == [
          "jira",
          "github",
          "summary",
          "daily_status",
          "dashboard",
      ]