import math


def _fn(sol):
    fn = sol.get("eigenpairs")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน eigenpairs", "Function eigenpairs was not found")
    return fn


def _good(sol, M, want_vals):
    got = _fn(sol)([list(r) for r in M])
    if not isinstance(got, (list, tuple)) or len(got) != 2 or not all(isinstance(p, (list, tuple)) and len(p) == 2 for p in got):
        raise Fail(f"{M}: ต้องคืนคู่ (ค่าลักษณะเฉพาะ, เวกเตอร์) สองคู่ แต่ได้ {got!r}", f"{M}: must return two (eigenvalue, vector) pairs, got {got!r}")
    vals = [p[0] for p in got]
    if not all(isinstance(x, (int, float)) for x in vals) or not all(math.isclose(x, w, abs_tol=1e-9) for x, w in zip(vals, want_vals)):
        raise Fail(f"{M}: ค่าลักษณะเฉพาะ (มากไปน้อย) ควรเป็น {want_vals} แต่ได้ {vals!r}", f"{M}: the eigenvalues (largest first) should be {want_vals}, got {vals!r}")
    for lam, v in got:
        if len(v) != 2 or not math.isclose(math.hypot(v[0], v[1]), 1, abs_tol=1e-9):
            raise Fail(f"{M}: เวกเตอร์ {v!r} ต้องยาว 1", f"{M}: vector {v!r} must have length 1")
        Mv = [M[0][0] * v[0] + M[0][1] * v[1], M[1][0] * v[0] + M[1][1] * v[1]]
        if not all(math.isclose(x, lam * y, abs_tol=1e-9) for x, y in zip(Mv, v)):
            raise Fail(f"{M}: M @ {v} = {Mv} ไม่เท่ากับ {lam} * v", f"{M}: M @ {v} = {Mv} is not {lam} * v")
    (_, v1), (_, v2) = got
    if abs(v1[0] * v2[1] - v1[1] * v2[0]) < 1e-6:
        raise Fail(f"{M}: เวกเตอร์ {v1} และ {v2} ชี้ไปทิศเดียวกัน จึงสร้าง V ที่หาเมทริกซ์ผกผันได้ไม่ได้", f"{M}: vectors {v1} and {v2} point the same way, so they can't build an invertible V")


def _raises(sol, M, th, en):
    try:
        got = _fn(sol)([list(r) for r in M])
    except ValueError:
        return
    raise Fail(f"{M} {th} ต้อง raise ValueError แต่ได้ {got!r}", f"{M} {en}, so it must raise ValueError; got {got!r}")


@check("symmetric", th="[[2, 1], [1, 2]] จากบทเรียน: 3 และ 1", en="The lesson's [[2, 1], [1, 2]]: 3 and 1")
def _(sol):
    _good(sol, [[2, 1], [1, 2]], [3, 1])


@check("triangular", th="[[3, 1], [0, 2]]: 3 และ 2", en="[[3, 1], [0, 2]]: 3 and 2")
def _(sol):
    _good(sol, [[3, 1], [0, 2]], [3, 2])


@check("diagonal-order", th="เมทริกซ์ทแยงมุม [[1, 0], [0, 4]] เรียงมากไปน้อย", en="Diagonal [[1, 0], [0, 4]], largest first")
def _(sol):
    _good(sol, [[1, 0], [0, 4]], [4, 1])


@check("rotation", th="การหมุน 90 องศามีค่าลักษณะเฉพาะเชิงซ้อน", en="A 90 degree rotation has complex eigenvalues")
def _(sol):
    _raises(sol, [[0, -1], [1, 0]], "มีค่าลักษณะเฉพาะเชิงซ้อน", "has complex eigenvalues")


@check("scalar", th="[[3, 0], [0, 3]]: ค่าลักษณะเฉพาะซ้ำ แต่มีสองทิศ", en="[[3, 0], [0, 3]]: repeated eigenvalue, two directions")
def _(sol):
    _good(sol, [[3, 0], [0, 3]], [3, 3])


@check("shear", th="การเฉือน [[1, 1], [0, 1]] มีเวกเตอร์ลักษณะเฉพาะทิศเดียว", en="The shear [[1, 1], [0, 1]] has one eigenvector direction")
def _(sol):
    _raises(sol, [[1, 1], [0, 1]], "มีเวกเตอร์ลักษณะเฉพาะทิศเดียว", "has a single eigenvector direction")


@check("lower", th="สามเหลี่ยมล่าง [[2, 0], [1, 3]]", en="Lower triangular [[2, 0], [1, 3]]", hidden=True)
def _(sol):
    _good(sol, [[2, 0], [1, 3]], [3, 2])


@check("negative", th="สะท้อนข้ามเส้น y = x: 1 และ -1", en="Reflection across y = x: 1 and -1", hidden=True)
def _(sol):
    _good(sol, [[0, 1], [1, 0]], [1, -1])


@check("float-repeated", th="ทแยงมุมที่ต่างกันแค่ความคลาดเคลื่อนของทศนิยม", en="Diagonal entries that differ only by rounding error", hidden=True)
def _(sol):
    _good(sol, [[0.1 + 0.2, 0], [0, 0.3]], [0.3, 0.3])
    _good(sol, [[1.1 + 2.2, 0], [0, 3.3]], [3.3, 3.3])
