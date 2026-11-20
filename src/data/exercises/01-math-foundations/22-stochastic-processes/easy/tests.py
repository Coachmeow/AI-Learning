import math

_W = [[0.7, 0.1, 0.2], [0.3, 0.4, 0.3], [0.4, 0.2, 0.4]]


def _step(sol, dist, P, want, th, en):
    fn = sol.get("step_distribution")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน step_distribution", "Function step_distribution was not found")
    got = fn(list(dist), P)
    if not isinstance(got, list) or len(got) != len(want) or not all(math.isclose(a, b, abs_tol=1e-12) for a, b in zip(got, want)):
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("sunny", th="เริ่มที่แดดออกแน่นอน: ได้แถวแรกของ P คือ [0.7, 0.1, 0.2]", en="Starting surely sunny gives P's first row, [0.7, 0.1, 0.2]")
def _(sol):
    _step(sol, [1.0, 0.0, 0.0], _W, [0.7, 0.1, 0.2], "เริ่มที่แดดออก", "Start sunny")


@check("mixed", th="[0.5, 0.5, 0] ได้ [0.5, 0.25, 0.25]", en="[0.5, 0.5, 0] gives [0.5, 0.25, 0.25]")
def _(sol):
    _step(sol, [0.5, 0.5, 0.0], _W, [0.5, 0.25, 0.25], "แจกแจงผสม", "Mixed start")


@check("stationary", th="การแจกแจงคงที่ [6/11, 2/11, 3/11] ไม่เปลี่ยน", en="The stationary distribution [6/11, 2/11, 3/11] does not change")
def _(sol):
    pi = [6 / 11, 2 / 11, 3 / 11]
    _step(sol, pi, _W, pi, "การแจกแจงคงที่", "Stationary distribution")
