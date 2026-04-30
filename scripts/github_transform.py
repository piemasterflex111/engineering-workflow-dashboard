"""Helpers for converting GitHub API pull request payloads into flat report rows."""


def pull_request_to_row(pr: dict) -> dict:
    """Convert one GitHub pull request dictionary into a flat CSV-friendly row."""
    user_data = pr.get("user")

    if user_data:
        author = user_data.get("login", "Unknown")
    else:
        author = "Unknown"

    return {
        "number": pr.get("number"),
        "title": pr.get("title"),
        "state": pr.get("state"),
        "author": author,
        "created_at": pr.get("created_at"),
        "updated_at": pr.get("updated_at"),
        "merged_at": pr.get("merged_at"),
        "html_url": pr.get("html_url"),
    }
