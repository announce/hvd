import enum


class Column(enum.IntEnum):
    id = 1
    type = 3
    additions = 13
    deletions = 14
    past_different_authors = 18
    future_different_authors = 19
    author_contributions_percent = 20
    patch = 21
    hunk_count = 23
    files_changed = 25
