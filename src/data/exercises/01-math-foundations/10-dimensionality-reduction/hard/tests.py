import math


def _run(sol, X, k):
    fn = sol.get("pca")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน pca", "Function pca was not found")
    got = fn([list(r) for r in X], k)
    if not isinstance(got, (tuple, list)) or len(got) != 2:
        raise Fail(f"ต้องคืน (components, ratios) แต่ได้ {got!r}", f"Must return (components, ratios), got {got!r}")
    return got


def _vecs(got, want, th, en, tol=1e-6):
    ok = isinstance(got, list) and len(got) == len(want) and all(
        len(g) == len(w) and all(math.isclose(a, b, abs_tol=tol) for a, b in zip(g, w)) for g, w in zip(got, want))
    if not ok:
        raise Fail(f"{th}: components ควรเป็น {want} แต่ได้ {got!r}", f"{en}: the components should be {want}, got {got!r}")


def _nums(got, want, th, en, tol=1e-6):
    if not isinstance(got, list) or len(got) != len(want) or not all(math.isclose(a, b, abs_tol=tol) for a, b in zip(got, want)):
        raise Fail(f"{th}: ratios ควรเป็น {want} แต่ได้ {got!r}", f"{en}: the ratios should be {want}, got {got!r}")


def _axes(scale, rotate):
    # 6 points: ±scale[0] on axis 1, ±scale[1] on axis 2, ±scale[2] on axis 3, then rotated
    pts = []
    for i, s in enumerate(scale):
        for sign in (1, -1):
            p = [0.0, 0.0, 0.0]
            p[i] = sign * s
            pts.append(p)
    return [[sum(rotate[r][c] * p[c] for c in range(3)) for r in range(3)] for p in pts]


R30 = [[math.cos(math.pi / 6), -math.sin(math.pi / 6), 0.0], [math.sin(math.pi / 6), math.cos(math.pi / 6), 0.0], [0.0, 0.0, 1.0]]


@check("anti-diagonal", th="ข้อมูลที่กระจายตามแนว [1, -1] (เริ่มที่ [1, 1] จะไม่เจอ)", en="Data spread along [1, -1] (a [1, 1] start never finds it)")
def _(sol):
    X = [[2, -2], [-2, 2], [1, -1], [-1, 1], [0.5, 0.5], [-0.5, -0.5]]
    comps, ratios = _run(sol, X, 2)
    r = 1 / math.sqrt(2)
    _vecs(comps, [[r, -r], [r, r]], "แนว [1, -1]", "Spread along [1, -1]")
    _nums(ratios, [20 / 21, 1 / 21], "แนว [1, -1]", "Spread along [1, -1]")


@check("rotated-axes", th="แกนที่หมุน 30 องศา ความแปรปรวน 3.6, 1.6, 0.4", en="Axes rotated by 30 degrees, variances 3.6, 1.6 and 0.4")
def _(sol):
    comps, ratios = _run(sol, _axes([3.0, 2.0, 1.0], R30), 3)
    want = [[R30[0][c], R30[1][c], R30[2][c]] for c in range(3)]
    want = [v if next(x for x in v if abs(x) > 1e-9) > 0 else [-x for x in v] for v in want]
    _vecs(comps, want, "หมุน 30 องศา", "Rotated by 30 degrees")
    _nums(ratios, [3.6 / 5.6, 1.6 / 5.6, 0.4 / 5.6], "หมุน 30 องศา", "Rotated by 30 degrees")


@check("offset", th="เลื่อนข้อมูลทั้งชุดไม่เปลี่ยนผล", en="Shifting all the data doesn't change the result")
def _(sol):
    X = [[p[0] + 50, p[1] - 20, p[2] + 7] for p in _axes([3.0, 2.0, 1.0], R30)]
    comps, ratios = _run(sol, X, 1)
    _vecs(comps, [[R30[0][0], R30[1][0], R30[2][0]]], "ข้อมูลที่เลื่อน", "Shifted data")
    _nums(ratios, [3.6 / 5.6], "ข้อมูลที่เลื่อน", "Shifted data")


@check("orthonormal", th="องค์ประกอบยาว 1 และตั้งฉากกัน", en="Components have length 1 and are orthogonal", hidden=True)
def _(sol):
    X = [[2.0, 0.0, 1.0], [0.0, 1.0, -1.0], [3.0, 1.0, 0.0], [1.0, 3.0, 2.0], [-1.0, 0.0, 1.0], [4.0, 2.0, 1.5]]
    comps, ratios = _run(sol, X, 3)
    for i in range(3):
        for j in range(3):
            dot = sum(a * b for a, b in zip(comps[i], comps[j]))
            if not math.isclose(dot, 1.0 if i == j else 0.0, abs_tol=1e-6):
                raise Fail(f"components[{i}] · components[{j}] = {dot:.6f} ควรเป็น {1 if i == j else 0}", f"components[{i}] · components[{j}] = {dot:.6f}, should be {1 if i == j else 0}")
    if not math.isclose(sum(ratios), 1.0, abs_tol=1e-6) or ratios != sorted(ratios, reverse=True):
        raise Fail(f"ratios ของทั้ง 3 องค์ประกอบต้องรวมได้ 1 และเรียงจากมากไปน้อย แต่ได้ {ratios}", f"The 3 ratios must add up to 1 and run from high to low, got {ratios}")
