from fnmatch import fnmatchcase


def is_ignored(path, patterns):
    parts = path.split("/")
    for line in patterns:
        p = line.strip()
        if not p:
            continue
        if p.endswith("/"):
            if any(fnmatchcase(x, p[:-1]) for x in parts[:-1]):
                return True
        elif p.startswith("/"):
            want = p[1:].split("/")
            if len(want) == len(parts) and all(fnmatchcase(a, b) for a, b in zip(parts, want)):
                return True
        elif fnmatchcase(parts[-1], p):
            return True
    return False
