import math


def _is(sol, xs, want):
    fn = sol.get("median")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน median", "Function median was not found")
    got = fn(list(xs))
    if not isinstance(got, (int, float)) or not math.isclose(got, want):
        raise Fail(f"median({list(xs)}) ควรเป็น {want} แต่ได้ {got!r}", f"median({list(xs)}) should be {want}, got {got!r}")


@check("odd", th="จำนวนคี่ที่มีค่าผิดปกติ: [1, 2, 3, 4, 1000] ได้ 3", en="An odd count with an outlier: [1, 2, 3, 4, 1000] gives 3")
def _(sol):
    _is(sol, [1, 2, 3, 4, 1000], 3)


@check("even", th="จำนวนคู่: [7, 1, 3, 5] ได้ 4", en="An even count: [7, 1, 3, 5] gives 4")
def _(sol):
    _is(sol, [7, 1, 3, 5], 4.0)


@check("unsorted-even", th="ไม่เรียงและเป็นจำนวนคู่: [10, 2, 8, 4, 6, 12] ได้ 7", en="Unsorted, even count: [10, 2, 8, 4, 6, 12] gives 7")
def _(sol):
    _is(sol, [10, 2, 8, 4, 6, 12], 7.0)
    _is(sol, [2.5], 2.5)
