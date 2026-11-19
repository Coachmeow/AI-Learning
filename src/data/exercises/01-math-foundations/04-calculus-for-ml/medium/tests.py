import math


def _fit(sol, *args, **kw):
    fn = sol.get("fit_line")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน fit_line", "Function fit_line was not found")
    got = fn(*args, **kw)
    if not isinstance(got, (tuple, list)) or len(got) != 2:
        raise Fail(f"ต้องคืน (w, b) แต่ได้ {got!r}", f"Must return (w, b), got {got!r}")
    return got


def _near(got, want, tol, th, en):
    if not all(math.isclose(g, w, abs_tol=tol) for g, w in zip(got, want)):
        raise Fail(f"{th}: ควรได้ประมาณ {want} แต่ได้ {tuple(got)}", f"{en}: should be about {want}, got {tuple(got)}")


@check("one-epoch", th="หนึ่ง epoch จาก (0, 0) ได้ค่าที่คำนวณด้วยมือ", en="One epoch from (0, 0) gives the hand-computed values")
def _(sol):
    _near(_fit(sol, [1.0, 2.0, 3.0], [3.0, 5.0, 7.0], lr=0.01, epochs=1), (0.68 / 3, 0.1), 1e-9,
          "หนึ่ง epoch (dw = -68/3, db = -10)", "One epoch (dw = -68/3, db = -10)")


@check("converges", th="ข้อมูล y = 2x + 1 ลู่เข้าสู่ w = 2, b = 1", en="Data on y = 2x + 1 converges to w = 2, b = 1")
def _(sol):
    _near(_fit(sol, [1.0, 2.0, 3.0, 4.0, 5.0], [3.0, 5.0, 7.0, 9.0, 11.0], lr=0.01, epochs=5000), (2.0, 1.0), 1e-3,
          "y = 2x + 1", "y = 2x + 1")


@check("zero-epochs", th="0 epoch คืนค่าเริ่มต้น (0, 0)", en="Zero epochs returns the start (0, 0)")
def _(sol):
    _near(_fit(sol, [1.0, 2.0], [3.0, 5.0], lr=0.01, epochs=0), (0.0, 0.0), 0, "epochs = 0", "epochs = 0")


@check("two-epochs", th="สอง epoch ตรงกับการอัปเดตแบบทั้ง batch", en="Two epochs match full-batch updates", hidden=True)
def _(sol):
    xs, ys, lr = [1.0, 2.0, 3.0], [3.0, 5.0, 7.0], 0.01
    w = b = 0.0
    for _ in range(2):
        errs = [w * x + b - y for x, y in zip(xs, ys)]
        dw = sum(2 * e * x for e, x in zip(errs, xs)) / 3
        db = sum(2 * e for e in errs) / 3
        w, b = w - lr * dw, b - lr * db
    _near(_fit(sol, xs, ys, lr=lr, epochs=2), (w, b), 1e-12, "สอง epoch", "Two epochs")


@check("negative", th="ความชันติดลบ: y = -3x + 4", en="A negative slope: y = -3x + 4", hidden=True)
def _(sol):
    xs = [-2.0, -1.0, 0.0, 1.0, 2.0]
    _near(_fit(sol, xs, [-3 * x + 4 for x in xs], lr=0.05, epochs=500), (-3.0, 4.0), 1e-6, "y = -3x + 4", "y = -3x + 4")
