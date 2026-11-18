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
    clauses = lambda s: [c.strip() for c in s.split(",") if c.strip()]
    specs = {n: clauses(s) for n, s in requirements.items()}
    chosen, queue = {}, sorted(requirements)
    while queue:
        name = queue.pop(0)
        if name in chosen:
            continue
        if name not in index:
            raise ValueError(name)
        ok = [v for v in index[name] if all(satisfies(v, s) for s in specs.get(name, []))]
        if not ok:
            raise ValueError(name)
        v = max(ok, key=parse)
        chosen[name] = v
        for d, s in index[name][v].items():
            specs.setdefault(d, []).extend(clauses(s))
            if d in chosen and not all(satisfies(chosen[d], c) for c in clauses(s)):
                raise ValueError(d)
            queue.append(d)
    return chosen
