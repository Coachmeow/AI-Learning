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
    clauses = [c.strip() for c in spec.split(",") if c.strip()]
    ok = [v for v in available if all(satisfies(v, c) for c in clauses)]
    return max(ok, key=parse) if ok else None


def resolve(index, requirements):
    """Pick one version per needed package so every spec holds, newest first, with backtracking."""

    def search(pending, chosen, specs):
        if not pending:
            return chosen
        name, rest = pending[0], pending[1:]
        if name in chosen:
            return search(rest, chosen, specs)
        if name not in index:
            return None
        for version in sorted(index[name], reverse=True):
            if not all(satisfies(version, s) for s in specs.get(name, [])):
                continue
            deps = index[name][version]
            if any(d in chosen and not satisfies(chosen[d], s) for d, s in deps.items() for s in _clauses(s)):
                continue
            new_specs = {k: list(v) for k, v in specs.items()}
            for d, s in deps.items():
                new_specs.setdefault(d, []).extend(_clauses(s))
            found = search(rest + [d for d in deps if d not in chosen], {**chosen, name: version}, new_specs)
            if found is not None:
                return found
        return None

    start = {name: _clauses(spec) for name, spec in requirements.items()}
    result = search(sorted(requirements), {}, start)
    if result is None:
        raise ValueError("no set of versions satisfies every requirement")
    return result


def _clauses(spec):
    return [c.strip() for c in spec.split(",") if c.strip()]
