import math


def _check(sol, A, want_s, th, en):
    fn = sol.get("svd2")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน svd2", "Function svd2 was not found")
    try:
        U, S, Vt = fn([list(r) for r in A])
    except (ValueError, ZeroDivisionError) as e:
        raise Fail(f"{th}: เกิด {type(e).__name__}: {e}", f"{en}: {type(e).__name__}: {e}")
    if len(S) != 2 or not all(math.isclose(s, w, abs_tol=1e-9) for s, w in zip(S, want_s)):
        raise Fail(f"{th}: S ควรเป็น {want_s} แต่ได้ {S!r}", f"{en}: S should be {want_s}, got {S!r}")
    for name, M in (("U", U), ("Vt", Vt)):
        for i in range(2):
            for j in range(2):
                dot = M[0][i] * M[0][j] + M[1][i] * M[1][j] if name == "U" else M[i][0] * M[j][0] + M[i][1] * M[j][1]
                if not math.isclose(dot, 1.0 if i == j else 0.0, abs_tol=1e-9):
                    raise Fail(f"{th}: {name} ไม่ใช่เมทริกซ์เชิงตั้งฉาก ({name} = {M!r})", f"{en}: {name} is not orthogonal ({name} = {M!r})")
    back = [[sum(U[i][k] * S[k] * Vt[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    if not all(math.isclose(back[i][j], A[i][j], abs_tol=1e-9) for i in range(2) for j in range(2)):
        raise Fail(f"{th}: U diag(S) Vt = {back} ไม่เท่ากับ A = {A}", f"{en}: U diag(S) Vt = {back} is not A = {A}")


@check("general", th="[[3, 0], [4, 5]]: ค่าเอกฐาน √45 และ √5", en="[[3, 0], [4, 5]]: singular values √45 and √5")
def _(sol):
    _check(sol, [[3, 0], [4, 5]], [math.sqrt(45), math.sqrt(5)], "[[3, 0], [4, 5]]", "[[3, 0], [4, 5]]")


@check("shear", th="การเฉือน [[1, 1], [0, 1]]: φ และ 1/φ", en="The shear [[1, 1], [0, 1]]: φ and 1/φ")
def _(sol):
    phi = (1 + math.sqrt(5)) / 2
    _check(sol, [[1, 1], [0, 1]], [phi, 1 / phi], "[[1, 1], [0, 1]]", "[[1, 1], [0, 1]]")


@check("rank-1", th="แรงก์ 1 [[1, 2], [2, 4]]: ค่าเอกฐาน 5 และ 0", en="Rank 1 [[1, 2], [2, 4]]: singular values 5 and 0")
def _(sol):
    _check(sol, [[1, 2], [2, 4]], [5.0, 0.0], "[[1, 2], [2, 4]]", "[[1, 2], [2, 4]]")


@check("reflection", th="ทแยงมุมที่มีค่าติดลบ [[-2, 0], [0, 3]]", en="A diagonal with a negative entry [[-2, 0], [0, 3]]")
def _(sol):
    _check(sol, [[-2, 0], [0, 3]], [3.0, 2.0], "[[-2, 0], [0, 3]]", "[[-2, 0], [0, 3]]")


@check("rotation", th="การหมุน 30 องศา: ค่าเอกฐานซ้ำ 1 และ 1", en="A 30 degree rotation: repeated singular values 1 and 1", hidden=True)
def _(sol):
    c, s = math.cos(math.pi / 6), math.sin(math.pi / 6)
    _check(sol, [[c, -s], [s, c]], [1.0, 1.0], "การหมุน 30 องศา", "30 degree rotation")


@check("rounding", th="แรงก์ 1 ที่ค่าลักษณะเฉพาะติดลบนิดหนึ่งจากการปัดเศษ", en="Rank 1 where rounding makes an eigenvalue slightly negative", hidden=True)
def _(sol):
    A = [[1 / 3, 2 / 3], [1 / 7, 2 / 7]]
    s1 = math.sqrt(sum(x * x for row in A for x in row))
    _check(sol, A, [s1, 0.0], "[[1/3, 2/3], [1/7, 2/7]]", "[[1/3, 2/3], [1/7, 2/7]]")


@check("zero", th="เมทริกซ์ศูนย์", en="The zero matrix", hidden=True)
def _(sol):
    _check(sol, [[0, 0], [0, 0]], [0.0, 0.0], "[[0, 0], [0, 0]]", "[[0, 0], [0, 0]]")
