import math


def _mul(sol, z, w, want, th, en):
    fn = sol.get("cmul")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน cmul", "Function cmul was not found")
    got = fn(z, w)
    if not isinstance(got, (tuple, list)) or len(got) != 2 or not all(math.isclose(p, q, abs_tol=1e-12) for p, q in zip(got, want)):
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("lesson", th="(3 + 2i)(1 + 4i) = -5 + 14i", en="(3 + 2i)(1 + 4i) = -5 + 14i")
def _(sol):
    _mul(sol, (3, 2), (1, 4), (-5, 14), "(3 + 2i)(1 + 4i)", "(3 + 2i)(1 + 4i)")


@check("i-squared", th="i · i = -1", en="i · i = -1")
def _(sol):
    _mul(sol, (0, 1), (0, 1), (-1, 0), "i · i", "i · i")


@check("quarter-turn", th="(2 + i) · i = -1 + 2i: หมุน 90 องศา", en="(2 + i) · i = -1 + 2i: a 90-degree turn")
def _(sol):
    _mul(sol, (2, 1), (0, 1), (-1, 2), "(2 + i) · i", "(2 + i) · i")


@check("exercise-1", th="แบบฝึกหัดที่ 1: (2 + 3i)(4 - i) = 11 + 10i", en="Exercise 1: (2 + 3i)(4 - i) = 11 + 10i")
def _(sol):
    _mul(sol, (2, 3), (4, -1), (11, 10), "(2 + 3i)(4 - i)", "(2 + 3i)(4 - i)")
