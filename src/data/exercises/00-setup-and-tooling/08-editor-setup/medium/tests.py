SETTINGS = """{
    // Type checking catches wrong argument types before you run
    "python.analysis.typeCheckingMode": "basic",
    "editor.formatOnSave": true,
    /* Black wraps at 88; the 120 marker is for comments */
    "editor.rulers": [88, 120,],
    "files.autoSave": "afterDelay",
}
"""


def _fn(sol):
    fn = sol.get("load_jsonc")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน load_jsonc", "Function load_jsonc was not found")
    return fn


def _expect(sol, text, want, th, en):
    try:
        got = _fn(sol)(text)
    except Exception as e:  # noqa: BLE001
        raise Fail(f"{th}: เกิด {type(e).__name__}: {e}", f"{en}: raised {type(e).__name__}: {e}")
    if got != want:
        raise Fail(f"{th}: ควรได้ {want!r} แต่ได้ {got!r}", f"{en}: should be {want!r}, got {got!r}")


@check("lesson", th="อ่านการตั้งค่าของบทเรียนที่มีคอมเมนต์และจุลภาคท้ายได้", en="Reads the lesson's settings with comments and trailing commas")
def _(sol):
    _expect(sol, SETTINGS, {
        "python.analysis.typeCheckingMode": "basic",
        "editor.formatOnSave": True,
        "editor.rulers": [88, 120],
        "files.autoSave": "afterDelay",
    }, "settings.json ของบทเรียน", "The lesson's settings.json")


@check("url", th="ไม่ตัด // ที่อยู่ในสตริง", en="Keeps // inside strings")
def _(sol):
    _expect(sol, '{"docs": "https://code.visualstudio.com/docs", // where to read\n "n": 1}', {"docs": "https://code.visualstudio.com/docs", "n": 1}, "URL ในสตริง", "A URL in a string")


@check("string-comma", th="ไม่แตะจุลภาคและวงเล็บในสตริง", en="Leaves commas and brackets inside strings alone")
def _(sol):
    _expect(sol, '{"label": "a, }", "list": ["x", "y",]}', {"label": "a, }", "list": ["x", "y"]}, "จุลภาคในสตริง", "A comma inside a string")


@check("escaped-quote", th="รับมือกับ \\\" ในสตริงได้", en="Copes with \\\" inside strings")
def _(sol):
    _expect(sol, '{"say": "he said \\"hi // there\\"", "ok": true,}', {"say": 'he said "hi // there"', "ok": True}, "เครื่องหมายคำพูดที่ escape", "An escaped quote")
