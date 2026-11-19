def _fn(sol):
    fn = sol.get("matmul")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน matmul", "Function matmul was not found")
    return fn


def _expect(sol, A, B, want):
    got = _fn(sol)(A, B)
    if got != want:
        raise Fail(f"matmul({A}, {B}) ควรได้ {want} แต่ได้ {got!r}", f"matmul({A}, {B}) should be {want}, got {got!r}")


@check("lesson", th="ตัวอย่างในบทเรียนได้ [[19, 22], [43, 50]]", en="The lesson's example gives [[19, 22], [43, 50]]")
def _(sol):
    _expect(sol, [[1, 2], [3, 4]], [[5, 6], [7, 8]], [[19, 22], [43, 50]])


@check("shape", th="(2 x 3) @ (3 x 1) ได้ผลขนาด 2 x 1", en="(2 x 3) @ (3 x 1) gives a 2 x 1 result")
def _(sol):
    _expect(sol, [[1, 0, 2], [0, 1, -1]], [[3], [4], [5]], [[13], [-1]])


@check("non-square", th="(1 x 2) @ (2 x 3) ได้ 1 x 3", en="(1 x 2) @ (2 x 3) gives 1 x 3")
def _(sol):
    _expect(sol, [[2, 3]], [[1, 0, -1], [0, 1, 2]], [[2, 3, 4]])


@check("mismatch", th="มิติด้านในไม่ตรงต้อง raise ValueError", en="Mismatched inner dimensions raise ValueError")
def _(sol):
    try:
        _fn(sol)([[1, 2]], [[1, 2]])
    except ValueError:
        return
    raise Fail("(1 x 2) @ (1 x 2) ต้อง raise ValueError", "(1 x 2) @ (1 x 2) must raise ValueError")
