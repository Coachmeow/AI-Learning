OK = {
    "python": "Python 3.12.4",
    "git": "git version 2.43.0",
    "numpy": "2.1.3",
    "node": "v22.11.0",
    "pnpm": "9.12.3",
    "rustc": "rustc 1.82.0 (f6e511eec 2024-10-15)",
    "cargo": "cargo 1.82.0 (8f40fc59f 2024-08-21)",
}


def _fn(sol):
    fn = sol.get("preflight")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน preflight", "Function preflight was not found")
    return fn


def _expect(sol, route, outputs, problems):
    got = _fn(sol)(route, outputs)
    want = {"ready": not problems, "problems": problems}
    if not isinstance(got, dict) or got.get("ready") != want["ready"] or list(got.get("problems", [])) != problems:
        raise Fail(
            f"preflight({route!r}, ...) ควรได้ {want} แต่ได้ {got!r}",
            f"preflight({route!r}, ...) should return {want}, got {got!r}",
        )


def _with(**changes):
    out = dict(OK)
    for tool, text in changes.items():
        if text == "<absent>":
            out.pop(tool, None)
        else:
            out[tool] = text
    return out


@check("ready", th="ทุกอย่างพร้อม ได้ ready = True และไม่มีปัญหา", en="Everything installed gives ready = True and no problems")
def _(sol):
    _expect(sol, "beginner", _with(), [])
    _expect(sol, "agents", _with(), [])


@check("missing", th="รายงานเครื่องมือที่ไม่ได้ติดตั้ง (None หรือไม่มีใน outputs)", en="Reports tools that are not installed (None or absent)")
def _(sol):
    _expect(sol, "agents", _with(node=None, pnpm="<absent>"), [("node", "missing"), ("pnpm", "missing")])


@check("too-old", th="รายงานเครื่องมือที่เก่ากว่าขั้นต่ำ", en="Reports tools below the minimum version")
def _(sol):
    _expect(sol, "agents", _with(node="v18.19.0"), [("node", "too old")])


@check("unrelated", th="ไม่รายงานเครื่องมือที่เส้นทางนี้ไม่ได้ใช้", en="Ignores tools the route does not use")
def _(sol):
    _expect(sol, "beginner", _with(rustc=None, node=None, cargo="<absent>"), [])


@check("unknown-route", th="ชื่อเส้นทางที่ไม่รู้จักต้อง raise ValueError", en="An unknown route raises ValueError")
def _(sol):
    try:
        got = _fn(sol)("gpu-wizard", _with())
    except ValueError:
        return
    raise Fail(f"เส้นทาง 'gpu-wizard' ไม่มีใน ROUTES ต้อง raise ValueError แต่ได้ {got!r}", f"'gpu-wizard' is not in ROUTES and must raise ValueError, got {got!r}")


@check("numeric", th="เทียบเวอร์ชันเป็นตัวเลข (3.9 เก่ากว่า 3.11)", en="Compares versions as numbers (3.9 is older than 3.11)", hidden=True)
def _(sol):
    _expect(sol, "beginner", _with(python="Python 3.9.18"), [("python", "too old")])
    _expect(sol, "beginner", _with(python="Python 3.11.0"), [])


@check("unreadable", th="ข้อความที่ไม่มีเลขเวอร์ชันนับเป็น unreadable", en="Text without a version number counts as unreadable", hidden=True)
def _(sol):
    _expect(sol, "beginner", _with(git="git: command not found"), [("git", "unreadable")])


@check("sorted", th="เรียงปัญหาตามชื่อเครื่องมือ", en="Problems are sorted by tool name", hidden=True)
def _(sol):
    _expect(sol, "systems", _with(rustc="rustc 1.70.0 (90c541806 2023-05-31)", cargo=None), [("cargo", "missing"), ("rustc", "too old")])


@check("padding", th="ขั้นต่ำที่มีหลายส่วนกว่า เช่น (3, 11, 0) ยังเทียบถูก", en="Minimums with more parts, like (3, 11, 0), still compare correctly", hidden=True)
def _(sol):
    routes = sol.get("ROUTES")
    if not isinstance(routes, dict):
        raise Fail("ใช้ตัวแปร ROUTES จาก starter", "Use the ROUTES variable from the starter")
    routes["exact"] = {"python": (3, 11, 0)}
    try:
        _expect(sol, "exact", _with(python="Python 3.11"), [])
    finally:
        routes.pop("exact", None)
