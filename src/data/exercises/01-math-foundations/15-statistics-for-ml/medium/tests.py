import math


def _run(sol, x, y):
    fn = sol.get("spearman")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน spearman", "Function spearman was not found")
    return fn(list(x), list(y))


def _near(sol, x, y, want, th, en):
    got = _run(sol, x, y)
    if not isinstance(got, (int, float)) or not math.isclose(got, want, abs_tol=1e-9):
        raise Fail(f"{th}: ควรได้ {want:.6f} แต่ได้ {got!r}", f"{en}: should be {want:.6f}, got {got!r}")


def _pearson(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    return sum((p - ma) * (q - mb) for p, q in zip(a, b)) / math.sqrt(sum((p - ma) ** 2 for p in a) * sum((q - mb) ** 2 for q in b))


@check("monotonic", th="y = x³ ได้ 1 (เพียร์สันได้แค่ 0.94)", en="y = x³ gives 1 (Pearson only 0.94)")
def _(sol):
    x = [1, 2, 3, 4, 5]
    _near(sol, x, [v ** 3 for v in x], 1.0, "y = x³", "y = x³")


@check("reversed", th="ลำดับกลับกันได้ -1", en="A reversed order gives -1")
def _(sol):
    _near(sol, [3, 1, 4, 1.5, 9], [-3, -1, -4, -1.5, -9], -1.0, "y = -x", "y = -x")


@check("ties", th="ค่าซ้ำได้อันดับเฉลี่ย", en="Ties get average ranks")
def _(sol):
    x = [10, 20, 20, 30, 40]
    y = [1, 3, 2, 5, 4]
    _near(sol, x, y, _pearson([1, 2.5, 2.5, 4, 5], [1, 3, 2, 5, 4]), "x มีค่า 20 ซ้ำ", "x has a tied 20")


@check("ties-both", th="ค่าซ้ำทั้งสองฝั่ง", en="Ties on both sides", hidden=True)
def _(sol):
    x = [1, 1, 2, 3, 3, 3]
    y = [5, 6, 6, 7, 9, 9]
    _near(sol, x, y, _pearson([1.5, 1.5, 3, 5, 5, 5], [1, 2.5, 2.5, 4, 5.5, 5.5]), "ค่าซ้ำหลายกลุ่ม", "Several tied groups")


@check("errors", th="ความยาวไม่เท่ากันหรือค่าคงที่ต้อง raise ValueError", en="Different lengths or a constant variable raise ValueError", hidden=True)
def _(sol):
    fn = sol.get("spearman")
    for x, y in (([1, 2, 3], [1, 2]), ([4, 4, 4], [1, 2, 3])):
        try:
            got = fn(x, y)
        except ValueError:
            continue
        except ZeroDivisionError:
            raise Fail(f"spearman({x}, {y}) เกิด ZeroDivisionError แต่ต้อง raise ValueError", f"spearman({x}, {y}) gave ZeroDivisionError; it must raise ValueError")
        raise Fail(f"spearman({x}, {y}) ต้อง raise ValueError แต่ได้ {got!r}", f"spearman({x}, {y}) must raise ValueError, got {got!r}")
