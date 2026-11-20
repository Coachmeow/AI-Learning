import math


def _solve(sol, U, b, want, th, en):
    fn = sol.get("back_substitution")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน back_substitution", "Function back_substitution was not found")
    got = fn([row[:] for row in U], list(b))
    if not isinstance(got, list) or len(got) != len(want) or not all(math.isclose(a, w, abs_tol=1e-9) for a, w in zip(got, want)):
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("two", th="ระบบ 2x2: 2x + y = 5, 3y = 3 ได้ [2, 1]", en="2x2 system: 2x + y = 5, 3y = 3 gives [2, 1]")
def _(sol):
    _solve(sol, [[2, 1], [0, 3]], [5, 3], [2.0, 1.0], "ระบบ 2x2", "2x2 system")


@check("lesson", th="U จากบทเรียน [[2,1,1],[0,1,1],[0,0,-2]] ได้ [1, 1, 2]", en="The lesson's U [[2,1,1],[0,1,1],[0,0,-2]] gives [1, 1, 2]")
def _(sol):
    _solve(sol, [[2, 1, 1], [0, 1, 1], [0, 0, -2]], [5, 3, -4], [1.0, 1.0, 2.0], "U ของบทเรียน", "The lesson's U")


@check("four", th="ระบบ 4x4 ที่ตัวทแยงมุมต่างกันทุกตัว", en="A 4x4 system with different diagonal entries")
def _(sol):
    U = [[2, -1, 3, 1], [0, 4, 1, -2], [0, 0, 5, 2], [0, 0, 0, 0.5]]
    _solve(sol, U, [7, 3, 12, 1], [0.775, 1.35, 1.6, 2.0], "ระบบ 4x4", "4x4 system")
