import re

ROUTES = {
    "beginner": {"python": (3, 11), "git": (2, 30)},
    "ml-foundations": {"python": (3, 11), "git": (2, 30), "numpy": (1, 26)},
    "agents": {"python": (3, 11), "git": (2, 30), "node": (20,), "pnpm": (9,)},
    "systems": {"git": (2, 30), "rustc": (1, 75), "cargo": (1, 75)},
}


def preflight(route, outputs):
    need = ROUTES.get(route)
    if need is None:
        raise ValueError(route)
    problems = []
    for tool, minimum in sorted(need.items()):
        text = outputs.get(tool)
        if text is None:
            problems.append((tool, "missing"))
            continue
        m = re.search(r"\d+(?:\.\d+)+", text)
        if m is None:
            problems.append((tool, "unreadable"))
        elif m.group(0) < ".".join(map(str, minimum)):
            problems.append((tool, "too old"))
    return {"ready": not problems, "problems": problems}
