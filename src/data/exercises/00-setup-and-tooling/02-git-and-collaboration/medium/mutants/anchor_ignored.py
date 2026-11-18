from fnmatch import fnmatchcase


def is_ignored(path, patterns):
    parts = path.split("/")
    for line in patterns:
        p = line.strip()
        if not p or p.startswith("#"):
            continue
        if p.endswith("/"):
            if any(fnmatchcase(x, p[:-1]) for x in parts[:-1]):
                return True
        elif fnmatchcase(parts[-1], p.lstrip("/")):
            return True
    return False
