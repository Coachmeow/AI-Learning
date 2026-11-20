import math


def _run(sol, A, b, **kw):
    fn = sol.get("conjugate_gradient")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน conjugate_gradient", "Function conjugate_gradient was not found")
    got = fn([row[:] for row in A], list(b), **kw)
    if not isinstance(got, (tuple, list)) or len(got) != 2:
        raise Fail(f"ต้องคืน (x, iterations) แต่ได้ {got!r}", f"Must return (x, iterations), got {got!r}")
    x, k = got
    if not isinstance(x, list) or len(x) != len(b):
        raise Fail(f"x ต้องเป็น list ยาว {len(b)} แต่ได้ {x!r}", f"x must be a list of length {len(b)}, got {x!r}")
    return x, k


def _expect(sol, A, b, want_x, want_k, th, en, rel=1e-8, **kw):
    x, k = _run(sol, A, b, **kw)
    scale = max(abs(v) for v in want_x) or 1.0
    if not all(abs(a - w) <= rel * scale for a, w in zip(x, want_x)):
        raise Fail(f"{th}: x ควรเป็น {want_x} แต่ได้ {x}", f"{en}: x should be {want_x}, got {x}")
    if k != want_k:
        raise Fail(f"{th}: ควรใช้ {want_k} รอบ แต่ได้ {k!r}", f"{en}: should take {want_k} iterations, got {k!r}")


def _raises(sol, exc, A, b, th, en, **kw):
    try:
        got = _run(sol, A, b, **kw)
    except exc:
        return
    except Exception as e:
        raise Fail(f"{th}: ควร raise {exc.__name__} แต่เกิด {type(e).__name__}: {e}", f"{en}: should raise {exc.__name__}, got {type(e).__name__}: {e}")
    raise Fail(f"{th}: ควร raise {exc.__name__} แต่คืน {got!r}", f"{en}: should raise {exc.__name__}, returned {got!r}")


_D3 = [1.0, 1.0, 4.0, 4.0, 9.0, 9.0]
_A3 = [[_D3[i] if i == j else 0.0 for j in range(6)] for i in range(6)]
_b3 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]


@check("two", th="[[4, 1], [1, 3]] x = [1, 2] ได้ [1/11, 7/11] ใน 2 รอบ", en="[[4, 1], [1, 3]] x = [1, 2] gives [1/11, 7/11] in 2 iterations")
def _(sol):
    _expect(sol, [[4, 1], [1, 3]], [1, 2], [1 / 11, 7 / 11], 2, "ระบบ 2x2", "2x2 system")


@check("distinct", th="เมทริกซ์ 6x6 ที่มีค่าลักษณะเฉพาะต่างกัน 3 ค่าใช้ 3 รอบ", en="A 6x6 matrix with 3 distinct eigenvalues takes 3 iterations")
def _(sol):
    _expect(sol, _A3, _b3, [b / d for b, d in zip(_b3, _D3)], 3, "ค่าลักษณะเฉพาะ 1, 4, 9", "Eigenvalues 1, 4, 9")


@check("zero-b", th="b = 0 คืนเวกเตอร์ศูนย์และ 0 รอบ", en="b = 0 returns the zero vector and 0 iterations")
def _(sol):
    x, k = _run(sol, [[2, 0], [0, 3]], [0.0, 0.0])
    if any(v != 0 for v in x) or k != 0:
        raise Fail(f"ควรได้ ([0.0, 0.0], 0) แต่ได้ ({x}, {k!r})", f"Should be ([0.0, 0.0], 0), got ({x}, {k!r})")


@check("indefinite", th="[[1, 0], [0, -2]] ต้อง raise ValueError", en="[[1, 0], [0, -2]] must raise ValueError")
def _(sol):
    _raises(sol, ValueError, [[1, 0], [0, -2]], [1, 1], "เมทริกซ์ไม่บวกแน่นอน", "Indefinite matrix")


@check("tiny-b", th="b เล็กมาก (1e-12) ยังต้องแก้ได้จริง: เกณฑ์ต้องเป็นแบบสัมพัทธ์", en="A tiny b (1e-12) must still be solved: the criterion must be relative", hidden=True)
def _(sol):
    _expect(sol, [[4, 1], [1, 3]], [1e-12, 2e-12], [1e-12 / 11, 7e-12 / 11], 2, "b ขนาด 1e-12", "b of size 1e-12")


@check("max-iter", th="max_iter = 2 กับระบบที่ต้องใช้ 3 รอบต้อง raise RuntimeError", en="max_iter = 2 on a system that needs 3 iterations must raise RuntimeError", hidden=True)
def _(sol):
    _raises(sol, RuntimeError, _A3, _b3, "max_iter = 2", "max_iter = 2", max_iter=2)


@check("no-mutation", th="ไม่แก้ไข A และ b ที่รับเข้ามา", en="Does not modify the A and b it receives", hidden=True)
def _(sol):
    fn = sol.get("conjugate_gradient")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน conjugate_gradient", "Function conjugate_gradient was not found")
    A = [[4.0, 1.0], [1.0, 3.0]]
    b = [1.0, 2.0]
    fn(A, b)
    if A != [[4.0, 1.0], [1.0, 3.0]] or b != [1.0, 2.0]:
        raise Fail(f"A หรือ b ถูกแก้: A = {A}, b = {b}", f"A or b was modified: A = {A}, b = {b}")


@check("larger", th="เมทริกซ์ 30x30 สมมาตรบวกแน่นอน: Ax ใกล้ b และไม่เกิน 30 รอบ", en="A 30x30 symmetric positive definite matrix: Ax is close to b within 30 iterations", hidden=True)
def _(sol):
    n = 30
    B = [[((i * 13 + j * 7) % 11 - 5) / 5 for j in range(n)] for i in range(n)]
    A = [[sum(B[i][k] * B[j][k] for k in range(n)) + (n if i == j else 0) for j in range(n)] for i in range(n)]
    b = [math.sin(i + 1) for i in range(n)]
    x, k = _run(sol, A, b)
    res = math.sqrt(sum((sum(A[i][j] * x[j] for j in range(n)) - b[i]) ** 2 for i in range(n)))
    if res > 1e-8:
        raise Fail(f"||Ax - b|| = {res:.3g} ยังใหญ่เกินไป", f"||Ax - b|| = {res:.3g} is still too large")
    if not isinstance(k, int) or not 1 <= k <= n:
        raise Fail(f"จำนวนรอบควรอยู่ระหว่าง 1 ถึง {n} แต่ได้ {k!r}", f"The iteration count should be between 1 and {n}, got {k!r}")
