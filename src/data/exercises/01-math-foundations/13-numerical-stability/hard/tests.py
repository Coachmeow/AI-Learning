import math


def _run(sol, xs):
    fn = sol.get("neumaier_sum")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน neumaier_sum", "Function neumaier_sum was not found")
    return fn(xs)


def _is(sol, xs, want, th, en):
    got = _run(sol, xs)
    if not isinstance(got, float) or got != want:
        raise Fail(f"{th}: ควรได้ {want!r} แต่ได้ {got!r}", f"{en}: should be {want!r}, got {got!r}")


@check("tiny-steps", th="1.0 บวก 1e-16 หนึ่งหมื่นครั้ง", en="1.0 plus 1e-16 ten thousand times")
def _(sol):
    _is(sol, [1.0] + [1e-16] * 10000, 1.000000000001, "1.0 + 10000 * 1e-16", "1.0 + 10000 * 1e-16")


@check("tenths", th="0.1 สิบครั้งได้ 1.0 พอดี", en="0.1 ten times gives exactly 1.0")
def _(sol):
    _is(sol, [0.1] * 10, 1.0, "[0.1] * 10", "[0.1] * 10")


@check("big-cancel", th="[1.0, 1e100, 1.0, -1e100] ได้ 2.0 (Kahan ดั้งเดิมได้ 0.0)", en="[1.0, 1e100, 1.0, -1e100] gives 2.0 (plain Kahan gives 0.0)")
def _(sol):
    _is(sol, [1.0, 1e100, 1.0, -1e100], 2.0, "[1.0, 1e100, 1.0, -1e100]", "[1.0, 1e100, 1.0, -1e100]")


@check("empty-generator", th="ค่าว่างได้ 0.0 และรับ generator ได้", en="Empty input gives 0.0, and generators work", hidden=True)
def _(sol):
    _is(sol, [], 0.0, "[]", "[]")
    _is(sol, (x for x in [1e16, 1.0, -1e16]), 1.0, "generator [1e16, 1.0, -1e16]", "generator [1e16, 1.0, -1e16]")


@check("mixed", th="ลำดับยาวที่บวกลบสลับกันตรงกับ math.fsum", en="A long alternating sequence matches math.fsum", hidden=True)
def _(sol):
    xs = [((-1) ** i) * (10.0 ** (i % 17)) / (i + 1) for i in range(2000)]
    want = math.fsum(xs)
    got = _run(sol, xs)
    if not math.isclose(got, want, rel_tol=1e-15, abs_tol=1e-12):
        raise Fail(f"ควรได้ {want!r} (math.fsum) แต่ได้ {got!r}", f"Should be {want!r} (math.fsum), got {got!r}")
