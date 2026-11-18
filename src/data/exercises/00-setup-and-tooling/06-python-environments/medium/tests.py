NUMPY = ["1.24.0", "1.26.4", "2.0.0", "2.1.3"]


def _fn(sol):
    fn = sol.get("pick_version")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน pick_version", "Function pick_version was not found")
    return fn


def _expect(fn, available, spec, want):
    got = fn(list(available), spec)
    if got != want:
        raise Fail(f"pick_version({available}, {spec!r}) ควรได้ {want!r} แต่ได้ {got!r}", f"pick_version({available}, {spec!r}) should be {want!r}, got {got!r}")


@check("range", th="เลือกตัวใหม่ที่สุดในช่วง >=1.26, <2", en="Picks the newest in the range >=1.26, <2")
def _(sol):
    _expect(_fn(sol), NUMPY, ">=1.26, <2", "1.26.4")


@check("open", th="spec ว่างได้เวอร์ชันใหม่ที่สุด", en="An empty spec gives the newest version")
def _(sol):
    _expect(_fn(sol), NUMPY, "", "2.1.3")


@check("exclude", th="!= ตัดเวอร์ชันนั้นทิ้ง", en="!= excludes that version")
def _(sol):
    _expect(_fn(sol), NUMPY, ">=2,!=2.1.3", "2.0.0")


@check("none", th="ไม่มีตัวไหนตรงได้ None", en="Returns None when nothing matches")
def _(sol):
    _expect(_fn(sol), NUMPY, ">=3", None)


@check("numeric", th="เทียบเป็นตัวเลข: 1.10.0 ใหม่กว่า 1.9.2", en="Compares numbers: 1.10.0 is newer than 1.9.2")
def _(sol):
    _expect(_fn(sol), ["1.9.2", "1.10.0", "1.2.0"], ">=1", "1.10.0")
