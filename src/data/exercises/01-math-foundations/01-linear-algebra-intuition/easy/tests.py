import math


def _fn(sol):
    fn = sol.get("angle_between")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน angle_between", "Function angle_between was not found")
    return fn


def _expect(fn, a, b, want):
    got = fn(a, b)
    if not isinstance(got, (int, float)) or not math.isclose(got, want, abs_tol=1e-6):
        raise Fail(f"angle_between({a}, {b}) ควรได้ {want} องศา แต่ได้ {got!r}", f"angle_between({a}, {b}) should be {want} degrees, got {got!r}")


@check("right-angle", th="[1, 0] กับ [0, 1] ทำมุม 90 องศา", en="[1, 0] and [0, 1] are 90 degrees apart")
def _(sol):
    _expect(_fn(sol), [1, 0], [0, 1], 90.0)


@check("degrees", th="คืนค่าเป็นองศา (45 และ 180)", en="Returns degrees (45 and 180)")
def _(sol):
    _expect(_fn(sol), [1, 0], [1, 1], 45.0)
    _expect(_fn(sol), [2, 0], [-3, 0], 180.0)


@check("lengths", th="ความยาวของเวกเตอร์ไม่มีผลกับมุม", en="Vector lengths don't change the angle")
def _(sol):
    _expect(_fn(sol), [3, 0], [0.5, 0.5], 45.0)


@check("clamp", th="เวกเตอร์กับตัวเองได้ 0 แม้ cosine จะเกิน 1 เล็กน้อย", en="A vector with itself gives 0, even when the cosine is a hair above 1")
def _(sol):
    try:
        _expect(_fn(sol), [1, 1, 1], [1, 1, 1], 0.0)
    except ValueError as e:
        raise Fail(f"เกิด ValueError ({e}) เพราะ cosine เป็น 1.0000000000000002 ต้องบีบค่าก่อน acos", f"ValueError ({e}) because the cosine is 1.0000000000000002; clamp it before acos")
