"""Run the full engineering workflow dashboard pipeline."""

from . import build_workflow_summary
from . import export_github_prs_csv
from . import export_jira_issues_csv
from . import generate_daily_status
from . import generate_dashboard


def main() -> None:
    """Run all pipeline steps in order."""
    print("Starting engineering workflow dashboard pipeline...")

    print("Step 1/5: Exporting Jira issues...")
    export_jira_issues_csv.main()

    print("Step 2/5: Exporting GitHub pull requests...")
    export_github_prs_csv.main()

    print("Step 3/5: Building workflow summary...")
    build_workflow_summary.main()

    print("Step 4/5: Generating daily status report...")
    generate_daily_status.main()

    print("Step 5/5: Generating HTML dashboard...")
    generate_dashboard.main()

    print("Pipeline complete.")



if __name__ == "__main__":
    main()