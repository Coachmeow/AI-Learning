import math


def _fn(sol):
    fn = sol.get("absorbing_analysis")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน absorbing_analysis", "Function absorbing_analysis was not found")
    return fn


def _walk(N, p):
    P = [[0.0] * (N + 1) for _ in range(N + 1)]
    P[0][0] = P[N][N] = 1.0
    for k in range(1, N):
        P[k][k + 1], P[k][k - 1] = p, 1 - p
    return P


def _expect(sol, P, B, t, th, en):
    got = _fn(sol)([row[:] for row in P])
    if not isinstance(got, (tuple, list)) or len(got) != 2:
        raise Fail(f"ต้องคืน (B, t) แต่ได้ {got!r}", f"Must return (B, t), got {got!r}")
    gB, gt = got
    ok_B = isinstance(gB, list) and len(gB) == len(B) and all(
        isinstance(r, list) and len(r) == len(w) and all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(r, w)) for r, w in zip(gB, B))
    if not ok_B:
        raise Fail(f"{th}: B ควรเป็น {B} แต่ได้ {gB!r}", f"{en}: B should be {B}, got {gB!r}")
    if not isinstance(gt, list) or len(gt) != len(t) or not all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(gt, t)):
        raise Fail(f"{th}: t ควรเป็น {t} แต่ได้ {gt!r}", f"{en}: t should be {t}, got {gt!r}")


def _raises(sol, P, th, en):
    try:
        got = _fn(sol)([row[:] for row in P])
    except ValueError:
        return
    except Exception as e:
        raise Fail(f"{th}: ควร raise ValueError แต่เกิด {type(e).__name__}: {e}", f"{en}: should raise ValueError, got {type(e).__name__}: {e}")
    raise Fail(f"{th}: ควร raise ValueError แต่คืน {got!r}", f"{en}: should raise ValueError, returned {got!r}")


@check("fair-walk", th="การเดินยุติธรรมบน 0..4: B = [[0.75, 0.25], [0.5, 0.5], [0.25, 0.75]], t = [3, 4, 3]", en="The fair walk on 0..4: B = [[0.75, 0.25], [0.5, 0.5], [0.25, 0.75]], t = [3, 4, 3]")
def _(sol):
    _expect(sol, _walk(4, 0.5), [[0.75, 0.25], [0.5, 0.5], [0.25, 0.75]], [3.0, 4.0, 3.0], "การเดินยุติธรรม", "Fair walk")


@check("biased-walk", th="การเดินที่เอนเอียง p = 0.6: จาก 1 ถึง 4 ก่อนด้วยความน่าจะเป็น 27/65", en="A biased walk with p = 0.6: from 1 it reaches 4 first with probability 27/65")
def _(sol):
    B = [[38 / 65, 27 / 65], [20 / 65, 45 / 65], [8 / 65, 57 / 65]]
    t = [3.3076923077, 3.8461538462, 2.5384615385]
    _expect(sol, _walk(4, 0.6), B, [round(x, 10) for x in t], "การเดินที่เอนเอียง", "Biased walk")


@check("self-loop", th="self-loop 0.5 ยังเป็นสถานะชั่วคราว: B = [[0.5, 0.5]], t = [2]", en="A 0.5 self-loop is still transient: B = [[0.5, 0.5]], t = [2]")
def _(sol):
    _expect(sol, [[1, 0, 0], [0.25, 0.5, 0.25], [0, 0, 1]], [[0.5, 0.5]], [2.0], "self-loop", "Self-loop")


@check("never-absorbed", th="สถานะ 1 และ 2 สลับกันไปเรื่อย ๆ ไม่มีวันถูกดูดกลืน: ต้อง raise ValueError", en="States 1 and 2 swap forever and are never absorbed: must raise ValueError")
def _(sol):
    _raises(sol, [[1, 0, 0], [0, 0, 1], [0, 1, 0]], "ไม่มีวันถูกดูดกลืน", "Never absorbed")


@check("middle", th="สถานะดูดกลืนไม่จำเป็นต้องอยู่ที่ปลาย: ดูดกลืนที่ 1 และ 3", en="Absorbing states need not be at the ends: absorbed at 1 and 3", hidden=True)
def _(sol):
    P = [[0.2, 0.5, 0.3, 0], [0, 1, 0, 0], [0.1, 0.2, 0.3, 0.4], [0, 0, 0, 1]]
    _expect(sol, P, [[41 / 53, 12 / 53], [21 / 53, 32 / 53]], [100 / 53, 90 / 53], "ดูดกลืนตรงกลาง", "Absorbed in the middle")


@check("long-walk", th="การเดินยุติธรรมบน 0..20: t[k] = k(20 - k) และ B[k] = [(20 - k)/20, k/20]", en="The fair walk on 0..20: t[k] = k(20 - k) and B[k] = [(20 - k)/20, k/20]", hidden=True)
def _(sol):
    N = 20
    B = [[(N - k) / N, k / N] for k in range(1, N)]
    t = [float(k * (N - k)) for k in range(1, N)]
    _expect(sol, _walk(N, 0.5), B, t, "เส้นทางยาว 20", "Walk of length 20")


@check("no-absorbing", th="ไม่มีสถานะดูดกลืนต้อง raise ValueError", en="No absorbing state must raise ValueError", hidden=True)
def _(sol):
    _raises(sol, [[0.5, 0.5], [0.5, 0.5]], "ไม่มีสถานะดูดกลืน", "No absorbing state")


@check("bad-rows", th="แถวที่ไม่ใช่การแจกแจงความน่าจะเป็นต้อง raise ValueError", en="A row that is not a probability distribution must raise ValueError", hidden=True)
def _(sol):
    _raises(sol, [[1, 0, 0], [0.3, 0.3, 0.3], [0, 0, 1]], "แถวรวมได้ 0.9", "Row sums to 0.9")
