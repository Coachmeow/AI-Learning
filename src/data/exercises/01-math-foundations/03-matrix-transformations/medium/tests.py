import math

def R90():
    return [[0, -1], [1, 0]]


def S():
    return [[2, 0], [0, 0.5]]


def _fn(sol):
    fn = sol.get("compose")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน compose", "Function compose was not found")
    return fn


def _same(got, want, what_th, what_en):
    ok = isinstance(got, list) and len(got) == 2 and all(
        isinstance(g, list) and len(g) == 2 and all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(g, w))
        for g, w in zip(got, want))
    if not ok:
        raise Fail(f"{what_th}: ควรได้ {want} แต่ได้ {got!r}", f"{what_en}: should be {want}, got {got!r}")


def _mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


@check("rotate-then-scale", th="หมุน 90 แล้วย่อขยาย (2, 0.5) ได้ S @ R", en="Rotate 90 then scale (2, 0.5) gives S @ R")
def _(sol):
    _same(_fn(sol)([R90(), S()]), [[0, -2], [0.5, 0]], "[R90, S]", "[R90, S]")


@check("scale-then-rotate", th="ย่อขยายแล้วหมุน 90 ได้ R @ S", en="Scale then rotate 90 gives R @ S")
def _(sol):
    _same(_fn(sol)([S(), R90()]), [[0, -0.5], [2, 0]], "[S, R90]", "[S, R90]")


@check("empty", th="ไม่มีขั้นตอนเลยได้เมทริกซ์เอกลักษณ์", en="No steps gives the identity")
def _(sol):
    _same(_fn(sol)([]), [[1, 0], [0, 1]], "compose([])", "compose([])")


@check("three", th="สามขั้นตอนจากแบบฝึกหัดที่ 3 และดีเทอร์มิแนนต์ 1.2", en="The three steps from Exercise 3, with determinant 1.2", hidden=True)
def _(sol):
    t = math.pi / 6
    rot = [[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]]
    scale = [[1.5, 0], [0, 0.8]]
    shear = [[1, 0.3], [0, 1]]
    want = _mul(shear, _mul(scale, rot))
    got = _fn(sol)([rot, scale, shear])
    _same(got, want, "หมุน 30 องศา ย่อขยาย แล้วเฉือน", "Rotate 30 degrees, scale, then shear")
    det = got[0][0] * got[1][1] - got[0][1] * got[1][0]
    if not math.isclose(det, 1.2, abs_tol=1e-9):
        raise Fail(f"ดีเทอร์มิแนนต์ควรเป็น 1.2 แต่ได้ {det}", f"The determinant should be 1.2, got {det}")


@check("no-mutation", th="ไม่แก้เมทริกซ์ที่ส่งเข้ามา", en="Leaves the given matrices unchanged", hidden=True)
def _(sol):
    a, b = [[0, -1], [1, 0]], [[2, 0], [0, 0.5]]
    _fn(sol)([a, b])
    if a != [[0, -1], [1, 0]] or b != [[2, 0], [0, 0.5]]:
        raise Fail(f"เมทริกซ์ที่ส่งเข้ามาถูกแก้เป็น {a} และ {b}", f"The given matrices were changed to {a} and {b}")
