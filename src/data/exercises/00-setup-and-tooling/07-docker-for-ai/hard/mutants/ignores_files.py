def rebuild_plan(old, new, changed):
    plan, broken = [], False
    for i, ins in enumerate(new):
        if not broken:
            broken = not (i < len(old) and old[i] == ins)
        plan.append("rebuild" if broken else "cached")
    return plan
