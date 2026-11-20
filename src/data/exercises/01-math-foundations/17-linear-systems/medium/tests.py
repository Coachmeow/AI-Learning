import math


def _fn(sol):
    fn = sol.get("cholesky")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน cholesky", "Function cholesky was not found")
    return fn


def _expect(sol, A, want, th, en):
    got = _fn(sol)([row[:] for row in A])
    ok = isinstance(got, list) and len(got) == len(want) and all(
        isinstance(r, list) and len(r) == len(w) and all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(r, w))
        for r, w in zip(got, want))
    if not ok:
        raise Fail(f"{th}: L ควรเป็น {want} แต่ได้ {got!r}", f"{en}: L should be {want}, got {got!r}")


def _raises(sol, A, th, en):
    try:
        got = _fn(sol)([row[:] for row in A])
    except ValueError:
        return
    except Exception as e:
        raise Fail(f"{th}: ควร raise ValueError แต่เกิด {type(e).__name__}: {e}", f"{en}: should raise ValueError, got {type(e).__name__}: {e}")
    raise Fail(f"{th}: ควร raise ValueError แต่คืน {got!r}", f"{en}: should raise ValueError, returned {got!r}")


@check("two", th="[[9, 3], [3, 5]] ได้ L = [[3, 0], [1, 2]]", en="[[9, 3], [3, 5]] gives L = [[3, 0], [1, 2]]")
def _(sol):
    _expect(sol, [[9, 3], [3, 5]], [[3.0, 0.0], [1.0, 2.0]], "เมทริกซ์ 2x2", "2x2 matrix")


@check("three", th="[[4, 2, 2], [2, 5, 3], [2, 3, 6]] ได้ L = [[2, 0, 0], [1, 2, 0], [1, 1, 2]]", en="[[4, 2, 2], [2, 5, 3], [2, 3, 6]] gives L = [[2, 0, 0], [1, 2, 0], [1, 1, 2]]")
def _(sol):
    _expect(sol, [[4, 2, 2], [2, 5, 3], [2, 3, 6]], [[2.0, 0.0, 0.0], [1.0, 2.0, 0.0], [1.0, 1.0, 2.0]], "เมทริกซ์ 3x3", "3x3 matrix")


@check("rebuild", th="L·Lᵀ ประกอบกลับเป็น A ของเมทริกซ์ 5x5", en="L·Lᵀ rebuilds A for a 5x5 matrix")
def _(sol):
    B = [[(i * 7 + j * 3) % 5 - 2 for j in range(5)] for i in range(5)]
    A = [[sum(B[i][k] * B[j][k] for k in range(5)) + (5 if i == j else 0) for j in range(5)] for i in range(5)]
    L = _fn(sol)([row[:] for row in A])
    if not isinstance(L, list) or len(L) != 5 or any(not isinstance(r, list) or len(r) != 5 for r in L):
        raise Fail(f"ต้องคืน list ของ list ขนาด 5x5 แต่ได้ {L!r}", f"Must return a 5x5 list of lists, got {L!r}")
    if any(L[i][j] != 0 for i in range(5) for j in range(i + 1, 5)):
        raise Fail("L ต้องเป็นสามเหลี่ยมล่าง (เหนือเส้นทแยงมุมเป็น 0)", "L must be lower triangular (zeros above the diagonal)")
    for i in range(5):
        for j in range(5):
            v = sum(L[i][k] * L[j][k] for k in range(5))
            if not math.isclose(v, A[i][j], abs_tol=1e-9):
                raise Fail(f"(L·Lᵀ)[{i}][{j}] = {v} แต่ A[{i}][{j}] = {A[i][j]}", f"(L·Lᵀ)[{i}][{j}] = {v} but A[{i}][{j}] = {A[i][j]}")


@check("not-symmetric", th="เมทริกซ์ไม่สมมาตร [[4, 1], [3, 5]] ต้อง raise ValueError", en="The non-symmetric [[4, 1], [3, 5]] must raise ValueError")
def _(sol):
    _raises(sol, [[4, 1], [3, 5]], "เมทริกซ์ไม่สมมาตร", "Non-symmetric matrix")


@check("indefinite", th="[[1, 2], [2, 1]] (ค่าลักษณะเฉพาะ 3 และ -1) ต้อง raise ValueError", en="[[1, 2], [2, 1]] (eigenvalues 3 and -1) must raise ValueError")
def _(sol):
    _raises(sol, [[1, 2], [2, 1]], "เมทริกซ์ไม่บวกแน่นอน", "Indefinite matrix")


@check("singular", th="[[1, 1], [1, 1]] มี pivot เป็นศูนย์พอดี ต้อง raise ValueError", en="[[1, 1], [1, 1]] has a pivot of exactly zero and must raise ValueError")
def _(sol):
    _raises(sol, [[1, 1], [1, 1]], "pivot เป็นศูนย์", "Zero pivot")
