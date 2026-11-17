import math


def _cls(sol):
    cls = sol.get("GradientDescent")
    if cls is None:
        raise Fail("ไม่พบคลาส GradientDescent", "Class GradientDescent was not found")
    return cls


def _close(a, b, tol=1e-9):
    return all(math.isclose(x, y, rel_tol=tol, abs_tol=tol) for x, y in zip(a, b)) and len(a) == len(b)


@check("one-step", th="ก้าวเดียวได้ค่าที่ถูกต้อง", en="One step gives the right values")
def _(sol):
    out = _cls(sol)(lr=0.1).step([1.0, 2.0], [0.5, -1.0])
    if not isinstance(out, list):
        raise Fail(f"step ต้องคืนค่าเป็น list แต่ได้ {type(out).__name__}", f"step must return a list, got {type(out).__name__}")
    if not _close(out, [0.95, 2.1]):
        raise Fail(
            f"lr=0.1, params=[1.0, 2.0], grads=[0.5, -1.0] ควรได้ [0.95, 2.1] แต่ได้ {out}",
            f"lr=0.1, params=[1.0, 2.0], grads=[0.5, -1.0] should give [0.95, 2.1], got {out}",
        )


@check("direction", th="ขยับสวนทางกับเกรเดียนต์", en="Moves against the gradient")
def _(sol):
    out = _cls(sol)(lr=0.5).step([0.0, 0.0], [1.0, -1.0])
    if not (out[0] < 0 < out[1]):
        raise Fail(
            f"เกรเดียนต์บวกต้องทำให้ค่าลดลง เกรเดียนต์ลบต้องทำให้ค่าเพิ่มขึ้น แต่ได้ {out}",
            f"A positive gradient must lower the value and a negative one must raise it, got {out}",
        )


@check("no-mutation", th="ไม่แก้ list params เดิม", en="Leaves the original params list unchanged")
def _(sol):
    params = [3.0, 4.0]
    _cls(sol)(lr=0.1).step(params, [1.0, 1.0])
    if params != [3.0, 4.0]:
        raise Fail("ห้ามแก้ list params ที่ส่งเข้ามา ให้สร้าง list ใหม่แทน", "Do not change the params list you are given; build a new list instead")


@check("rosenbrock", th="ลด loss บนฟังก์ชัน Rosenbrock ได้", en="Lowers the loss on the Rosenbrock function")
def _(sol):
    def f(p):
        x, y = p
        return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

    def grad(p):
        x, y = p
        return [-2 * (1 - x) + 200 * (y - x ** 2) * (-2 * x), 200 * (y - x ** 2)]

    opt = _cls(sol)(lr=0.0005)
    p = [-1.0, 1.0]
    for _ in range(5000):
        p = opt.step(p, grad(p))
    if not f(p) < 0.1:
        raise Fail(f"หลัง 5000 ก้าว loss ควรต่ำกว่า 0.1 แต่ได้ {f(p):.4g}", f"After 5000 steps the loss should be below 0.1, got {f(p):.4g}")
