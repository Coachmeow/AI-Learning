import math


def _is(sol, a, b, want, th, en):
    fn = sol.get("cosine_similarity")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน cosine_similarity", "Function cosine_similarity was not found")
    got = fn(list(a), list(b))
    if not isinstance(got, (int, float)) or not math.isclose(got, want, abs_tol=1e-9):
        raise Fail(f"{th}: ควรได้ {want:.6f} แต่ได้ {got!r}", f"{en}: should be {want:.6f}, got {got!r}")


@check("lesson", th="(1, 0) กับ (1, 1): 1/√2", en="(1, 0) and (1, 1): 1/√2")
def _(sol):
    _is(sol, (1, 0), (1, 1), 1 / math.sqrt(2), "(1, 0), (1, 1)", "(1, 0), (1, 1)")


@check("length", th="(1, 2) กับ (2, 4): ทิศเดียวกันได้ 1.0", en="(1, 2) and (2, 4): the same direction gives 1.0")
def _(sol):
    _is(sol, (1, 2), (2, 4), 1.0, "(1, 2), (2, 4)", "(1, 2), (2, 4)")


@check("opposite-perpendicular", th="ทิศตรงข้ามได้ -1 และตั้งฉากได้ 0", en="Opposite gives -1 and perpendicular gives 0")
def _(sol):
    _is(sol, (3, -1, 2), (-6, 2, -4), -1.0, "(3, -1, 2), (-6, 2, -4)", "(3, -1, 2), (-6, 2, -4)")
    _is(sol, (1, 2), (-2, 1), 0.0, "(1, 2), (-2, 1)", "(1, 2), (-2, 1)")
