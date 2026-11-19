def _is(sol, f, x, y, want, th, en):
    fn = sol.get("classify")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน classify", "Function classify was not found")
    got = fn(f, x, y)
    if got != want:
        raise Fail(f"{th} ที่ ({x}, {y}) ควรเป็น {want!r} แต่ได้ {got!r}", f"{en} at ({x}, {y}) should be {want!r}, got {got!r}")


@check("bowl", th="x² + y² ที่ (0, 0) เป็นค่าต่ำสุด", en="x² + y² at (0, 0) is a minimum")
def _(sol):
    _is(sol, lambda x, y: x ** 2 + y ** 2, 0.0, 0.0, "minimum", "x² + y²", "x² + y²")


@check("cap", th="-(x² + y²) ที่ (0, 0) เป็นค่าสูงสุด", en="-(x² + y²) at (0, 0) is a maximum")
def _(sol):
    _is(sol, lambda x, y: -(x ** 2 + y ** 2), 0.0, 0.0, "maximum", "-(x² + y²)", "-(x² + y²)")


@check("saddle", th="x² - y² ที่ (0, 0) เป็นจุดอานม้า", en="x² - y² at (0, 0) is a saddle")
def _(sol):
    _is(sol, lambda x, y: x ** 2 - y ** 2, 0.0, 0.0, "saddle", "x² - y²", "x² - y²")


@check("cross-term", th="x² + 4xy + y²: ทแยงมุมเป็นบวกแต่เป็นจุดอานม้า", en="x² + 4xy + y²: positive diagonal, still a saddle")
def _(sol):
    _is(sol, lambda x, y: x ** 2 + 4 * x * y + y ** 2, 0.0, 0.0, "saddle", "x² + 4xy + y²", "x² + 4xy + y²")


@check("not-critical", th="จุดที่ gradient ไม่เป็นศูนย์ต้อง raise ValueError", en="A point with a non-zero gradient raises ValueError")
def _(sol):
    fn = sol.get("classify")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน classify", "Function classify was not found")
    try:
        got = fn(lambda x, y: x ** 2 + y ** 2, 1.0, 1.0)
    except ValueError:
        return
    raise Fail(f"x² + y² ที่ (1, 1) มี gradient [2, 2] จึงต้อง raise ValueError แต่ได้ {got!r}",
               f"x² + y² at (1, 1) has gradient [2, 2], so it must raise ValueError; got {got!r}")


@check("shifted-min", th="ค่าต่ำสุดที่ (1, -2) ที่มีพจน์ไขว้", en="A minimum at (1, -2) with a cross term", hidden=True)
def _(sol):
    _is(sol, lambda x, y: (x - 1) ** 2 + (x - 1) * (y + 2) + (y + 2) ** 2, 1.0, -2.0, "minimum",
        "(x-1)² + (x-1)(y+2) + (y+2)²", "(x-1)² + (x-1)(y+2) + (y+2)²")


@check("shifted-max", th="ค่าสูงสุดที่ (2, 1)", en="A maximum at (2, 1)", hidden=True)
def _(sol):
    _is(sol, lambda x, y: 5 - (x - 2) ** 2 - 3 * (y - 1) ** 2, 2.0, 1.0, "maximum", "5 - (x-2)² - 3(y-1)²", "5 - (x-2)² - 3(y-1)²")


@check("flat", th="Hessian เป็นศูนย์: การทดสอบตัดสินไม่ได้", en="A zero Hessian: the test can't decide", hidden=True)
def _(sol):
    _is(sol, lambda x, y: x ** 4 + y ** 4, 0.0, 0.0, "unknown", "x⁴ + y⁴", "x⁴ + y⁴")
    _is(sol, lambda x, y: x ** 3 - 3 * x * y ** 2, 0.0, 0.0, "unknown", "x³ - 3xy²", "x³ - 3xy²")
