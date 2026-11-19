def _run(sol, s, e):
    fn = sol.get("rank_for_error")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน rank_for_error", "Function rank_for_error was not found")
    return fn(list(s), e)


def _is(got, want, th, en):
    if got != want:
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("unsorted", th="[3, 4] (ไม่เรียง): แรงก์ 1 ผิดพลาด 3/5 = 0.6", en="[3, 4] (unsorted): rank 1 has error 3/5 = 0.6")
def _(sol):
    _is(_run(sol, [3, 4], 0.6), 1, "max 0.6", "max 0.6")
    _is(_run(sol, [3, 4], 0.5), 2, "max 0.5", "max 0.5")


@check("squares", th="[10, 1, 1, 1] กับ 0.2 ต้องใช้กำลังสอง", en="[10, 1, 1, 1] with 0.2 needs the squares")
def _(sol):
    # rank 1: sqrt(3) / sqrt(103) ≈ 0.171 <= 0.2; with plain sums it would be 3 / 13 ≈ 0.23
    _is(_run(sol, [10, 1, 1, 1], 0.2), 1, "[10, 1, 1, 1], 0.2", "[10, 1, 1, 1], 0.2")


@check("everything", th="ยอมให้ผิดพลาดได้ 100% ได้แรงก์ 0", en="Allowing 100% error gives rank 0")
def _(sol):
    _is(_run(sol, [5, 2], 1.0), 0, "max 1.0", "max 1.0")


@check("zeros", th="ค่าเอกฐานศูนย์ทั้งหมดคืน 0", en="All-zero singular values return 0", hidden=True)
def _(sol):
    _is(_run(sol, [0, 0, 0], 0.1), 0, "[0, 0, 0]", "[0, 0, 0]")


@check("negative", th="ค่าที่ติดลบต้อง raise ValueError", en="A negative value raises ValueError", hidden=True)
def _(sol):
    fn = sol.get("rank_for_error")
    try:
        got = fn([3, -1], 0.5)
    except ValueError:
        return
    raise Fail(f"[3, -1] ต้อง raise ValueError แต่ได้ {got!r}", f"[3, -1] must raise ValueError, got {got!r}")


@check("exact-rank", th="ข้อมูลแรงก์ 3 ที่ max_rel_error = 0", en="Rank-3 data with max_rel_error = 0", hidden=True)
def _(sol):
    _is(_run(sol, [0, 7, 0.5, 3, 0], 0), 3, "[0, 7, 0.5, 3, 0], 0", "[0, 7, 0.5, 3, 0], 0")
