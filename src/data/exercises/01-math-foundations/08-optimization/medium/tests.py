import math


def _cls(sol):
    cls = sol.get("SGDMomentum")
    if cls is None:
        raise Fail("ไม่พบคลาส SGDMomentum", "Class SGDMomentum was not found")
    return cls


def _close(a, b, tol=1e-9):
    return len(a) == len(b) and all(math.isclose(x, y, rel_tol=tol, abs_tol=tol) for x, y in zip(a, b))


@check("first-step", th="ก้าวแรกเหมือน gradient descent", en="First step matches gradient descent")
def _(sol):
    out = _cls(sol)(lr=0.1, momentum=0.9).step([1.0], [2.0])
    if not isinstance(out, list) or not _close(out, [0.8]):
        raise Fail(
            f"ก้าวแรกความเร็วเริ่มจากศูนย์ จึงควรได้ [0.8] (1.0 - 0.1 × 2.0) แต่ได้ {out}",
            f"On the first step the velocity starts at zero, so expect [0.8] (1.0 - 0.1 × 2.0), got {out}",
        )


@check("accumulates", th="ความเร็วสะสมข้ามก้าว", en="Velocity builds up across steps")
def _(sol):
    opt = _cls(sol)(lr=0.1, momentum=0.9)
    p = opt.step([1.0], [2.0])
    p = opt.step(p, [2.0])
    if not _close(p, [0.42]):
        raise Fail(
            f"ก้าวที่สอง v = 0.9 × 2 + 2 = 3.8 จึงควรได้ [0.42] แต่ได้ {p} (ถ้าได้ [0.6] แปลว่าความเร็วถูกรีเซ็ตทุกก้าว)",
            f"On step two v = 0.9 × 2 + 2 = 3.8, so expect [0.42], got {p} (getting [0.6] means the velocity is reset every step)",
        )


@check("zero-momentum", th="momentum = 0 ทำงานเหมือน GD ธรรมดา", en="momentum = 0 behaves like plain GD")
def _(sol):
    opt = _cls(sol)(lr=0.5, momentum=0.0)
    p = opt.step([1.0, -1.0], [1.0, 1.0])
    p = opt.step(p, [1.0, 1.0])
    if not _close(p, [0.0, -2.0]):
        raise Fail(f"ควรได้ [0.0, -2.0] แต่ได้ {p}", f"Expected [0.0, -2.0], got {p}")


@check("own-state", th="แต่ละตัวมีความเร็วเป็นของตัวเอง", en="Each optimizer keeps its own velocity")
def _(sol):
    cls = _cls(sol)
    a = cls(lr=0.1, momentum=0.9)
    b = cls(lr=0.1, momentum=0.9)
    a.step([0.0], [10.0])
    out = b.step([1.0], [2.0])
    if not _close(out, [0.8]):
        raise Fail(
            "optimizer สองตัวใช้ความเร็วร่วมกัน ให้เก็บความเร็วไว้ใน self ไม่ใช่ตัวแปรของคลาส",
            "Two optimizers share one velocity. Store it on self, not on the class.",
        )


@check("rosenbrock", th="ลู่เข้าบนฟังก์ชัน Rosenbrock", en="Converges on the Rosenbrock function", hidden=True)
def _(sol):
    def f(p):
        x, y = p
        return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

    def grad(p):
        x, y = p
        return [-2 * (1 - x) + 200 * (y - x ** 2) * (-2 * x), 200 * (y - x ** 2)]

    opt = _cls(sol)(lr=0.0001, momentum=0.9)
    p = [-1.0, 1.0]
    for _ in range(5000):
        p = opt.step(p, grad(p))
    if not f(p) < 0.01:
        raise Fail(f"loss หลัง 5000 ก้าวควรต่ำกว่า 0.01 แต่ได้ {f(p):.4g}", f"Loss after 5000 steps should be below 0.01, got {f(p):.4g}")


@check("many-dims", th="ใช้กับพารามิเตอร์หลายตัวได้", en="Works with many parameters", hidden=True)
def _(sol):
    opt = _cls(sol)(lr=0.1, momentum=0.5)
    out = opt.step([1.0, 2.0, 3.0, 4.0], [1.0, 1.0, 1.0, 1.0])
    if not _close(out, [0.9, 1.9, 2.9, 3.9]):
        raise Fail(f"ควรได้ [0.9, 1.9, 2.9, 3.9] แต่ได้ {out}", f"Expected [0.9, 1.9, 2.9, 3.9], got {out}")
