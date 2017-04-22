import enum


class Column(enum.IntEnum):
    """
    # Corrupt data
    * files_changed: all 0
    """
    # Commits
    _commits_id = 1
    repository_id = 2
    type = 3
    blamed_commit_id = 4
    sha = 5
    url = 6
    author_email = 7
    author_name = 8
    author_when = 9
    committer_email = 10
    committer_name = 11
    committer_when = 12
    additions = 13
    deletions = 14
    total_changes = 15
    past_changes = 16
    future_changes = 17
    past_different_authors = 18
    future_different_authors = 19
    author_contributions_percent = 20
    patch = 21
    message = 22
    hunk_count = 23
    cve = 24
    files_changed = 25
    patch_keywords = 26

    # Repositories
    # The paper mentions Star count but not exists
    _repositories_id = 27
    name = 28
    description = 29
    pushed_at = 30
    created_at = 31
    updated_at = 32
    forks_count = 33
    stargazers_count = 34
    watchers_count = 35
    subscribers_count = 36
    open_issues_count = 37
    size = 38
    language = 39
    default_branch = 40
    git_url = 41
    distinct_authors_count = 42
    commits_count = 43
