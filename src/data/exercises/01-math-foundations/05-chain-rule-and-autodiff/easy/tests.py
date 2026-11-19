import math


def _V(sol):
    V = sol.get("Value")
    if V is None:
        raise Fail("ไม่พบคลาส Value", "Class Value was not found")
    return V


def _eq(got, want, th, en):
    if not isinstance(got, (int, float)) or not math.isclose(got, want, abs_tol=1e-9):
        raise Fail(f"{th}: ควรเป็น {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("two-factors", th="y = x1 * x2 ที่ x1 = 2, x2 = 3", en="y = x1 * x2 with x1 = 2, x2 = 3")
def _(sol):
    V = _V(sol)
    x1, x2 = V(2.0), V(3.0)
    (x1 * x2).backward()
    _eq(x1.grad, 3.0, "dy/dx1 (= x2)", "dy/dx1 (= x2)")
    _eq(x2.grad, 2.0, "dy/dx2 (= x1)", "dy/dx2 (= x1)")


@check("chain", th="y = (x * w) * 5: gradient ต้องคูณ out.grad ที่ไหลมา", en="y = (x * w) * 5: the gradient must include the incoming out.grad")
def _(sol):
    V = _V(sol)
    x, w = V(2.0), V(-4.0)
    ((x * w) * 5).backward()
    _eq(x.grad, -20.0, "dy/dx (= w * 5)", "dy/dx (= w * 5)")
    _eq(w.grad, 10.0, "dy/dw (= x * 5)", "dy/dw (= x * 5)")


@check("same-value", th="y = x * x + x ที่ x = 3 ได้ 2x + 1 = 7", en="y = x * x + x at x = 3 gives 2x + 1 = 7")
def _(sol):
    V = _V(sol)
    x = V(3.0)
    (x * x + x).backward()
    _eq(x.grad, 7.0, "dy/dx", "dy/dx")
