import re

# Tools each route needs, with the minimum version of each.
ROUTES = {
    "beginner": {"python": (3, 11), "git": (2, 30)},
    "ml-foundations": {"python": (3, 11), "git": (2, 30), "numpy": (1, 26)},
    "agents": {"python": (3, 11), "git": (2, 30), "node": (20,), "pnpm": (9,)},
    "systems": {"git": (2, 30), "rustc": (1, 75), "cargo": (1, 75)},
}


def preflight(route, outputs):
    """Check the tools `route` needs.

    outputs maps tool -> text printed by `<tool> --version`, or None if not installed.
    Returns {"ready": bool, "problems": [(tool, reason), ...]} sorted by tool,
    where reason is "missing", "unreadable" or "too old".
    """
    raise NotImplementedError
