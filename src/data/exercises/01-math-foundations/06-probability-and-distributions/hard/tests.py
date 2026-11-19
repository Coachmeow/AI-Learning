import math


def _run(sol, logits, target):
    fn = sol.get("cross_entropy_with_grad")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน cross_entropy_with_grad", "Function cross_entropy_with_grad was not found")
    try:
        got = fn(list(logits), target)
    except (ValueError, OverflowError, ZeroDivisionError) as e:
        raise Fail(f"{logits}, target {target}: เกิด {type(e).__name__}: {e} (ใช้ log-sum-exp แทนการหา log ของ softmax)",
                   f"{logits}, target {target}: {type(e).__name__}: {e} (use log-sum-exp instead of the log of the softmax)")
    if not isinstance(got, (tuple, list)) or len(got) != 2 or not isinstance(got[1], list):
        raise Fail(f"ต้องคืน (loss, grad) แต่ได้ {got!r}", f"Must return (loss, grad), got {got!r}")
    return got


def _num(x, want, th, en, tol=1e-6):
    if not isinstance(x, (int, float)) or not math.isclose(x, want, abs_tol=tol):
        raise Fail(f"{th}: ควรเป็นประมาณ {want} แต่ได้ {x!r}", f"{en}: should be about {want}, got {x!r}")


def _vec(got, want, th, en, tol=1e-6):
    if len(got) != len(want) or not all(math.isclose(g, w, abs_tol=tol) for g, w in zip(got, want)):
        raise Fail(f"{th}: ควรเป็นประมาณ {want} แต่ได้ {got!r}", f"{en}: should be about {want}, got {got!r}")


@check("lesson", th="logits ของแบบฝึกหัดที่ 3 กับ target 3 ได้ loss ≈ 0.421", en="Exercise 3's logits with target 3 give a loss of about 0.421")
def _(sol):
    loss, _g = _run(sol, [2.0, 0.5, -1.0, 3.0, 0.1], 3)
    _num(loss, 0.420881, "loss", "loss")


@check("grad", th="gradient = softmax - one-hot", en="The gradient is softmax minus one-hot")
def _(sol):
    _loss, g = _run(sol, [2.0, 1.0, 0.1], 0)
    _vec(g, [0.659001 - 1, 0.242433, 0.098566], "grad", "grad")


@check("spread", th="[1000.0, -1000.0] กับ target 1 ได้ loss 2000", en="[1000.0, -1000.0] with target 1 gives a loss of 2000")
def _(sol):
    loss, g = _run(sol, [1000.0, -1000.0], 1)
    _num(loss, 2000.0, "loss", "loss")
    _vec(g, [1.0, -1.0], "grad", "grad")


@check("finite-difference", th="gradient ตรงกับผลต่างจำกัดของ loss", en="The gradient matches finite differences of the loss", hidden=True)
def _(sol):
    z, t, h = [0.3, -1.2, 2.5, 0.0], 2, 1e-6
    _loss, g = _run(sol, z, t)
    for i in range(len(z)):
        up = list(z); up[i] += h
        dn = list(z); dn[i] -= h
        est = (_run(sol, up, t)[0] - _run(sol, dn, t)[0]) / (2 * h)
        _num(g[i], est, f"grad[{i}] เทียบกับผลต่างจำกัด", f"grad[{i}] against the finite difference", tol=1e-5)


@check("no-mutation", th="ไม่แก้ list ที่ส่งเข้ามา", en="Leaves the given list unchanged", hidden=True)
def _(sol):
    fn = sol.get("cross_entropy_with_grad")
    z = [1.0, 2.0, 3.0]
    fn(z, 1)
    if z != [1.0, 2.0, 3.0]:
        raise Fail(f"logits ถูกแก้เป็น {z}", f"The logits were changed to {z}")
