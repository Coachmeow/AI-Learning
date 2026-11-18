def _fn(sol):
    fn = sol.get("parse_version")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน parse_version", "Function parse_version was not found")
    return fn


def _expect(fn, text, want):
    got = fn(text)
    if got != want or not all(type(x) is int for x in (got or ())):
        raise Fail(
            f"parse_version({text!r}) ควรได้ {want} (tuple ของ int) แต่ได้ {got!r}",
            f"parse_version({text!r}) should be {want} (a tuple of ints), got {got!r}",
        )


@check("python", th="อ่านผลของ python3 --version ได้", en="Reads the output of python3 --version")
def _(sol):
    _expect(_fn(sol), "Python 3.12.4", (3, 12, 4))


@check("node", th="อ่านเวอร์ชันที่มี v นำหน้าได้ (node --version)", en="Reads a version with a leading v (node --version)")
def _(sol):
    _expect(_fn(sol), "v22.11.0", (22, 11, 0))


@check("rustc", th="ไม่สับสนกับ hash และวันที่ (rustc --version)", en="Is not confused by the hash and date (rustc --version)")
def _(sol):
    _expect(_fn(sol), "rustc 1.82.0 (f6e511eec 2024-10-15)", (1, 82, 0))
    _expect(_fn(sol), "julia version 1.11.1", (1, 11, 1))


@check("first", th="เลือกเลขเวอร์ชันชุดแรก ไม่ใช่ชุดสุดท้าย", en="Takes the first version number, not the last")
def _(sol):
    _expect(_fn(sol), "Python 3.12.4 (main, Jun  6 2024) [Clang 15.0.0]", (3, 12, 4))


@check("none", th="ไม่พบเลขเวอร์ชันแล้ว raise ValueError", en="Raises ValueError when there is no version number")
def _(sol):
    try:
        got = _fn(sol)("bash: node: command not found")
    except ValueError:
        return
    raise Fail(f"ข้อความที่ไม่มีเลขเวอร์ชันต้อง raise ValueError แต่ได้ {got!r}", f"Text without a version number must raise ValueError, got {got!r}")
