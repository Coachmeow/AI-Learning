import math

NAN, INF = float("nan"), float("inf")


def _fn(sol):
    fn = sol.get("value_stats")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน value_stats", "Function value_stats was not found")
    return fn


def _same(a, b):
    if a is None or b is None:
        return a is b
    if isinstance(b, bool):
        return a is b
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)


def _expect(sol, values, want):
    got = _fn(sol)(list(values))
    if not isinstance(got, dict) or any(not _same(got.get(k), v) for k, v in want.items()):
        raise Fail(f"value_stats({values!r}) ควรได้ {want} แต่ได้ {got!r}", f"value_stats({values!r}) should give {want}, got {got!r}")


@check("clean", th="ค่าปกติไม่มี NaN", en="Ordinary values without NaN")
def _(sol):
    _expect(sol, [0.5, -1.5, 2.0], {"count": 3, "has_nan": False, "has_inf": False, "min": -1.5, "max": 2.0, "mean": 1 / 3})


@check("nan-order", th="NaN อยู่ตำแหน่งไหนก็ได้ min/max ยังถูก", en="min/max stay right wherever the NaN sits")
def _(sol):
    want = {"count": 3, "has_nan": True, "has_inf": False, "min": 0.5, "max": 1.0, "mean": 0.75}
    _expect(sol, [NAN, 1.0, 0.5], want)
    _expect(sol, [1.0, NAN, 0.5], want)


@check("inf", th="inf ถูกแจ้งแต่ไม่นับในค่าเฉลี่ย", en="inf is flagged but kept out of the mean")
def _(sol):
    _expect(sol, [1.0, INF, 3.0, -INF], {"count": 4, "has_nan": False, "has_inf": True, "min": 1.0, "max": 3.0, "mean": 2.0})


@check("all-bad", th="ไม่มีค่าที่จำกัดเลย ได้ None", en="No finite values gives None")
def _(sol):
    _expect(sol, [NAN, INF], {"count": 2, "has_nan": True, "has_inf": True, "min": None, "max": None, "mean": None})
