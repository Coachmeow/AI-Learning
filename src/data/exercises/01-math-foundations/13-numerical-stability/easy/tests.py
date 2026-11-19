import math


def _run(sol, g, m):
    fn = sol.get("clip_by_norm")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน clip_by_norm", "Function clip_by_norm was not found")
    return fn(list(g), m)


def _same(got, want, th, en):
    if not isinstance(got, list) or len(got) != len(want) or not all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(got, want)):
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("three-four", th="[3, 4] กับ max_norm 1 ได้ [0.6, 0.8]", en="[3, 4] with max_norm 1 gives [0.6, 0.8]")
def _(sol):
    _same(_run(sol, [3.0, 4.0], 1.0), [0.6, 0.8], "[3, 4], 1.0", "[3, 4], 1.0")


@check("lesson", th="[10, 20, 30] กับ max_norm 5: นอร์มเป็น 5 และทิศเหมือนเดิม", en="[10, 20, 30] with max_norm 5: norm 5, same direction")
def _(sol):
    n = math.sqrt(1400)
    _same(_run(sol, [10.0, 20.0, 30.0], 5.0), [10 * 5 / n, 20 * 5 / n, 30 * 5 / n], "[10, 20, 30], 5.0", "[10, 20, 30], 5.0")


@check("small", th="นอร์มไม่เกินเกณฑ์: ไม่เปลี่ยน", en="A norm under the limit is left unchanged")
def _(sol):
    _same(_run(sol, [0.3, -0.4], 1.0), [0.3, -0.4], "[0.3, -0.4], 1.0", "[0.3, -0.4], 1.0")
