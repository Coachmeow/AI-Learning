def _covers(source, path):
    if source == ".":
        return True
    s = source.rstrip("/")
    return path == s or path.startswith(s + "/")


def _sources_changed(instruction, changed):
    words = instruction.split()
    if not words or words[0].upper() not in ("COPY", "ADD"):
        return False
    sources = [w for w in words[1:-1] if not w.startswith("--")]
    return any(_covers(s, f) for s in sources for f in changed)


def rebuild_plan(old, new, changed):
    """For each instruction in `new`, return "cached" or "rebuild" (Docker's layer cache rules)."""
    plan, broken = [], False
    for i, ins in enumerate(new):
        if not broken:
            same = i < len(old) and old[i] == ins
            broken = not same or _sources_changed(ins, changed)
        plan.append("rebuild" if broken else "cached")
    return plan
