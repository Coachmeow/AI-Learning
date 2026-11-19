import math


def _V(sol):
    V = sol.get("Value")
    if V is None:
        raise Fail("ไม่พบคลาส Value", "Class Value was not found")
    return V


def _eq(got, want, th, en, tol=1e-9):
    if not isinstance(got, (int, float)) or not math.isclose(got, want, rel_tol=tol, abs_tol=tol):
        raise Fail(f"{th}: ควรเป็น {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("simple", th="y = x1 * x2 + b ที่ x1 = 2, x2 = 3", en="y = x1 * x2 + b with x1 = 2, x2 = 3")
def _(sol):
    V = _V(sol)
    x1, x2, b = V(2.0), V(3.0), V(1.0)
    y = x1 * x2 + b
    y.backward()
    _eq(y.grad, 1.0, "y.grad (ค่าตั้งต้น)", "y.grad (the seed)")
    _eq(x1.grad, 3.0, "dy/dx1", "dy/dx1")
    _eq(x2.grad, 2.0, "dy/dx2", "dy/dx2")
    _eq(b.grad, 1.0, "dy/db", "dy/db")


@check("shared", th="a = x * 2, y = a + (a * 3) * 2: ได้ dy/dx = 14", en="a = x * 2, y = a + (a * 3) * 2: dy/dx = 14")
def _(sol):
    V = _V(sol)
    x = V(1.0)
    a = x * 2
    y = a + (a * 3) * 2
    y.backward()
    _eq(a.grad, 7.0, "dy/da", "dy/da")
    _eq(x.grad, 14.0, "dy/dx", "dy/dx")


@check("reused", th="a = x * 2, y = a + a: แต่ละโหนดทำ _backward ครั้งเดียว", en="a = x * 2, y = a + a: each node runs _backward once")
def _(sol):
    V = _V(sol)
    x = V(5.0)
    a = x * 2
    (a + a).backward()
    _eq(x.grad, 4.0, "dy/dx", "dy/dx")


@check("deep", th="ลูกโซ่การคูณลึก 1,500 ชั้น", en="A chain of 1,500 multiplications", hidden=True)
def _(sol):
    V = _V(sol)
    x = V(1.0)
    y = x
    for _ in range(1500):
        y = y * 1.001
    try:
        y.backward()
    except RecursionError:
        raise Fail("เกิด RecursionError: ต้องเรียงลำดับโดยไม่ใช้ recursion", "RecursionError: the sort must not use recursion")
    _eq(x.grad, 1.001 ** 1500, "dy/dx", "dy/dx")


@check("neuron", th="นิวรอน tanh(w1*x1 + w2*x2 + b) เทียบกับสูตร", en="A neuron tanh(w1*x1 + w2*x2 + b) against the formula", hidden=True)
def _(sol):
    V = _V(sol)
    x1, x2, w1, w2, b = V(0.5), V(-1.5), V(0.8), V(0.3), V(0.1)
    y = (w1 * x1 + w2 * x2 + b).tanh()
    y.backward()
    z = 0.8 * 0.5 + 0.3 * -1.5 + 0.1
    d = 1 - math.tanh(z) ** 2
    for name, v, want in (("w1", w1, d * 0.5), ("w2", w2, d * -1.5), ("x1", x1, d * 0.8), ("b", b, d)):
        _eq(v.grad, want, f"dy/d{name}", f"dy/d{name}")
