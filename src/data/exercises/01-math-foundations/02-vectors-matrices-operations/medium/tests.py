def _fn(sol):
    fn = sol.get("determinant")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน determinant", "Function determinant was not found")
    return fn


def _expect(sol, M, want):
    got = _fn(sol)([list(r) for r in M])
    if got != want:
        raise Fail(f"determinant({M}) ควรได้ {want} แต่ได้ {got!r}", f"determinant({M}) should be {want}, got {got!r}")


@check("small", th="เมทริกซ์ 1x1 และ 2x2", en="1x1 and 2x2 matrices")
def _(sol):
    _expect(sol, [[7]], 7)
    _expect(sol, [[1, 2], [3, 4]], -2)


@check("three", th="เมทริกซ์ 3x3 (เครื่องหมายสลับกัน)", en="A 3x3 matrix (alternating signs)")
def _(sol):
    _expect(sol, [[2, 0, 1], [1, 3, 2], [1, 1, 1]], 0)
    _expect(sol, [[6, 1, 1], [4, -2, 5], [2, 8, 7]], -306)


@check("singular", th="แถวที่ขึ้นต่อกันได้ดีเทอร์มิแนนต์ 0", en="Dependent rows give a determinant of 0")
def _(sol):
    _expect(sol, [[1, 2, 3], [2, 4, 6], [1, 0, 1]], 0)


@check("four", th="เมทริกซ์ 4x4", en="A 4x4 matrix")
def _(sol):
    _expect(sol, [[1, 0, 2, -1], [3, 0, 0, 5], [2, 1, 4, -3], [1, 0, 5, 0]], 30)


@check("not-square", th="เมทริกซ์ที่ไม่ใช่จัตุรัสต้อง raise ValueError", en="A non-square matrix raises ValueError")
def _(sol):
    try:
        _fn(sol)([[1, 2, 3], [4, 5, 6]])
    except ValueError:
        return
    raise Fail("เมทริกซ์ 2x3 ต้อง raise ValueError", "A 2x3 matrix must raise ValueError")
