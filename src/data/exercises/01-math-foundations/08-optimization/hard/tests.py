import math


def _cls(sol):
    cls = sol.get("Adam")
    if cls is None:
        raise Fail("ไม่พบคลาส Adam", "Class Adam was not found")
    return cls


@check("first-step", th="ก้าวแรกขยับราว lr ไม่ว่าเกรเดียนต์จะใหญ่แค่ไหน", en="First step moves about lr, whatever the gradient size")
def _(sol):
    out = _cls(sol)(lr=0.001).step([0.0, 0.0], [1000.0, 0.001])
    if not isinstance(out, list) or len(out) != 2:
        raise Fail(f"step ต้องคืน list ยาว 2 แต่ได้ {out!r}", f"step must return a list of length 2, got {out!r}")
    for x in out:
        if math.isclose(abs(x), 0.001 * 0.1 / math.sqrt(0.001), rel_tol=1e-3):
            raise Fail(
                f"ได้ก้าวราว 3.16 × lr ({out}) แปลว่ายังไม่ได้ทำ bias correction",
                f"Got steps of about 3.16 × lr ({out}): bias correction is missing",
            )
        if not math.isclose(x, -0.001, rel_tol=1e-4):
            raise Fail(f"ทั้งสองค่าควรใกล้ -0.001 แต่ได้ {out}", f"Both values should be close to -0.001, got {out}")


@check("second-step", th="เกรเดียนต์คงที่ ขยับก้าวละราว lr", en="Constant gradient moves about lr per step")
def _(sol):
    opt = _cls(sol)(lr=0.01)
    p = [1.0]
    for _ in range(2):
        p = opt.step(p, [5.0])
    if not math.isclose(p[0], 0.98, rel_tol=1e-4):
        raise Fail(
            f"เกรเดียนต์ 5.0 สองก้าวด้วย lr=0.01 ควรได้ราว [0.98] แต่ได้ {p} (ลองเช็กว่าเพิ่ม t ทุกก้าวหรือไม่)",
            f"Two steps with gradient 5.0 and lr=0.01 should give about [0.98], got {p} (check that t grows every step)",
        )


@check("zero-grad", th="เกรเดียนต์เป็นศูนย์ไม่ทำให้เกิด nan หรือหารด้วยศูนย์", en="A zero gradient does not divide by zero or give nan")
def _(sol):
    try:
        out = _cls(sol)().step([1.5, -2.0], [0.0, 0.0])
    except ZeroDivisionError:
        raise Fail("หารด้วยศูนย์: บวก epsilon หลังถอดราก sqrt(v_hat)", "Division by zero: add epsilon after sqrt(v_hat)")
    if any(math.isnan(x) for x in out) or out != [1.5, -2.0]:
        raise Fail(f"เกรเดียนต์เป็นศูนย์ พารามิเตอร์ต้องไม่ขยับ แต่ได้ {out}", f"With a zero gradient the params must not move, got {out}")


@check("own-state", th="แต่ละตัวมีสถานะเป็นของตัวเอง", en="Each optimizer keeps its own state")
def _(sol):
    cls = _cls(sol)
    a, b = cls(lr=0.001), cls(lr=0.001)
    for _ in range(3):
        a.step([0.0], [1.0])
    out = b.step([0.0], [-1.0])
    if not math.isclose(out[0], 0.001, rel_tol=1e-4):
        raise Fail(
            "optimizer สองตัวใช้สถานะร่วมกัน ให้เก็บ m, v และ t ไว้ใน self",
            "Two optimizers share state. Keep m, v and t on self.",
        )


@check("rosenbrock", th="ลู่เข้าบนฟังก์ชัน Rosenbrock", en="Converges on the Rosenbrock function", hidden=True)
def _(sol):
    def f(p):
        x, y = p
        return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

    def grad(p):
        x, y = p
        return [-2 * (1 - x) + 200 * (y - x ** 2) * (-2 * x), 200 * (y - x ** 2)]

    opt = _cls(sol)(lr=0.01)
    p = [-1.0, 1.0]
    for _ in range(5000):
        p = opt.step(p, grad(p))
    if not f(p) < 1e-3:
        raise Fail(f"loss หลัง 5000 ก้าวควรต่ำกว่า 0.001 แต่ได้ {f(p):.4g}", f"Loss after 5000 steps should be below 0.001, got {f(p):.4g}")


@check("scale-free", th="ขยายเกรเดียนต์ 1000 เท่าแล้วก้าวแทบไม่เปลี่ยน", en="Scaling gradients by 1000 barely changes the steps", hidden=True)
def _(sol):
    cls = _cls(sol)
    a, b = cls(lr=0.01), cls(lr=0.01)
    pa, pb = [0.0], [0.0]
    for g in [1.0, -0.5, 2.0]:
        pa = a.step(pa, [g])
        pb = b.step(pb, [g * 1000])
    if not math.isclose(pa[0], pb[0], rel_tol=1e-5, abs_tol=1e-8):
        raise Fail(f"ควรได้ค่าเกือบเท่ากัน แต่ได้ {pa} กับ {pb}", f"Should be almost equal, got {pa} and {pb}")
