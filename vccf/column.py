import enum


class Column(enum.IntEnum):
    """
    # Corrupt data
    * files_changed: all 0
    """
    # Commits
    _commits_id = 0
    repository_id = 1
    blamed_commit_id = 2
    type = 3
    sha = 4
    url = 5
    author_email = 6
    author_name = 7
    author_when = 8
    committer_email = 9
    committer_name = 10
    committer_when = 11
    additions = 12
    deletions = 13
    total_changes = 14
    past_changes = 15
    future_changes = 16
    past_different_authors = 17
    future_different_authors = 18
    author_contributions_percent = 19
    message = 20
    patch = 21
    hunk_count = 22
    cve = 23
    files_changed = 24
    patch_keywords = 25

    # Repositories
    # The paper mentions Star count but not exists
    _repositories_id = 26
    name = 27
    description = 28
    pushed_at = 29
    created_at = 30
    updated_at = 31
    forks_count = 32
    stargazers_count = 33
    watchers_count = 34
    subscribers_count = 35
    open_issues_count = 36
    size = 37
    language = 38
    default_branch = 39
    git_url = 40
    distinct_authors_count = 41
    commits_count = 42
