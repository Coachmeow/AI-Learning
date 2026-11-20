import math


def _close(sol, logits, t, want, th, en):
    fn = sol.get("temperature_softmax")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน temperature_softmax", "Function temperature_softmax was not found")
    got = fn(list(logits), t)
    if not isinstance(got, list) or len(got) != len(want) or not all(math.isclose(a, b, abs_tol=1e-6) for a, b in zip(got, want)):
        raise Fail(f"{th}: ควรได้ประมาณ {want} แต่ได้ {got!r}", f"{en}: should be about {want}, got {got!r}")


@check("sharpen", th="[2, 1] ที่ T = 0.5 ได้ [0.881, 0.119]", en="[2, 1] at T = 0.5 gives [0.881, 0.119]")
def _(sol):
    _close(sol, [2.0, 1.0], 0.5, [0.880797, 0.119203], "T = 0.5", "T = 0.5")


@check("standard", th="T = 1 เท่ากับ softmax ปกติ", en="T = 1 is the plain softmax")
def _(sol):
    _close(sol, [2.0, 1.0], 1.0, [0.731059, 0.268941], "T = 1", "T = 1")


@check("flatten", th="T = 10 ทำให้เกือบสม่ำเสมอ", en="T = 10 makes it nearly uniform")
def _(sol):
    _close(sol, [2.0, 1.0, 0.0], 10.0, [0.367165, 0.332225, 0.300610], "T = 10", "T = 10")
