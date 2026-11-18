import re

ROUTES = {
    "beginner": {"python": (3, 11), "git": (2, 30)},
    "ml-foundations": {"python": (3, 11), "git": (2, 30), "numpy": (1, 26)},
    "agents": {"python": (3, 11), "git": (2, 30), "node": (20,), "pnpm": (9,)},
    "systems": {"git": (2, 30), "rustc": (1, 75), "cargo": (1, 75)},
}


def _version(text):
    m = re.search(r"\d+(?:\.\d+)+", text)
    return tuple(int(p) for p in m.group(0).split(".")) if m else None


def preflight(route, outputs):
    need = ROUTES.get(route)
    if need is None:
        raise ValueError(route)
    problems = []
    for tool in sorted(set(need) | set(outputs)):
        text = outputs.get(tool)
        if text is None:
            problems.append((tool, "missing"))
            continue
        found = _version(text)
        if found is None:
            problems.append((tool, "unreadable"))
        elif tool in need and found < need[tool]:
            problems.append((tool, "too old"))
    return {"ready": not problems, "problems": problems}
