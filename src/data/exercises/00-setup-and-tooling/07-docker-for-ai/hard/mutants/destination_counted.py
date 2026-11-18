def _covers(source, path):
    if source == ".":
        return True
    s = source.rstrip("/")
    return path == s or path.startswith(s + "/")


def rebuild_plan(old, new, changed):
    plan, broken = [], False
    for i, ins in enumerate(new):
        if not broken:
            words = ins.split()
            src = [w for w in words[1:] if not w.startswith("--")] if words[0].upper() in ("COPY", "ADD") else []
            broken = not (i < len(old) and old[i] == ins) or any(_covers(s, f) for s in src for f in changed)
        plan.append("rebuild" if broken else "cached")
    return plan
