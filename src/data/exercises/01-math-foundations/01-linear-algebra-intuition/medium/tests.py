import math


def _fn(sol):
    fn = sol.get("gram_schmidt")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน gram_schmidt", "Function gram_schmidt was not found")
    return fn


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _orthonormal(basis):
    for i, u in enumerate(basis):
        if not math.isclose(_dot(u, u), 1.0, abs_tol=1e-9):
            return f"u{i + 1} has length {math.sqrt(_dot(u, u)):.6f}"
        for j in range(i):
            if abs(_dot(u, basis[j])) > 1e-9:
                return f"u{j + 1} · u{i + 1} = {_dot(u, basis[j]):.6f}"
    return None


@check("lesson", th="ตัวอย่างของบทเรียนได้แกน x, y, z", en="The lesson's example gives the x, y and z axes")
def _(sol):
    got = _fn(sol)([[1, 0, 0], [1, 1, 0], [1, 1, 1]])
    want = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    if len(got) != 3 or any(not all(math.isclose(x, y, abs_tol=1e-9) for x, y in zip(g, w)) for g, w in zip(got, want)):
        raise Fail(f"ควรได้ {want} แต่ได้ {got!r}", f"Expected {want}, got {got!r}")


@check("orthonormal", th="ผลลัพธ์ตั้งฉากกันทุกคู่และยาว 1 ทุกตัว", en="Every result vector has length 1 and every pair is perpendicular")
def _(sol):
    basis = _fn(sol)([[2, 1, 0, 1], [1, 3, 1, 0], [0, 1, 4, 1], [1, 0, 1, 5]])
    problem = _orthonormal(basis) if len(basis) == 4 else f"expected 4 vectors, got {len(basis)}"
    if problem:
        raise Fail(f"ผลลัพธ์ไม่ใช่ orthonormal: {problem}", f"The result is not orthonormal: {problem}")


@check("dependent", th="ข้ามเวกเตอร์ที่ขึ้นต่อกับตัวก่อนหน้า", en="Skips vectors that depend on earlier ones")
def _(sol):
    basis = _fn(sol)([[1, 0, 0], [2, 0, 0], [3, 4, 0], [5, 5, 0]])
    if len(basis) != 2:
        raise Fail(f"เวกเตอร์ทั้งหมดอยู่บนระนาบ xy ควรได้ 2 ตัว แต่ได้ {len(basis)} ตัว", f"All the vectors lie in the xy-plane, so expect 2, got {len(basis)}")


@check("direction", th="เวกเตอร์ตัวแรกชี้ทางเดียวกับข้อมูลขาเข้าตัวแรก", en="The first output points the same way as the first input")
def _(sol):
    basis = _fn(sol)([[3, 4], [1, 0]])
    if not basis or not all(math.isclose(x, y, abs_tol=1e-9) for x, y in zip(basis[0], [0.6, 0.8])):
        raise Fail(f"u1 ควรเป็น [0.6, 0.8] แต่ได้ {basis[:1]!r}", f"u1 should be [0.6, 0.8], got {basis[:1]!r}")
