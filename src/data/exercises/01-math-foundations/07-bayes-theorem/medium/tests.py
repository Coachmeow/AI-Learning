import math


def _run(sol, *args):
    fn = sol.get("update_after_tests")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน update_after_tests", "Function update_after_tests was not found")
    return fn(*args)


def _near(got, want, th, en, tol=1e-6):
    if not isinstance(got, (int, float)) or not math.isclose(got, want, abs_tol=tol):
        raise Fail(f"{th}: ควรได้ประมาณ {want:.6f} แต่ได้ {got!r}", f"{en}: should be about {want:.6f}, got {got!r}")


def _ref(p, results, sens, spec):
    for r in results:
        a, b = (sens, 1 - spec) if r else (1 - sens, spec)
        p = a * p / (a * p + b * (1 - p))
    return p


@check("two-positives", th="ผลบวกสองครั้ง (99%, ความชุก 1/10,000) ได้ประมาณ 0.495", en="Two positives (99%, prevalence 1/10,000) give about 0.495")
def _(sol):
    _near(_run(sol, 0.0001, [True, True], 0.99, 0.99), 0.495, "[True, True]", "[True, True]")


@check("negative", th="ผลบวกแล้วตามด้วยผลลบ (sensitivity 0.9, specificity 0.95)", en="A positive then a negative (sensitivity 0.9, specificity 0.95)")
def _(sol):
    _near(_run(sol, 0.1, [True, False], 0.9, 0.95), _ref(0.1, [True, False], 0.9, 0.95), "[True, False]", "[True, False]")


@check("no-results", th="ไม่มีผลตรวจคืนค่า prior", en="No results returns the prior")
def _(sol):
    _near(_run(sol, 0.3, [], 0.9, 0.95), 0.3, "[]", "[]")


@check("order", th="ลำดับของผลตรวจไม่มีผล", en="The order of the results doesn't matter", hidden=True)
def _(sol):
    want = _ref(0.05, [True, True, False], 0.8, 0.9)
    for order in ([True, True, False], [False, True, True], [True, False, True]):
        _near(_run(sol, 0.05, list(order), 0.8, 0.9), want, str(order), str(order))


@check("asymmetric", th="sensitivity กับ specificity ต่างกันมาก", en="Very different sensitivity and specificity", hidden=True)
def _(sol):
    _near(_run(sol, 0.2, [True], 0.6, 0.99), _ref(0.2, [True], 0.6, 0.99), "sensitivity 0.6, specificity 0.99", "sensitivity 0.6, specificity 0.99")
    _near(_run(sol, 0.2, [False], 0.6, 0.99), _ref(0.2, [False], 0.6, 0.99), "ผลลบ sensitivity 0.6", "negative, sensitivity 0.6")


@check("invalid", th="ค่าที่อยู่นอกช่วง [0, 1] ต้อง raise ValueError", en="Values outside [0, 1] raise ValueError", hidden=True)
def _(sol):
    fn = sol.get("update_after_tests")
    for args in ((1.5, [True], 0.9, 0.9), (0.1, [True], -0.1, 0.9), (0.1, [True], 0.9, 1.2)):
        try:
            got = fn(*args)
        except ValueError:
            continue
        raise Fail(f"update_after_tests{args} ต้อง raise ValueError แต่ได้ {got!r}", f"update_after_tests{args} must raise ValueError, got {got!r}")
