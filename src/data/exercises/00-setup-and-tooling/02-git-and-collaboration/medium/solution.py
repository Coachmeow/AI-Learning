from fnmatch import fnmatchcase


def _matches(parts, pattern):
    if pattern.endswith("/"):
        return any(fnmatchcase(d, pattern[:-1]) for d in parts[:-1])
    if pattern.startswith("/"):
        want = pattern[1:].split("/")
        return len(want) == len(parts) and all(fnmatchcase(p, w) for p, w in zip(parts, want))
    return fnmatchcase(parts[-1], pattern)


def is_ignored(path, patterns):
    """True if `path` (e.g. "runs/3/best.pt") is excluded by one of the .gitignore `patterns`."""
    parts = path.split("/")
    for line in patterns:
        pattern = line.strip()
        if not pattern or pattern.startswith("#"):
            continue
        if _matches(parts, pattern):
            return True
    return False
