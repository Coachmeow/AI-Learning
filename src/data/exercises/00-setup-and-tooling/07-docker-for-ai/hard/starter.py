def rebuild_plan(old, new, changed):
    """For each instruction in `new`, return "cached" or "rebuild" (Docker's layer cache rules)."""
    raise NotImplementedError
