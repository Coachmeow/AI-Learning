import math


def _run(sol, X):
    fn = sol.get("covariance_matrix")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน covariance_matrix", "Function covariance_matrix was not found")
    return fn([list(r) for r in X])


def _same(got, want, th, en):
    ok = isinstance(got, list) and len(got) == len(want) and all(
        isinstance(g, list) and len(g) == len(w) and all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(g, w)) for g, w in zip(got, want))
    if not ok:
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("two-features", th="ข้อมูล 4x2 ที่คำนวณด้วยมือ", en="4x2 data computed by hand")
def _(sol):
    # means 2.5 and 5; deviations (-1.5, -0.5, 0.5, 1.5) and (-3, -1, 1, 3) -> 5/3, 10/3, 20/3
    _same(_run(sol, [[1, 2], [2, 4], [3, 6], [4, 8]]), [[5 / 3, 10 / 3], [10 / 3, 20 / 3]], "[[1, 2], [2, 4], [3, 6], [4, 8]]", "[[1, 2], [2, 4], [3, 6], [4, 8]]")


@check("negative", th="คุณลักษณะที่สวนทางกันได้ความแปรปรวนร่วมติดลบ", en="Features moving in opposite directions get a negative covariance")
def _(sol):
    _same(_run(sol, [[0, 3], [1, 2], [2, 1], [3, 0]]), [[5 / 3, -5 / 3], [-5 / 3, 5 / 3]], "[[0, 3], [1, 2], [2, 1], [3, 0]]", "[[0, 3], [1, 2], [2, 1], [3, 0]]")


@check("one-row", th="แถวเดียวต้อง raise ValueError", en="A single row raises ValueError")
def _(sol):
    fn = sol.get("covariance_matrix")
    try:
        got = fn([[1.0, 2.0]])
    except ValueError:
        return
    except ZeroDivisionError:
        raise Fail("แถวเดียวทำให้เกิด ZeroDivisionError แต่ต้อง raise ValueError", "A single row gave ZeroDivisionError; it must raise ValueError")
    raise Fail(f"แถวเดียวต้อง raise ValueError แต่ได้ {got!r}", f"A single row must raise ValueError, got {got!r}")


@check("three-features", th="ข้อมูล 5x3 เทียบกับสูตร", en="5x3 data against the formula", hidden=True)
def _(sol):
    X = [[2.0, 0.5, -1.0], [4.0, 1.5, 0.0], [1.0, -0.5, 2.0], [3.0, 2.5, 1.0], [5.0, 1.0, -2.0]]
    n = len(X)
    m = [sum(r[j] for r in X) / n for j in range(3)]
    want = [[sum((r[i] - m[i]) * (r[j] - m[j]) for r in X) / (n - 1) for j in range(3)] for i in range(3)]
    _same(_run(sol, X), want, "ข้อมูล 5x3", "5x3 data")


@check("offset", th="บวกค่าคงที่ให้ทุกค่าไม่เปลี่ยนความแปรปรวนร่วม", en="Adding a constant everywhere doesn't change the covariance", hidden=True)
def _(sol):
    X = [[1, 2], [2, 4], [3, 6], [4, 8]]
    _same(_run(sol, [[a + 1000, b - 500] for a, b in X]), [[5 / 3, 10 / 3], [10 / 3, 20 / 3]], "ข้อมูลที่เลื่อน +1000 และ -500", "Data shifted by +1000 and -500")
