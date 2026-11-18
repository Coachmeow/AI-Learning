def rebuild_plan(old, new, changed):
    plan, broken = [], False
    for i, ins in enumerate(new):
        if not broken:
            words = ins.split()
            src = [w for w in words[1:-1] if not w.startswith("--")] if words[0].upper() in ("COPY", "ADD") else []
            hit = any(s == "." or s in changed for s in src)
            broken = not (i < len(old) and old[i] == ins) or hit
        plan.append("rebuild" if broken else "cached")
    return plan
