"""Fetch GitHub pull requests and save them as a CSV file."""

from pathlib import Path

import pandas as pd
import requests

from .config import ENV_SETTINGS, APP_CONFIG
from .github_transform import pull_request_to_row

GITHUB_PR_COLUMNS = [
    "number",
    "title",
    "state",
    "author",
    "created_at",
    "updated_at",
    "merged_at",
    "html_url",
]


def fetch_github_pull_requests() -> list[dict]:
    """Fetch pull requests from the configured GitHub repository."""
    url = f"https://api.github.com/repos/{ENV_SETTINGS.github_owner}/{ENV_SETTINGS.github_repo}/pulls"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {ENV_SETTINGS.github_token}",
    }
    params = {
        "state": "all",
        "per_page": 50,
    }
    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10,
    )
    print("Status Code:", response.status_code)

    if response.status_code != 200:
        print("GitHub PR fetch failed.")
        print(response.text)
        raise SystemExit(1)
    return response.json()


def save_rows_to_csv(rows: list[dict], output_path: Path) -> None:
    """Save flattened GitHub PR rows to a CSV file."""
    file = Path(output_path)
    file.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows, columns=GITHUB_PR_COLUMNS)
    df.to_csv(file, index=False)
    print(f"GitHub PR rows successfully written to {file}")


def main() -> None:
    """Run the GitHub PR export workflow."""
    pull_requests = fetch_github_pull_requests()
    rows = []
    for pr in pull_requests:
        row = pull_request_to_row(pr)
        rows.append(row)
    output_path = APP_CONFIG.outputs.raw_github_prs_csv
    save_rows_to_csv(rows, output_path)


if __name__ == "__main__":
    main()
