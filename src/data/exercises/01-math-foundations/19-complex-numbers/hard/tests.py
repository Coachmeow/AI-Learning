import math


def _fn(sol, name):
    fn = sol.get(name)
    if fn is None:
        raise Fail(f"ไม่พบฟังก์ชัน {name}", f"Function {name} was not found")
    return fn


def _vec(sol, vec, pos, want, th, en, **kw):
    got = _fn(sol, "rope")(list(vec), pos, **kw)
    if not isinstance(got, list) or len(got) != len(want) or not all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(got, want)):
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


def _score(sol, m, n, want, th, en):
    got = _fn(sol, "rope_score")(list(_Q), list(_K), m, n)
    if not isinstance(got, (int, float)) or not math.isclose(got, want, abs_tol=1e-9):
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


_Q = [0.5, -1.0, 2.0, 0.25, -0.75, 1.5]
_K = [1.0, 0.5, -0.5, 1.25, 0.3, -2.0]


@check("identity", th="pos = 0 ไม่เปลี่ยนเวกเตอร์", en="pos = 0 leaves the vector unchanged")
def _(sol):
    _vec(sol, [0.5, -1.0, 2.0, 0.25], 0, [0.5, -1.0, 2.0, 0.25], "pos = 0", "pos = 0")


@check("quarter-turn", th="[1, 0] ที่ pos = π/2 ได้ [0, 1] (ทวนเข็มนาฬิกา)", en="[1, 0] at pos = π/2 gives [0, 1] (counterclockwise)")
def _(sol):
    _vec(sol, [1.0, 0.0], math.pi / 2, [0.0, 1.0], "หมุนหนึ่งในสี่รอบ", "Quarter turn")


@check("frequencies", th="d = 4, base = 100, pos = 2: คู่แรกหมุน 2 rad คู่ที่สองหมุน 0.2 rad", en="d = 4, base = 100, pos = 2: the first pair turns 2 rad, the second 0.2 rad")
def _(sol):
    want = [math.cos(2), math.sin(2), math.cos(0.2), math.sin(0.2)]
    _vec(sol, [1.0, 0.0, 1.0, 0.0], 2, want, "ความถี่ของแต่ละคู่", "Per-pair frequencies", base=100.0)


@check("score", th="rope_score(q, k, 3, 0) ≈ -3.358247", en="rope_score(q, k, 3, 0) ≈ -3.358247")
def _(sol):
    _score(sol, 3, 0, -3.3582466723986593, "m = 3, n = 0", "m = 3, n = 0")


@check("relative", th="คะแนนขึ้นกับ m - n เท่านั้น: (13, 10) เท่ากับ (3, 0)", en="The score depends only on m - n: (13, 10) equals (3, 0)")
def _(sol):
    _score(sol, 13, 10, -3.3582466723986593, "m = 13, n = 10", "m = 13, n = 10")
    _score(sol, 0, 3, -4.4533095672659915, "m = 0, n = 3 (ทิศกลับกัน)", "m = 0, n = 3 (the other direction)")


@check("same-position", th="m = n ได้ผลคูณจุดเดิม q · k = -3.9125", en="m = n gives the plain dot product q · k = -3.9125", hidden=True)
def _(sol):
    _score(sol, 7, 7, -3.9125, "m = n = 7", "m = n = 7")


@check("base", th="ใช้ base ที่รับเข้ามา: [0, 1, 0, 1] ที่ pos = 3, base = 4", en="Uses the given base: [0, 1, 0, 1] at pos = 3, base = 4", hidden=True)
def _(sol):
    want = [-math.sin(3), math.cos(3), -math.sin(1.5), math.cos(1.5)]
    _vec(sol, [0.0, 1.0, 0.0, 1.0], 3, want, "base = 4", "base = 4", base=4.0)


@check("norm", th="การหมุนรักษาความยาวของเวกเตอร์ 8 มิติที่ pos = 1000", en="The rotation preserves the length of an 8D vector at pos = 1000", hidden=True)
def _(sol):
    v = [0.3, -1.2, 2.5, 0.7, -0.4, 1.1, 0.9, -2.2]
    got = _fn(sol, "rope")(list(v), 1000)
    n0 = math.sqrt(sum(x * x for x in v))
    n1 = math.sqrt(sum(x * x for x in got)) if isinstance(got, list) and len(got) == 8 else float("nan")
    if not math.isclose(n0, n1, abs_tol=1e-9):
        raise Fail(f"ความยาวเปลี่ยนจาก {n0} เป็น {n1}", f"The length changed from {n0} to {n1}")


@check("bad-length", th="ความยาวคี่หรือศูนย์ต้อง raise ValueError", en="An odd or zero length must raise ValueError", hidden=True)
def _(sol):
    for v in ([1.0, 2.0, 3.0], []):
        try:
            got = _fn(sol, "rope")(v, 1)
        except ValueError:
            continue
        except Exception as e:
            raise Fail(f"ความยาว {len(v)}: ควร raise ValueError แต่เกิด {type(e).__name__}", f"Length {len(v)}: should raise ValueError, got {type(e).__name__}")
        raise Fail(f"ความยาว {len(v)}: ควร raise ValueError แต่คืน {got!r}", f"Length {len(v)}: should raise ValueError, returned {got!r}")


@check("no-mutation", th="ไม่แก้ไข vec ที่รับเข้ามา", en="Does not modify the vec it receives", hidden=True)
def _(sol):
    v = [1.0, 0.0, 0.5, 0.5]
    _fn(sol, "rope")(v, 2)
    if v != [1.0, 0.0, 0.5, 0.5]:
        raise Fail(f"vec ถูกแก้เป็น {v}", f"vec was modified to {v}")
