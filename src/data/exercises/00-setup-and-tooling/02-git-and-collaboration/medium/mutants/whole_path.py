from fnmatch import fnmatch


def is_ignored(path, patterns):
    for line in patterns:
        p = line.strip()
        if not p or p.startswith("#"):
            continue
        if fnmatch(path, p.lstrip("/").rstrip("/")) or fnmatch(path, "*/" + p.rstrip("/")) or fnmatch(path, p.rstrip("/") + "/*"):
            return True
    return False
