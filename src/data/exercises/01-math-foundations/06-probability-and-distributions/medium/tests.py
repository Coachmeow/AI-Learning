import math

WEATHER = [[0.40, 0.10], [0.05, 0.45]]


def _run(sol, joint):
    fn = sol.get("analyze_joint")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน analyze_joint", "Function analyze_joint was not found")
    got = fn([list(r) for r in joint])
    if not isinstance(got, (tuple, list)) or len(got) != 3:
        raise Fail(f"ต้องคืน (px, py, independent) แต่ได้ {got!r}", f"Must return (px, py, independent), got {got!r}")
    return got


def _vec(got, want, th, en):
    if not isinstance(got, list) or len(got) != len(want) or not all(math.isclose(g, w, abs_tol=1e-9) for g, w in zip(got, want)):
        raise Fail(f"{th} ควรเป็น {want} แต่ได้ {got!r}", f"{en} should be {want}, got {got!r}")


def _loaded():
    a = [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]
    b = [0.25, 0.15, 0.15, 0.15, 0.15, 0.15]
    return [[x * y for y in b] for x in a], a, b


def _raises(sol, joint, th, en):
    fn = sol.get("analyze_joint")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน analyze_joint", "Function analyze_joint was not found")
    try:
        got = fn(joint)
    except ValueError:
        return
    raise Fail(f"{th} ต้อง raise ValueError แต่ได้ {got!r}", f"{en}, so it must raise ValueError; got {got!r}")


@check("weather", th="ตารางสภาพอากาศกับร่มในบทเรียน", en="The lesson's weather and umbrella table")
def _(sol):
    px, py, ind = _run(sol, WEATHER)
    _vec(px, [0.5, 0.5], "px (ผลรวมแถว)", "px (row sums)")
    _vec(py, [0.45, 0.55], "py (ผลรวมคอลัมน์)", "py (column sums)")
    if ind is not False:
        raise Fail(f"0.45 ≠ 0.50 * 0.55 จึงไม่เป็นอิสระ แต่ได้ {ind!r}", f"0.45 ≠ 0.50 * 0.55, so not independent; got {ind!r}")


@check("loaded-dice", th="ลูกเต๋าถ่วงน้ำหนักสองลูกที่เป็นอิสระต่อกัน", en="Two independent loaded dice")
def _(sol):
    joint, a, b = _loaded()
    px, py, ind = _run(sol, joint)
    _vec(px, a, "px", "px")
    _vec(py, b, "py", "py")
    if ind is not True:
        raise Fail(f"ทุกช่องเท่ากับผลคูณของส่วนขอบ จึงเป็นอิสระ แต่ได้ {ind!r}", f"Every cell is the product of its marginals, so independent; got {ind!r}")


@check("not-one", th="ตารางที่รวมได้ 0.9 ต้อง raise ValueError", en="A table adding up to 0.9 raises ValueError")
def _(sol):
    _raises(sol, [[0.4, 0.1], [0.1, 0.3]], "ตารางที่รวมได้ 0.9", "The table adds up to 0.9")


@check("off-diagonal", th="ช่องบนเส้นทแยงมุมตรงแต่ช่องอื่นไม่ตรง", en="Diagonal cells match but other cells don't", hidden=True)
def _(sol):
    joint = [[0.04, 0.09, 0.07], [0.03, 0.09, 0.18], [0.13, 0.12, 0.25]]
    px, py, ind = _run(sol, joint)
    if ind is not False:
        raise Fail(f"{joint}: ช่องบนเส้นทแยงมุมเท่ากับผลคูณของส่วนขอบ แต่ช่อง (0, 1) = 0.09 ส่วน px[0] * py[1] = 0.2 * 0.3 = 0.06 จึงไม่เป็นอิสระ แต่ได้ {ind!r}",
                   f"{joint}: the diagonal cells equal the products of their marginals, but cell (0, 1) = 0.09 while px[0] * py[1] = 0.2 * 0.3 = 0.06, so not independent; got {ind!r}")


@check("negative", th="ช่องที่ติดลบต้อง raise ValueError", en="A negative cell raises ValueError", hidden=True)
def _(sol):
    _raises(sol, [[0.6, -0.1], [0.2, 0.3]], "ตารางที่มีช่องติดลบ", "The table has a negative cell")


@check("rectangular", th="ตาราง 2x4 ที่เป็นอิสระ (เลขทศนิยมไม่เท่ากันพอดี)", en="An independent 2x4 table (floats don't match exactly)", hidden=True)
def _(sol):
    joint = [[0.03, 0.06, 0.09, 0.12], [0.07, 0.14, 0.21, 0.28]]
    px, py, ind = _run(sol, joint)
    _vec(px, [0.3, 0.7], "px", "px")
    _vec(py, [0.1, 0.2, 0.3, 0.4], "py", "py")
    if ind is not True:
        raise Fail(f"{joint}: ทุกช่องเท่ากับผลคูณของส่วนขอบภายใน 1e-9 จึงเป็นอิสระ แต่ได้ {ind!r} (ใช้ == กับเลขทศนิยมหรือเปล่า?)",
                   f"{joint}: every cell equals the product of its marginals to within 1e-9, so independent; got {ind!r} (comparing floats with ==?)")
