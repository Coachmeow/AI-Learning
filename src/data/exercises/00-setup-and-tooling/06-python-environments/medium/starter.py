def parse(v):
    return [int(p) for p in v.strip().split(".")]


def compare(a, b):
    """-1, 0 or 1 comparing versions as numbers; missing parts count as 0."""
    x, y = parse(a), parse(b)
    n = max(len(x), len(y))
    x += [0] * (n - len(x))
    y += [0] * (n - len(y))
    return (x > y) - (x < y)


def satisfies(version, clause):
    """True if `version` meets one clause such as ">=1.26" or "!=2.0"."""
    for op in (">=", "<=", "==", "!=", ">", "<"):
        if clause.startswith(op):
            target = clause[len(op):].strip()
            c = compare(version, target)
            return {">=": c >= 0, "<=": c <= 0, "==": c == 0, "!=": c != 0, ">": c > 0, "<": c < 0}[op]
    raise ValueError(f"unknown clause: {clause!r}")


def pick_version(available, spec):
    """Newest version in `available` meeting every comma-separated clause of `spec`, or None."""
    raise NotImplementedError
