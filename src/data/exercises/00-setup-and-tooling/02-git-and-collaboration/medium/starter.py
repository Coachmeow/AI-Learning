from fnmatch import fnmatchcase


def is_ignored(path, patterns):
    """True if `path` (e.g. "runs/3/best.pt") is excluded by one of the .gitignore `patterns`."""
    raise NotImplementedError
