import math


def _run(sol, df, d2f, x0, steps, want, th, en):
    fn = sol.get("newton_1d")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน newton_1d", "Function newton_1d was not found")
    got = fn(df, d2f, x0, steps)
    if not isinstance(got, list) or len(got) != len(want) or not all(math.isclose(a, w, abs_tol=1e-9) for a, w in zip(got, want)):
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("quadratic", th="5x² + 3x + 1 จาก x = 4 ถึง -0.3 ในก้าวเดียว", en="5x² + 3x + 1 from x = 4 reaches -0.3 in one step")
def _(sol):
    _run(sol, lambda x: 10 * x + 3, lambda x: 10.0, 4.0, 2, [4.0, -0.3, -0.3], "5x² + 3x + 1", "5x² + 3x + 1")


@check("quartic", th="x⁴ จาก x = 1 ลดลงทีละ 2/3 ต่อก้าว", en="x⁴ from x = 1 shrinks by 2/3 per step")
def _(sol):
    _run(sol, lambda x: 4 * x ** 3, lambda x: 12 * x ** 2, 1.0, 3, [1.0, 2 / 3, 4 / 9, 8 / 27], "x⁴", "x⁴")


@check("log", th="x - log x จาก 0.5 ลู่เข้าหา 1 อย่างรวดเร็ว", en="x - log x from 0.5 converges quickly to 1")
def _(sol):
    _run(sol, lambda x: 1 - 1 / x, lambda x: 1 / x ** 2, 0.5, 3, [0.5, 0.75, 0.9375, 0.99609375], "x - log x", "x - log x")
