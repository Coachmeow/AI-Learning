import math


def _fn(sol):
    fn = sol.get("inverse")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน inverse", "Function inverse was not found")
    return fn


def _close(got, want, label_th, label_en):
    ok = isinstance(got, list) and len(got) == len(want) and all(
        len(g) == len(w) and all(math.isclose(x, y, abs_tol=1e-9) for x, y in zip(g, w)) for g, w in zip(got, want))
    if not ok:
        raise Fail(f"{label_th}: ควรได้ {want} แต่ได้ {got!r}", f"{label_en}: should be {want}, got {got!r}")


def _mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def _singular(sol, M, th, en):
    try:
        got = _fn(sol)([list(r) for r in M])
    except ValueError:
        return
    raise Fail(f"{th} เป็นเอกฐาน ต้อง raise ValueError แต่ได้ {got!r}", f"{en} is singular and must raise ValueError, got {got!r}")


@check("two", th="เมทริกซ์ 2x2 จากบทเรียน", en="The lesson's 2x2 matrix")
def _(sol):
    _close(_fn(sol)([[1, 2], [3, 4]]), [[-2, 1], [1.5, -0.5]], "[[1, 2], [3, 4]]", "[[1, 2], [3, 4]]")


@check("identity-check", th="A @ inverse(A) ได้เมทริกซ์เอกลักษณ์ (3x3)", en="A @ inverse(A) gives the identity (3x3)")
def _(sol):
    A = [[2, -1, 0], [-1, 2, -1], [0, -1, 2]]
    _close(_mul(A, _fn(sol)(A)), [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "A @ inverse(A)", "A @ inverse(A)")


@check("zero-pivot", th="ช่องบนเส้นทแยงมุมเป็นศูนย์ต้องสลับแถว", en="A zero on the diagonal needs a row swap")
def _(sol):
    _close(_fn(sol)([[0, 1], [1, 0]]), [[0, 1], [1, 0]], "[[0, 1], [1, 0]]", "[[0, 1], [1, 0]]")


@check("singular", th="เมทริกซ์เอกฐานต้อง raise ValueError", en="A singular matrix raises ValueError")
def _(sol):
    _singular(sol, [[1, 2], [2, 4]], "[[1, 2], [2, 4]]", "[[1, 2], [2, 4]]")


@check("float-singular", th="เอกฐานแม้เลขทศนิยมไม่ให้ศูนย์พอดี", en="Singular even when floating point gives no exact zero", hidden=True)
def _(sol):
    _singular(sol, [[0.1, 0.3], [0.3, 0.9]], "[[0.1, 0.3], [0.3, 0.9]]", "[[0.1, 0.3], [0.3, 0.9]]")


@check("four", th="เมทริกซ์ 4x4", en="A 4x4 matrix", hidden=True)
def _(sol):
    A = [[4, 7, 2, 0], [3, 6, 1, 1], [2, 5, 3, 2], [1, 0, 2, 5]]
    _close(_mul(A, _fn(sol)(A)), [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], "4x4", "4x4")


@check("no-mutation", th="ไม่แก้เมทริกซ์ที่ส่งเข้ามา", en="Leaves the input matrix unchanged", hidden=True)
def _(sol):
    A = [[0, 1], [1, 0]]
    _fn(sol)(A)
    if A != [[0, 1], [1, 0]]:
        raise Fail(f"เมทริกซ์ที่ส่งเข้ามาถูกแก้เป็น {A}", f"The input matrix was changed to {A}")
