import math


def _fn(sol, name):
    fn = sol.get(name)
    if fn is None:
        raise Fail(f"ไม่พบฟังก์ชัน {name}", f"Function {name} was not found")
    return fn


def _same(got, want, th, en):
    if not isinstance(got, list) or len(got) != len(want) or not all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(got, want)):
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("exercise-3", th="แบบฝึกหัดที่ 3: x = [1, 2, 3, 4, 0, 0, 0, 0], h = [1, 1, 1, 0, ...] ได้ [1, 3, 6, 9, 7, 4, 0, 0]", en="Exercise 3: x = [1, 2, 3, 4, 0, 0, 0, 0], h = [1, 1, 1, 0, ...] gives [1, 3, 6, 9, 7, 4, 0, 0]")
def _(sol):
    got = _fn(sol, "circular_convolution")([1, 2, 3, 4, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0])
    _same(got, [1, 3, 6, 9, 7, 4, 0, 0], "คอนโวลูชันแบบวงกลม", "Circular convolution")


@check("wraparound", th="เมื่อสัญญาณเต็มความยาว ค่าวนรอบ: [1, 2, 3, 4] กับ [1, 1, 0, 0] ได้ [5, 3, 5, 7]", en="When the signal fills the length it wraps: [1, 2, 3, 4] with [1, 1, 0, 0] gives [5, 3, 5, 7]")
def _(sol):
    got = _fn(sol, "circular_convolution")([1, 2, 3, 4], [1, 1, 0, 0])
    _same(got, [5, 3, 5, 7], "การวนรอบ", "Wraparound")


@check("direction", th="h ที่ไม่สมมาตร [0, 1, 0, 0] เลื่อนสัญญาณไปทางขวาหนึ่งช่อง", en="The asymmetric h = [0, 1, 0, 0] shifts the signal one step to the right")
def _(sol):
    got = _fn(sol, "circular_convolution")([1, 2, 3, 4], [0, 1, 0, 0])
    _same(got, [4, 1, 2, 3], "ทิศของคอนโวลูชัน", "Convolution direction")


@check("lengths", th="ความยาวไม่เท่ากันต้อง raise ValueError", en="Different lengths must raise ValueError")
def _(sol):
    try:
        got = _fn(sol, "circular_convolution")([1, 2, 3], [1, 1])
    except ValueError:
        return
    except Exception as e:
        raise Fail(f"ควร raise ValueError แต่เกิด {type(e).__name__}: {e}", f"Should raise ValueError, got {type(e).__name__}: {e}")
    raise Fail(f"ควร raise ValueError แต่คืน {got!r}", f"Should raise ValueError, returned {got!r}")


@check("linear", th="คอนโวลูชันเชิงเส้นของ [1, 2, 3, 4] กับ [1, 1, 1] ได้ [1, 3, 6, 9, 7, 4]", en="The linear convolution of [1, 2, 3, 4] and [1, 1, 1] is [1, 3, 6, 9, 7, 4]")
def _(sol):
    _same(_fn(sol, "linear_convolution")([1, 2, 3, 4], [1, 1, 1]), [1, 3, 6, 9, 7, 4], "คอนโวลูชันเชิงเส้น", "Linear convolution")


@check("linear-no-wrap", th="คอนโวลูชันเชิงเส้นไม่วนรอบ: [1, 2, 3, 4] กับ [1, 1] ได้ [1, 3, 5, 7, 4]", en="Linear convolution does not wrap: [1, 2, 3, 4] with [1, 1] gives [1, 3, 5, 7, 4]")
def _(sol):
    _same(_fn(sol, "linear_convolution")([1, 2, 3, 4], [1, 1]), [1, 3, 5, 7, 4], "ไม่วนรอบ", "No wraparound")
