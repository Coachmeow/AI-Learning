import math


def _need(sol, name):
    obj = sol.get(name)
    if obj is None:
        raise Fail(f"ไม่พบ {name}", f"{name} was not found")
    return obj


def _deriv(sol, f, x, want, th, en):
    got = _need(sol, "derivative")(f, x)
    if not isinstance(got, (int, float)) or not math.isclose(got, want, abs_tol=1e-9):
        raise Fail(f"{th}: อนุพันธ์ควรเป็น {want} แต่ได้ {got!r}", f"{en}: the derivative should be {want}, got {got!r}")


@check("cube", th="x * x * x ที่ x = 2: ค่า 8 อนุพันธ์ 12", en="x * x * x at x = 2: value 8, derivative 12")
def _(sol):
    D = _need(sol, "Dual")
    x = D(2.0, 1.0)
    y = x * x * x
    if not math.isclose(y.val, 8.0) or not math.isclose(y.der, 12.0):
        raise Fail(f"ควรได้ (8, 12) แต่ได้ ({y.val}, {y.der})", f"Should be (8, 12), got ({y.val}, {y.der})")


@check("constants", th="ค่าคงที่ทั้งซ้ายและขวา: 3 * x + 1", en="Constants on both sides: 3 * x + 1")
def _(sol):
    _deriv(sol, lambda x: 3 * x + 1, 5.0, 3.0, "3 * x + 1", "3 * x + 1")
    _deriv(sol, lambda x: x * 3 + 1, 5.0, 3.0, "x * 3 + 1", "x * 3 + 1")


@check("subtract", th="10 - x * x ที่ x = 3 ได้ -6", en="10 - x * x at x = 3 gives -6")
def _(sol):
    _deriv(sol, lambda x: 10 - x * x, 3.0, -6.0, "10 - x * x", "10 - x * x")


@check("sin", th="sin(x * x) ที่ x = 1.5 ได้ cos(2.25) * 3", en="sin(x * x) at x = 1.5 gives cos(2.25) * 3")
def _(sol):
    s = _need(sol, "dual_sin")
    _deriv(sol, lambda x: s(x * x), 1.5, math.cos(2.25) * 3.0, "sin(x * x)", "sin(x * x)")


@check("constant-function", th="ฟังก์ชันคงที่มีอนุพันธ์ 0.0", en="A constant function has derivative 0.0", hidden=True)
def _(sol):
    _deriv(sol, lambda x: 7, 1.0, 0.0, "f(x) = 7", "f(x) = 7")


@check("mixed", th="(x * x - 4 * x) * x - 2 ที่ x = 1.5", en="(x * x - 4 * x) * x - 2 at x = 1.5", hidden=True)
def _(sol):
    _deriv(sol, lambda x: (x * x - 4 * x) * x - 2, 1.5, 3 * 1.5 ** 2 - 8 * 1.5, "x³ - 4x² - 2", "x³ - 4x² - 2")
