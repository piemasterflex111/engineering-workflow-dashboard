# LinkedIn Post Draft

I built a Python engineering workflow dashboard as a hands-on automation project.

The pipeline connects to Jira and GitHub, exports workflow data to CSV, builds summary metrics, and generates Markdown/HTML reports.

I also added a synthetic Jira traceability workflow inspired by hardware module, part, nonconformance, and rework tracking. The goal was to model a real problem I have seen in engineering environments: messy linked tickets and inconsistent human-entered strings that make filtering and reporting difficult.

What the project demonstrates:

- Jira Cloud API integration
- GitHub REST API integration
- `.env` secrets and `config.toml` runtime settings
- nested API payload normalization
- CSV exports and processed metrics
- Markdown and HTML report generation
- pytest coverage for pure transformation logic
- synthetic traceability normalization for hardware-style workflows

The main lesson:

Raw workflow data is not automatically useful. The value comes from turning it into repeatable, inspectable, human-readable evidence.

Repo:
https://github.com/piemasterflex111/engineering-workflow-dashboard

