import math


def _fn(sol):
    fn = sol.get("closest_point")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน closest_point", "Function closest_point was not found")
    return fn


def _expect(sol, c, a, b, want_x, want_lam, th, en):
    got = _fn(sol)(list(c), list(a), b)
    if not isinstance(got, (tuple, list)) or len(got) != 2:
        raise Fail(f"ต้องคืน (x, lam) แต่ได้ {got!r}", f"Must return (x, lam), got {got!r}")
    x, lam = got
    if not isinstance(x, list) or len(x) != len(want_x) or not all(math.isclose(p, q, abs_tol=1e-9) for p, q in zip(x, want_x)):
        raise Fail(f"{th}: x ควรเป็น {want_x} แต่ได้ {x!r}", f"{en}: x should be {want_x}, got {x!r}")
    if not isinstance(lam, (int, float)) or not math.isclose(lam, want_lam, abs_tol=1e-9):
        raise Fail(f"{th}: lam ควรเป็น {want_lam} แต่ได้ {lam!r}", f"{en}: lam should be {want_lam}, got {lam!r}")


@check("lesson", th="ตัวอย่างในบทเรียน: x + y = 1 ใกล้จุดกำเนิดที่สุดที่ (0.5, 0.5), lam = -1", en="The lesson's example: the point of x + y = 1 closest to the origin is (0.5, 0.5), lam = -1")
def _(sol):
    _expect(sol, [0, 0], [1, 1], 1, [0.5, 0.5], -1.0, "x + y = 1", "x + y = 1")


@check("exercise-3", th="แบบฝึกหัดที่ 3: c = (3, 3), x + 2y = 4 ได้ (2, 1), lam = 2", en="Exercise 3: c = (3, 3), x + 2y = 4 gives (2, 1), lam = 2")
def _(sol):
    _expect(sol, [3, 3], [1, 2], 4, [2.0, 1.0], 2.0, "x + 2y = 4", "x + 2y = 4")


@check("three-d", th="3 มิติ: c = (1, 2, 3) บนระนาบ x + y + z = 0 ได้ (-1, 0, 1), lam = 4", en="3D: c = (1, 2, 3) on the plane x + y + z = 0 gives (-1, 0, 1), lam = 4")
def _(sol):
    _expect(sol, [1, 2, 3], [1, 1, 1], 0, [-1.0, 0.0, 1.0], 4.0, "x + y + z = 0", "x + y + z = 0")


@check("on-plane", th="ถ้า c อยู่บนไฮเปอร์เพลนแล้ว ได้ x = c และ lam = 0 (ข้อจำกัดไม่ต้องดึง)", en="If c is already on the hyperplane, x = c and lam = 0 (the constraint has nothing to pull)")
def _(sol):
    _expect(sol, [1, 1], [1, 1], 2, [1.0, 1.0], 0.0, "c อยู่บนเส้นแล้ว", "c already on the line")


@check("zero-a", th="a = (0, 0) ต้อง raise ValueError", en="a = (0, 0) must raise ValueError")
def _(sol):
    try:
        got = _fn(sol)([1, 2], [0, 0], 3)
    except ValueError:
        return
    except Exception as e:
        raise Fail(f"ควร raise ValueError แต่เกิด {type(e).__name__}: {e}", f"Should raise ValueError, got {type(e).__name__}: {e}")
    raise Fail(f"ควร raise ValueError แต่คืน {got!r}", f"Should raise ValueError, returned {got!r}")


@check("no-mutation", th="ไม่แก้ไข c และ a ที่รับเข้ามา", en="Does not modify the c and a it receives", hidden=True)
def _(sol):
    c, a = [3.0, 3.0], [1.0, 2.0]
    _fn(sol)(c, a, 4)
    if c != [3.0, 3.0] or a != [1.0, 2.0]:
        raise Fail(f"c หรือ a ถูกแก้: c = {c}, a = {a}", f"c or a was modified: c = {c}, a = {a}")
