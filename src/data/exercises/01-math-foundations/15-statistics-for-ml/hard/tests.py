import math
from fractions import Fraction
from itertools import product


def _run(sol, a, b):
    fn = sol.get("paired_permutation_test")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน paired_permutation_test", "Function paired_permutation_test was not found")
    return fn(list(a), list(b))


def _is(sol, a, b, want, th, en):
    got = _run(sol, a, b)
    if not isinstance(got, (int, float)) or not math.isclose(got, want, abs_tol=1e-12):
        raise Fail(f"{th}: p ควรเป็น {want} แต่ได้ {got!r}", f"{en}: p should be {want}, got {got!r}")


def _exact(d_strs):
    d = [Fraction(s) for s in d_strs]
    obs = abs(sum(d))
    return sum(1 for signs in product([1, -1], repeat=len(d)) if abs(sum(s * x for s, x in zip(signs, d))) >= obs) / 2 ** len(d)


@check("five-folds", th="B ชนะทั้ง 5 fold: p = 2/32 = 0.0625", en="B wins all 5 folds: p = 2/32 = 0.0625")
def _(sol):
    a = [0.80, 0.85, 0.90, 0.82, 0.88]
    _is(sol, a, [x + d for x, d in zip(a, [0.01, 0.012, 0.008, 0.011, 0.009])], 2 / 32, "5 fold", "5 folds")


@check("balanced", th="ผลต่าง [1, -1, 1, -1]: ผลรวมเป็น 0 จึงได้ p = 1", en="Differences [1, -1, 1, -1]: the sum is 0, so p = 1")
def _(sol):
    _is(sol, [0, 0, 0, 0], [1, -1, 1, -1], 1.0, "[1, -1, 1, -1]", "[1, -1, 1, -1]")


@check("mixed", th="ผลต่างที่มีทั้งบวกและลบ", en="Differences with both signs")
def _(sol):
    d = ["3", "1", "-2", "4", "2", "5"]
    _is(sol, [0] * 6, [int(x) for x in d], _exact(d), "[3, 1, -2, 4, 2, 5]", "[3, 1, -2, 4, 2, 5]")


@check("rounding-tie", th="ผลรวมที่เท่ากันแต่ต่างกันจากการปัดเศษต้องถูกนับ", en="Sums equal up to rounding must be counted", hidden=True)
def _(sol):
    d = ["-0.4", "-0.8", "0.6", "0.2"]
    _is(sol, [0.0] * 4, [float(x) for x in d], _exact(d), "[-0.4, -0.8, 0.6, 0.2]", "[-0.4, -0.8, 0.6, 0.2]")


@check("ten-folds", th="10 fold ที่ B ชนะทุก fold: p = 2/1024", en="10 folds all won by B: p = 2/1024", hidden=True)
def _(sol):
    _is(sol, [0.5] * 10, [0.5 + 0.01 * (i + 1) for i in range(10)], 2 / 1024, "10 fold", "10 folds")


@check("errors", th="ความยาวไม่เท่ากัน ว่าง หรือเกิน 16 ต้อง raise ValueError", en="Different lengths, empty input or more than 16 raise ValueError", hidden=True)
def _(sol):
    fn = sol.get("paired_permutation_test")
    for a, b in (([1, 2], [1]), ([], []), ([0] * 17, [1] * 17)):
        try:
            got = fn(a, b)
        except ValueError:
            continue
        raise Fail(f"paired_permutation_test(ยาว {len(a)} และ {len(b)}) ต้อง raise ValueError แต่ได้ {got!r}", f"paired_permutation_test(lengths {len(a)} and {len(b)}) must raise ValueError, got {got!r}")
