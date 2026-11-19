import math

SQUARE = [[0, 0], [1, 0], [1, 1], [0, 1]]


def _fn(sol):
    fn = sol.get("apply")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน apply", "Function apply was not found")
    return fn


def _same(got, want, what_th, what_en):
    ok = isinstance(got, list) and len(got) == len(want) and all(
        len(g) == 2 and all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(g, w)) for g, w in zip(got, want))
    if not ok:
        raise Fail(f"{what_th}: ควรได้ {want} แต่ได้ {got!r}", f"{what_en}: should be {want}, got {got!r}")


@check("shear", th="เฉือนสี่เหลี่ยมจัตุรัสหนึ่งหน่วยด้วย kx=1", en="Shear the unit square with kx=1")
def _(sol):
    _same(_fn(sol)([[1, 1], [0, 1]], SQUARE), [[0, 0], [1, 0], [2, 1], [1, 1]], "เฉือน", "Shear")


@check("rotate", th="หมุน 90 องศา: (1, 0) ไปเป็น (0, 1)", en="Rotate 90 degrees: (1, 0) goes to (0, 1)")
def _(sol):
    _same(_fn(sol)([[0, -1], [1, 0]], [[1, 0], [0, 2]]), [[0, 1], [-2, 0]], "หมุน 90 องศา", "Rotate 90 degrees")


@check("scale", th="ย่อขยายด้วย sx=2, sy=0.5", en="Scale with sx=2, sy=0.5")
def _(sol):
    _same(_fn(sol)([[2, 0], [0, 0.5]], [[2, 1], [0, 2]]), [[4, 0.5], [0, 1]], "ย่อขยาย", "Scale")


@check("empty", th="ไม่มีจุดก็คืนรายการว่าง", en="No points gives an empty list")
def _(sol):
    _same(_fn(sol)([[1, 0], [0, 1]], []), [], "รายการว่าง", "Empty list")
