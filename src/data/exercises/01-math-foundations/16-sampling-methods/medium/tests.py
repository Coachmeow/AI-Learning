import math


def _is(sol, probs, p, want, th, en):
    fn = sol.get("top_p_filter")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน top_p_filter", "Function top_p_filter was not found")
    got = fn(list(probs), p)
    ok = isinstance(got, list) and len(got) == len(want) and all(
        g[0] == w[0] and math.isclose(g[1], w[1], abs_tol=1e-9) for g, w in zip(got, want))
    if not ok:
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("lesson", th="[0.5, 0.3, 0.15, 0.05] กับ p = 0.9 เก็บ 3 ตัว", en="[0.5, 0.3, 0.15, 0.05] with p = 0.9 keeps 3")
def _(sol):
    _is(sol, [0.5, 0.3, 0.15, 0.05], 0.9, [(0, 0.5 / 0.95), (1, 0.3 / 0.95), (2, 0.15 / 0.95)], "p = 0.9", "p = 0.9")


@check("unsorted", th="ลำดับเดิมไม่ได้เรียง", en="The input is not sorted")
def _(sol):
    _is(sol, [0.1, 0.6, 0.3], 0.8, [(1, 0.6 / 0.9), (2, 0.3 / 0.9)], "[0.1, 0.6, 0.3], p = 0.8", "[0.1, 0.6, 0.3], p = 0.8")


@check("exact-threshold", th="ผลรวมเท่ากับ p พอดี: [0.5, 0.4, 0.1] กับ p = 0.9 เก็บ 2 ตัว", en="A sum exactly equal to p: [0.5, 0.4, 0.1] with p = 0.9 keeps 2")
def _(sol):
    _is(sol, [0.5, 0.4, 0.1], 0.9, [(0, 0.5 / 0.9), (1, 0.4 / 0.9)], "p = 0.9", "p = 0.9")


@check("ties-and-tiny-p", th="ความน่าจะเป็นเท่ากันเรียงตาม index และ p เล็กมากเก็บตัวเดียว", en="Equal probabilities sort by index, and a tiny p keeps one token", hidden=True)
def _(sol):
    _is(sol, [0.2, 0.4, 0.4], 0.5, [(1, 0.5), (2, 0.5)], "[0.2, 0.4, 0.4], p = 0.5", "[0.2, 0.4, 0.4], p = 0.5")
    _is(sol, [0.2, 0.5, 0.3], 0.01, [(1, 1.0)], "p = 0.01", "p = 0.01")


@check("keep-all", th="p = 1.0 กับ [0.1] * 10 (ผลรวม 0.9999999999999999) เก็บทั้งหมด", en="p = 1.0 with [0.1] * 10 (the sum is 0.9999999999999999) keeps them all", hidden=True)
def _(sol):
    _is(sol, [0.1] * 10, 1.0, [(i, 0.1 / sum([0.1] * 10)) for i in range(10)], "[0.1] * 10, p = 1.0", "[0.1] * 10, p = 1.0")
