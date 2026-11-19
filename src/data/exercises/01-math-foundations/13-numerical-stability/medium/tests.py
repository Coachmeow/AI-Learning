import math


def _run(sol, xs):
    fn = sol.get("welford")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน welford", "Function welford was not found")
    try:
        return fn(xs)
    except TypeError as e:
        raise Fail(f"เกิด TypeError: {e} (xs อาจเป็น generator ที่ใช้ len() ไม่ได้และอ่านได้รอบเดียว)", f"TypeError: {e} (xs may be a generator: no len(), and it can be read only once)")


def _near(got, want, th, en, tol=1e-9):
    if not isinstance(got, (tuple, list)) or len(got) != 2 or not all(math.isclose(a, b, rel_tol=tol, abs_tol=tol) for a, b in zip(got, want)):
        raise Fail(f"{th}: ควรได้ (mean, variance) ≈ {want} แต่ได้ {got!r}", f"{en}: should be (mean, variance) ≈ {want}, got {got!r}")


@check("lesson", th="[1000000, 1000001, 1000002]: ความแปรปรวน 2/3", en="[1000000, 1000001, 1000002]: variance 2/3")
def _(sol):
    _near(_run(sol, [1000000.0, 1000001.0, 1000002.0]), (1000001.0, 2 / 3), "ค่าเฉลี่ย 10^6", "Mean 10^6")


@check("large-mean", th="ค่าเฉลี่ยราว 10^9: สูตรตรง ๆ พัง", en="A mean near 10^9: the direct formula breaks")
def _(sol):
    _near(_run(sol, [1e9, 1e9 + 1, 1e9 + 2, 1e9 + 3]), (1e9 + 1.5, 1.25), "ค่าเฉลี่ย 10^9", "Mean 10^9")


@check("generator", th="รับ generator ที่อ่านได้รอบเดียว", en="Accepts a generator that can be read once")
def _(sol):
    _near(_run(sol, (float(v) for v in [2, 4, 4, 4, 5, 5, 7, 9])), (5.0, 4.0), "generator", "Generator")


@check("empty", th="ไม่มีค่าเลยต้อง raise ValueError", en="No values raises ValueError", hidden=True)
def _(sol):
    fn = sol.get("welford")
    try:
        got = fn([])
    except ValueError:
        return
    except ZeroDivisionError:
        raise Fail("ค่าว่างทำให้เกิด ZeroDivisionError แต่ต้อง raise ValueError", "No values gave ZeroDivisionError; it must raise ValueError")
    raise Fail(f"ค่าว่างต้อง raise ValueError แต่ได้ {got!r}", f"No values must raise ValueError, got {got!r}")


@check("single", th="ค่าเดียว: ความแปรปรวน 0", en="One value: variance 0", hidden=True)
def _(sol):
    _near(_run(sol, iter([7.5])), (7.5, 0.0), "[7.5]", "[7.5]")
