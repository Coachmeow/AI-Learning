import math

R = 1 / math.sqrt(2)
TERMS = [(5.0, [R, R], [1.0, 0.0, 0.0]), (2.0, [R, -R], [0.0, 1.0, 0.0])]


def _run(sol, terms, k):
    fn = sol.get("low_rank")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน low_rank", "Function low_rank was not found")
    return fn(terms, k)


def _same(got, want, th, en):
    ok = isinstance(got, list) and len(got) == len(want) and all(
        len(g) == len(w) and all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(g, w)) for g, w in zip(got, want))
    if not ok:
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("rank-1", th="แรงก์ 1: 5 * u1 * v1^T (ขนาด 2x3)", en="Rank 1: 5 * u1 * v1^T (2x3)")
def _(sol):
    _same(_run(sol, TERMS, 1), [[5 * R, 0, 0], [5 * R, 0, 0]], "k = 1", "k = 1")


@check("rank-2", th="แรงก์ 2: รวมสองพจน์", en="Rank 2: the sum of both terms")
def _(sol):
    _same(_run(sol, TERMS, 2), [[5 * R, 2 * R, 0], [5 * R, -2 * R, 0]], "k = 2", "k = 2")


@check("rank-0", th="k = 0 ได้เมทริกซ์ศูนย์", en="k = 0 gives the zero matrix")
def _(sol):
    _same(_run(sol, TERMS, 0), [[0, 0, 0], [0, 0, 0]], "k = 0", "k = 0")
