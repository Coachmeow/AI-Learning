from collections import defaultdict


def profile_report(events):
    """[{"func", "ncalls", "tottime", "cumtime"}, ...] sorted by cumtime (desc), then func."""
    ncalls, tottime, cumtime = defaultdict(int), defaultdict(float), defaultdict(float)
    stack = []
    for kind, func, t in events:
        if kind == "call":
            ncalls[func] += 1
            stack.append([func, t, 0.0])
        elif kind == "return":
            if not stack or stack[-1][0] != func:
                raise ValueError(f"return from {func!r} does not match the call stack")
            _, start, child = stack.pop()
            duration = t - start
            tottime[func] += duration - child
            if all(frame[0] != func for frame in stack):
                cumtime[func] += duration
            if stack:
                stack[-1][2] += duration
        else:
            raise ValueError(f"unknown event kind: {kind!r}")
    rows = [{"func": f, "ncalls": ncalls[f], "tottime": tottime[f], "cumtime": cumtime[f]} for f in ncalls]
    rows.sort(key=lambda r: (-r["tottime"], r["func"]))
    return rows
