import math


def _fn(sol):
    fn = sol.get("profile_report")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน profile_report", "Function profile_report was not found")
    return fn


def _expect(sol, events, want, th, en):
    got = _fn(sol)(list(events))
    ok = isinstance(got, list) and len(got) == len(want) and all(
        isinstance(g, dict) and g.get("func") == w[0] and g.get("ncalls") == w[1]
        and math.isclose(g.get("tottime", -1), w[2], abs_tol=1e-9) and math.isclose(g.get("cumtime", -1), w[3], abs_tol=1e-9)
        for g, w in zip(got, want)
    )
    if not ok:
        shown = [(w[0], w[1], w[2], w[3]) for w in want]
        raise Fail(f"{th}: ควรได้ (func, ncalls, tottime, cumtime) = {shown} แต่ได้ {got!r}", f"{en}: should give (func, ncalls, tottime, cumtime) = {shown}, got {got!r}")


@check("basic", th="tottime ไม่รวมฟังก์ชันที่ถูกเรียก ส่วน cumtime รวม", en="tottime excludes callees, cumtime includes them")
def _(sol):
    events = [("call", "main", 0), ("call", "load_batch", 1), ("return", "load_batch", 3),
              ("call", "train_step", 3), ("return", "train_step", 6), ("return", "main", 7)]
    _expect(sol, events, [("main", 1, 2, 7), ("train_step", 1, 3, 3), ("load_batch", 1, 2, 2)], "main เรียก load_batch และ train_step", "main calls load_batch and train_step")


@check("repeated", th="เรียกซ้ำหลายครั้งนับ ncalls และรวมเวลา", en="Repeated calls add up ncalls and time")
def _(sol):
    events = [("call", "main", 0)]
    t = 0
    for _ in range(3):
        events += [("call", "load_batch", t), ("return", "load_batch", t + 2), ("call", "train_step", t + 2), ("return", "train_step", t + 3)]
        t += 3
    events.append(("return", "main", t))
    _expect(sol, events, [("main", 1, 0, 9), ("load_batch", 3, 6, 6), ("train_step", 3, 3, 3)], "ลูป 3 รอบ (การโหลดข้อมูลกินเวลา 2 ใน 3)", "A 3-step loop (loading takes 2 of every 3)")


@check("nested", th="เวลาของหลาน ถูกหักจากลูกเท่านั้น ไม่ใช่จากปู่", en="A grandchild's time comes off its parent only, not the grandparent")
def _(sol):
    events = [("call", "main", 0), ("call", "train_step", 0), ("call", "forward", 1), ("return", "forward", 4),
              ("return", "train_step", 5), ("return", "main", 6)]
    _expect(sol, events, [("main", 1, 1, 6), ("train_step", 1, 2, 5), ("forward", 1, 3, 3)], "main → train_step → forward", "main → train_step → forward")


@check("recursion", th="ฟังก์ชันเรียกตัวเองไม่นับ cumtime ซ้ำ", en="Recursion does not double-count cumtime", hidden=True)
def _(sol):
    events = [("call", "walk", 0), ("call", "walk", 1), ("return", "walk", 3), ("return", "walk", 4)]
    _expect(sol, events, [("walk", 2, 4, 4)], "walk เรียกตัวเอง", "walk calls itself")


@check("ties", th="cumtime เท่ากันเรียงตามชื่อ", en="Equal cumtime is ordered by name", hidden=True)
def _(sol):
    events = [("call", "zeta", 0), ("return", "zeta", 2), ("call", "alpha", 2), ("return", "alpha", 4)]
    _expect(sol, events, [("alpha", 1, 2, 2), ("zeta", 1, 2, 2)], "สองฟังก์ชันใช้เวลาเท่ากัน", "Two functions with the same time")


@check("mismatch", th="return ที่ไม่ตรงกับ stack ต้อง raise ValueError", en="A return that doesn't match the stack raises ValueError", hidden=True)
def _(sol):
    try:
        got = _fn(sol)([("call", "main", 0), ("call", "load", 1), ("return", "main", 2)])
    except ValueError:
        return
    raise Fail(f"return ของ main ขณะที่ load ยังไม่คืนค่า ต้อง raise ValueError แต่ได้ {got!r}", f"Returning from main while load is still running must raise ValueError, got {got!r}")
