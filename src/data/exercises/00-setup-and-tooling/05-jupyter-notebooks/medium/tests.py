def _code(n):
    return {"cell_type": "code", "execution_count": n, "source": ""}


MD = {"cell_type": "markdown", "source": "notes"}


def _fn(sol):
    fn = sol.get("run_order_report")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน run_order_report", "Function run_order_report was not found")
    return fn


def _expect(sol, counts_or_cells, want):
    cells = [c if isinstance(c, dict) else _code(c) for c in counts_or_cells]
    got = _fn(sol)({"cells": cells})
    shown = [c["execution_count"] if c.get("cell_type") == "code" else "md" for c in cells]
    if not isinstance(got, dict) or list(got.get("not_run", ())) != want["not_run"] or list(got.get("out_of_order", ())) != want["out_of_order"]:
        raise Fail(f"เซลล์ {shown} ควรได้ {want} แต่ได้ {got!r}", f"Cells {shown} should give {want}, got {got!r}")


@check("clean", th="รันจากบนลงล่างครบ ไม่มีปัญหา", en="A clean top-to-bottom run has no problems")
def _(sol):
    _expect(sol, [1, 2, 3, 4], {"not_run": [], "out_of_order": []})


@check("lesson-example", th="ตัวเลข [3], [1], [7], [2]", en="Counters [3], [1], [7], [2]")
def _(sol):
    _expect(sol, [3, 1, 7, 2], {"not_run": [], "out_of_order": [1, 3]})


@check("largest-so-far", th="เทียบกับค่ามากที่สุดที่ผ่านมา ไม่ใช่แค่เซลล์ก่อนหน้า", en="Compares with the largest so far, not only the previous cell")
def _(sol):
    _expect(sol, [1, 5, 2, 3], {"not_run": [], "out_of_order": [2, 3]})


@check("not-run", th="แยกเซลล์ที่ยังไม่รันออกมา และไม่นับเป็นค่ามากที่สุด", en="Lists never-run cells and does not count them as the largest")
def _(sol):
    _expect(sol, [1, None, 2, None], {"not_run": [1, 3], "out_of_order": []})


@check("markdown", th="ไม่สนเซลล์ markdown แต่ใช้ index จริงใน nb['cells']", en="Ignores markdown cells but uses real indexes in nb['cells']")
def _(sol):
    _expect(sol, [MD, 2, MD, 1, None], {"not_run": [4], "out_of_order": [3]})


@check("repeat", th="ตัวเลขซ้ำกันนับว่าไม่ตามลำดับ", en="A repeated number counts as out of order")
def _(sol):
    _expect(sol, [1, 2, 2], {"not_run": [], "out_of_order": [2]})
