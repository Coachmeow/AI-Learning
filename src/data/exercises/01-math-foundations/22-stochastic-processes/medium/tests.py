import math


def _fn(sol):
    fn = sol.get("stationary_distribution")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน stationary_distribution", "Function stationary_distribution was not found")
    return fn


def _expect(sol, P, want, th, en, **kw):
    got = _fn(sol)(P, **kw)
    if not isinstance(got, list) or len(got) != len(want) or not all(math.isclose(a, b, abs_tol=1e-8) for a, b in zip(got, want)):
        raise Fail(f"{th}: ควรได้ {[round(w, 6) for w in want]} แต่ได้ {got!r}", f"{en}: should be {[round(w, 6) for w in want]}, got {got!r}")


def _raises(sol, exc, P, th, en, **kw):
    try:
        got = _fn(sol)(P, **kw)
    except exc:
        return
    except Exception as e:
        raise Fail(f"{th}: ควร raise {exc.__name__} แต่เกิด {type(e).__name__}: {e}", f"{en}: should raise {exc.__name__}, got {type(e).__name__}: {e}")
    raise Fail(f"{th}: ควร raise {exc.__name__} แต่คืน {got!r}", f"{en}: should raise {exc.__name__}, returned {got!r}")


@check("weather", th="ลูกโซ่สภาพอากาศได้ [6/11, 2/11, 3/11]", en="The weather chain gives [6/11, 2/11, 3/11]")
def _(sol):
    _expect(sol, [[0.7, 0.1, 0.2], [0.3, 0.4, 0.3], [0.4, 0.2, 0.4]], [6 / 11, 2 / 11, 3 / 11], "สภาพอากาศ", "Weather")


@check("two-state", th="[[0.9, 0.1], [0.3, 0.7]] ได้ [0.75, 0.25]", en="[[0.9, 0.1], [0.3, 0.7]] gives [0.75, 0.25]")
def _(sol):
    _expect(sol, [[0.9, 0.1], [0.3, 0.7]], [0.75, 0.25], "สองสถานะ", "Two states")


@check("bad-row", th="แถวที่รวมได้ 0.9 ต้อง raise ValueError", en="A row summing to 0.9 must raise ValueError")
def _(sol):
    _raises(sol, ValueError, [[0.5, 0.4], [0.3, 0.7]], "แถวรวมไม่เท่ากับ 1", "Row does not sum to 1")


@check("column-stochastic", th="เมทริกซ์ที่คอลัมน์รวมได้ 1 แต่แถวไม่ใช่ ต้อง raise ValueError", en="A matrix whose columns sum to 1 but rows do not must raise ValueError")
def _(sol):
    _raises(sol, ValueError, [[0.9, 0.3], [0.1, 0.7]], "รวมตามคอลัมน์", "Column sums")


@check("negative", th="ช่องที่ติดลบต้อง raise ValueError แม้แถวจะรวมได้ 1", en="A negative entry must raise ValueError even if the row sums to 1", hidden=True)
def _(sol):
    _raises(sol, ValueError, [[1.2, -0.2], [0.5, 0.5]], "ความน่าจะเป็นติดลบ", "Negative probability")


@check("slow", th="ลูกโซ่ที่ผสมช้า [[0.99, 0.01], [0.02, 0.98]] ได้ [2/3, 1/3]", en="The slowly mixing chain [[0.99, 0.01], [0.02, 0.98]] gives [2/3, 1/3]", hidden=True)
def _(sol):
    _expect(sol, [[0.99, 0.01], [0.02, 0.98]], [2 / 3, 1 / 3], "ผสมช้า", "Slow mixing")


@check("periodic", th="ลูกโซ่เป็นคาบที่ไม่ลู่เข้าจากการแจกแจงสม่ำเสมอต้อง raise RuntimeError", en="A periodic chain that never settles from the uniform start must raise RuntimeError", hidden=True)
def _(sol):
    _raises(sol, RuntimeError, [[0, 1, 0], [0.5, 0, 0.5], [0, 1, 0]], "ลูกโซ่เป็นคาบ", "Periodic chain", max_iter=1000)
