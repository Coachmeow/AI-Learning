import math


def _run(sol, *args):
    fn = sol.get("metropolis")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน metropolis", "Function metropolis was not found")
    try:
        got = fn(*args)
    except OverflowError:
        raise Fail("เกิด OverflowError: ใช้ exp(min(0, delta)) แทน exp(delta)", "OverflowError: use exp(min(0, delta)) instead of exp(delta)")
    if not isinstance(got, (tuple, list)) or len(got) != 2:
        raise Fail(f"ต้องคืน (chain, acceptance_rate) แต่ได้ {got!r}", f"Must return (chain, acceptance_rate), got {got!r}")
    return got


def _check(got, chain, rate, th, en):
    c, r = got
    if not isinstance(c, list) or len(c) != len(chain) or not all(math.isclose(a, b, abs_tol=1e-12) for a, b in zip(c, chain)):
        raise Fail(f"{th}: chain ควรเป็น {chain} แต่ได้ {c!r}", f"{en}: the chain should be {chain}, got {c!r}")
    if not isinstance(r, (int, float)) or not math.isclose(r, rate, abs_tol=1e-12):
        raise Fail(f"{th}: acceptance_rate ควรเป็น {rate} แต่ได้ {r!r}", f"{en}: the acceptance rate should be {rate}, got {r!r}")


def _normal(x):
    return -x * x / 2


def _unit(x):
    return 0.0 if 0.0 <= x <= 1.0 else float("-inf")


@check("trace", th="ไล่ด้วยมือบนการแจกแจงปกติมาตรฐาน", en="A hand-traced chain on the standard normal")
def _(sol):
    # 0 -> 1 (u 0.5 < e^-0.5), -> 0.5 (uphill), -> 2.5 (u 0.01 < e^-3), stays (u 0.99 > e^-0.255)
    got = _run(sol, _normal, 0.0, [1.0, -0.5, 2.0, 0.1], [0.5, 0.9, 0.01, 0.99])
    _check(got, [1.0, 0.5, 2.5, 2.5], 0.75, "การแจกแจงปกติ", "Standard normal")


@check("support", th="จุดนอก support ถูกปฏิเสธเสมอ แม้ u = 0.0", en="A point outside the support is always rejected, even with u = 0.0")
def _(sol):
    got = _run(sol, _unit, 0.5, [0.7, -0.2, 0.3], [0.0, 0.5, 0.5])
    _check(got, [0.5, 0.3, 0.6], 2 / 3, "Uniform(0, 1)", "Uniform(0, 1)")


@check("steep-uphill", th="ขึ้นเขาชันมาก (delta = 1000) ต้องไม่ล้น", en="A very steep uphill move (delta = 1000) must not overflow", hidden=True)
def _(sol):
    got = _run(sol, lambda x: 1000.0 * x, 0.0, [1.0, -1.0], [0.5, 0.5])
    _check(got, [1.0, 1.0], 0.5, "log_target = 1000x", "log_target = 1000x")


@check("errors", th="เริ่มนอก support หรือความยาวไม่เท่ากันต้อง raise ValueError", en="A start outside the support or mismatched lengths raise ValueError", hidden=True)
def _(sol):
    fn = sol.get("metropolis")
    for args in ((_unit, 2.0, [0.1], [0.5]), (_normal, 0.0, [0.1, 0.2], [0.5])):
        try:
            got = fn(*args)
        except ValueError:
            continue
        raise Fail(f"x0 = {args[1]}, steps {args[2]}, uniforms {args[3]} ต้อง raise ValueError แต่ได้ {got!r}", f"x0 = {args[1]}, steps {args[2]}, uniforms {args[3]} must raise ValueError, got {got!r}")
