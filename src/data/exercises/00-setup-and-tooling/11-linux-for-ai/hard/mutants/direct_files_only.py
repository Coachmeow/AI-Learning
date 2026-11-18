from collections import defaultdict


def human(n):
    """du -h style size: '512B', '1.5K', '14G' (base 1024)."""
    if n < 1024:
        return f"{n}B"
    value, unit = float(n), "B"
    for unit in "KMGT":
        value /= 1024
        if value < 1024 or unit == "T":
            break
    return f"{value:.1f}{unit}" if value < 10 else f"{round(value)}{unit}"


def space_hogs(files, max_depth, top):
    """[(human_size, folder), ...] for the `top` largest folders no deeper than `max_depth`."""
    totals = defaultdict(int)
    for path, size in files.items():
        parts = path.split("/")[:-1]
        totals["/".join(parts) or "."] += size
    depth = lambda p: 0 if p == "." else p.count("/") + 1
    kept = [(p, s) for p, s in totals.items() if depth(p) <= max_depth]
    kept.sort(key=lambda kv: (-kv[1], kv[0]))
    return [(human(s), p) for p, s in kept[:top]]
