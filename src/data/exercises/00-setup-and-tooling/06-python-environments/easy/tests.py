def _fn(sol):
    fn = sol.get("satisfies")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน satisfies", "Function satisfies was not found")
    return fn


def _expect(fn, version, clause, want):
    got = fn(version, clause)
    if got is not want:
        raise Fail(f"satisfies({version!r}, {clause!r}) ควรได้ {want} แต่ได้ {got!r}", f"satisfies({version!r}, {clause!r}) should be {want}, got {got!r}")


@check("at-least", th=">= ยอมรับเวอร์ชันที่เท่ากันหรือใหม่กว่า", en=">= accepts equal or newer versions")
def _(sol):
    fn = _fn(sol)
    _expect(fn, "1.26.4", ">=1.26", True)
    _expect(fn, "1.26", ">=1.26", True)
    _expect(fn, "1.24.0", ">=1.26", False)


@check("below", th="< และ <= ทำงานถูกทิศ", en="< and <= point the right way")
def _(sol):
    fn = _fn(sol)
    _expect(fn, "1.26.4", "<2", True)
    _expect(fn, "2.0.0", "<2", False)
    _expect(fn, "2.0", "<=2.0", True)
    _expect(fn, "2.0.1", "<=2.0", False)


@check("equal", th="== และ != เทียบเป็นตัวเลข (2.0 เท่ากับ 2.0.0)", en="== and != compare numbers (2.0 equals 2.0.0)")
def _(sol):
    fn = _fn(sol)
    _expect(fn, "2.0.0", "==2.0", True)
    _expect(fn, "1.26.4", "==1.26.4", True)
    _expect(fn, "2.0", "!=2.0.0", False)
    _expect(fn, "2.1", "!=2.0", True)


@check("strict", th="> เข้มงวด: เวอร์ชันที่เท่ากันไม่ผ่าน", en="> is strict: an equal version does not pass")
def _(sol):
    fn = _fn(sol)
    _expect(fn, "2.3", ">2.3", False)
    _expect(fn, "2.3.1", ">2.3", True)


@check("numeric", th="1.10 ใหม่กว่า 1.9", en="1.10 is newer than 1.9")
def _(sol):
    _expect(_fn(sol), "1.10.0", ">=1.9", True)
