import math


def _fn(sol):
    fn = sol.get("project_l1")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน project_l1", "Function project_l1 was not found")
    return fn


def _expect(sol, v, r, want, th, en):
    got = _fn(sol)(list(v), r)
    if not isinstance(got, list) or len(got) != len(want) or not all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(got, want)):
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


def _reference(v, r):
    # Bisection on theta: sum(max(|v_i| - theta, 0)) is decreasing in theta.
    if sum(abs(x) for x in v) <= r:
        return list(v)
    lo, hi = 0.0, max(abs(x) for x in v)
    for _ in range(200):
        mid = (lo + hi) / 2
        if sum(max(abs(x) - mid, 0.0) for x in v) > r:
            lo = mid
        else:
            hi = mid
    return [math.copysign(max(abs(x) - hi, 0.0), x) for x in v]


def _raises(sol, v, r, th, en):
    try:
        got = _fn(sol)(list(v), r)
    except ValueError:
        return
    except Exception as e:
        raise Fail(f"{th}: ควร raise ValueError แต่เกิด {type(e).__name__}: {e}", f"{en}: should raise ValueError, got {type(e).__name__}: {e}")
    raise Fail(f"{th}: ควร raise ValueError แต่คืน {got!r}", f"{en}: should raise ValueError, returned {got!r}")


@check("corner", th="[3, 2] กับ radius 1 ได้ [1, 0] ที่มุม", en="[3, 2] with radius 1 gives [1, 0], at the corner")
def _(sol):
    _expect(sol, [3, 2], 1, [1.0, 0.0], "[3, 2]", "[3, 2]")


@check("inside", th="จุดที่อยู่ในลูกบอลแล้วไม่ถูกเปลี่ยน", en="A point already inside the ball is unchanged")
def _(sol):
    _expect(sol, [0.5, -0.2, 0.1], 1, [0.5, -0.2, 0.1], "อยู่ในลูกบอลแล้ว", "Already inside")


@check("edge", th="[2, 1.5] กับ radius 1 ได้ [0.75, 0.25] บนขอบ ไม่ใช่มุม", en="[2, 1.5] with radius 1 gives [0.75, 0.25], on an edge rather than a corner")
def _(sol):
    _expect(sol, [2, 1.5], 1, [0.75, 0.25], "[2, 1.5]", "[2, 1.5]")


@check("partial-k", th="[3, 1, 0.5] กับ radius 1 ใช้ k = 1 และได้ [1, 0, 0]", en="[3, 1, 0.5] with radius 1 uses k = 1 and gives [1, 0, 0]")
def _(sol):
    _expect(sol, [3, 1, 0.5], 1, [1.0, 0.0, 0.0], "[3, 1, 0.5]", "[3, 1, 0.5]")


@check("signs", th="ค่าลบคงเครื่องหมายไว้: [-2, 2] กับ radius 1 ได้ [-0.5, 0.5]", en="Negative entries keep their sign: [-2, 2] with radius 1 gives [-0.5, 0.5]", hidden=True)
def _(sol):
    _expect(sol, [-2, 2], 1, [-0.5, 0.5], "[-2, 2]", "[-2, 2]")


@check("unsorted", th="ลำดับของขาเข้าไม่เรียง: [0.1, -4, 0.3, 2.5] กับ radius 2", en="Unsorted input: [0.1, -4, 0.3, 2.5] with radius 2", hidden=True)
def _(sol):
    _expect(sol, [0.1, -4, 0.3, 2.5], 2, [0.0, -1.75, 0.0, 0.25], "[0.1, -4, 0.3, 2.5]", "[0.1, -4, 0.3, 2.5]")


@check("radius", th="radius = 0 หรือติดลบต้อง raise ValueError", en="radius = 0 or negative must raise ValueError", hidden=True)
def _(sol):
    _raises(sol, [1, 2], 0, "radius = 0", "radius = 0")
    _raises(sol, [1, 2], -1, "radius = -1", "radius = -1")


@check("no-mutation", th="ไม่แก้ไข v ที่รับเข้ามา", en="Does not modify the v it receives", hidden=True)
def _(sol):
    v = [3.0, -2.0, 0.5]
    _fn(sol)(v, 1)
    if v != [3.0, -2.0, 0.5]:
        raise Fail(f"v ถูกแก้เป็น {v}", f"v was modified to {v}")


@check("many", th="เวกเตอร์ 40 มิติ ตรงกับคำตอบอ้างอิงที่หาด้วย bisection", en="40-dimensional vectors match a bisection reference", hidden=True)
def _(sol):
    for seed in range(5):
        v = [math.sin(7.3 * i + seed) * (1 + (i * seed) % 5) for i in range(40)]
        r = 1.0 + seed * 3.5
        want = _reference(v, r)
        got = _fn(sol)(list(v), r)
        if not isinstance(got, list) or len(got) != 40 or not all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(got, want)):
            raise Fail(f"seed {seed}, radius {r}: ไม่ตรงกับคำตอบอ้างอิง", f"seed {seed}, radius {r}: does not match the reference")
        if sum(abs(x) for x in got) > r + 1e-9:
            raise Fail(f"seed {seed}: sum(|w|) = {sum(abs(x) for x in got)} เกิน radius {r}", f"seed {seed}: sum(|w|) = {sum(abs(x) for x in got)} exceeds radius {r}")
