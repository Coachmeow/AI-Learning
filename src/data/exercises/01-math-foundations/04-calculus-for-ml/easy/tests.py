import math


def _check(sol, f, x, want, th, en):
    fn = sol.get("numerical_derivative")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน numerical_derivative", "Function numerical_derivative was not found")
    got = fn(f, x)
    if not isinstance(got, (int, float)) or not math.isclose(got, want, abs_tol=1e-6):
        raise Fail(f"{th}: ควรได้ประมาณ {want} แต่ได้ {got!r}", f"{en}: should be about {want}, got {got!r}")


@check("square", th="x² ที่ x = 3 ได้ 6", en="x² at x = 3 gives 6")
def _(sol):
    _check(sol, lambda x: x ** 2, 3.0, 6.0, "อนุพันธ์ของ x² ที่ x = 3", "Derivative of x² at x = 3")


@check("cube", th="x³ ที่ x = 2 ได้ 12", en="x³ at x = 2 gives 12")
def _(sol):
    _check(sol, lambda x: x ** 3, 2.0, 12.0, "อนุพันธ์ของ x³ ที่ x = 2", "Derivative of x³ at x = 2")


@check("sin", th="sin(x) ที่ x = 0 ได้ cos(0) = 1", en="sin(x) at x = 0 gives cos(0) = 1")
def _(sol):
    _check(sol, math.sin, 0.0, 1.0, "อนุพันธ์ของ sin ที่ 0", "Derivative of sin at 0")


@check("exp", th="e^x ที่ x = 1 ได้ e", en="e^x at x = 1 gives e")
def _(sol):
    _check(sol, math.exp, 1.0, math.e, "อนุพันธ์ของ e^x ที่ 1", "Derivative of e^x at 1")
