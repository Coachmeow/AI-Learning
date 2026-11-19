import math


def _run(sol, X):
    fn = sol.get("center")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน center", "Function center was not found")
    return fn(X)


def _same(got, want, th, en):
    ok = isinstance(got, list) and len(got) == len(want) and all(
        len(g) == len(w) and all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(g, w)) for g, w in zip(got, want))
    if not ok:
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("basic", th="ข้อมูล 3x2: ค่าเฉลี่ยคอลัมน์คือ 2 และ 20", en="3x2 data: the column means are 2 and 20")
def _(sol):
    _same(_run(sol, [[1, 10], [2, 20], [3, 30]]), [[-1, -10], [0, 0], [1, 10]], "[[1, 10], [2, 20], [3, 30]]", "[[1, 10], [2, 20], [3, 30]]")


@check("means-zero", th="หลังจัดกึ่งกลาง ค่าเฉลี่ยของทุกคอลัมน์เป็น 0", en="After centering, every column has mean 0")
def _(sol):
    X = [[4.0, -1.0, 7.0], [2.0, 5.0, 7.5], [9.0, 0.5, 6.0], [1.0, 2.5, 8.5]]
    got = _run(sol, [list(r) for r in X])
    means = [sum(r[j] for r in got) / len(got) for j in range(3)]
    if not all(math.isclose(m, 0, abs_tol=1e-9) for m in means):
        raise Fail(f"ค่าเฉลี่ยของคอลัมน์ควรเป็น 0 แต่ได้ {means}", f"The column means should be 0, got {means}")
    _same(got, [[r[j] - (sum(x[j] for x in X) / 4) for j in range(3)] for r in X], "ข้อมูล 4x3", "4x3 data")


@check("no-mutation", th="ไม่แก้ X ที่ส่งเข้ามา", en="Leaves the given X unchanged")
def _(sol):
    X = [[1.0, 2.0], [3.0, 4.0]]
    _run(sol, X)
    if X != [[1.0, 2.0], [3.0, 4.0]]:
        raise Fail(f"X ถูกแก้เป็น {X}", f"X was changed to {X}")
