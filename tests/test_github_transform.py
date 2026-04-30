from scripts.github_transform import pull_request_to_row


def test_pull_request_to_row_flattens_common_github_fields() -> None:
    pr = {
        "number": 42,
        "title": "Add workflow dashboard",
        "state": "closed",
        "user": {"login": "payam"},
        "created_at": "2026-04-20T10:00:00Z",
        "updated_at": "2026-04-21T12:00:00Z",
        "merged_at": "2026-04-21T12:30:00Z",
        "html_url": "https://github.com/example/repo/pull/42",
    }

    row = pull_request_to_row(pr)

    assert row == {
        "number": 42,
        "title": "Add workflow dashboard",
        "state": "closed",
        "author": "payam",
        "created_at": "2026-04-20T10:00:00Z",
        "updated_at": "2026-04-21T12:00:00Z",
        "merged_at": "2026-04-21T12:30:00Z",
        "html_url": "https://github.com/example/repo/pull/42",
    }


def test_pull_request_to_row_marks_missing_user_as_unknown() -> None:
    pr = {
        "number": 43,
        "title": "PR without user",
        "state": "open",
        "user": None,
    }

    row = pull_request_to_row(pr)

    assert row["author"] == "Unknown"
