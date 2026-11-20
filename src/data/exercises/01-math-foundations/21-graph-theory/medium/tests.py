import math


def _run(sol, n, edges, want, th, en, tol=1e-6, **kw):
    fn = sol.get("pagerank")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน pagerank", "Function pagerank was not found")
    got = fn(n, list(edges), **kw)
    if not isinstance(got, list) or len(got) != n or not all(math.isclose(a, b, abs_tol=tol) for a, b in zip(got, want)):
        raise Fail(f"{th}: ควรได้ประมาณ {[round(w, 6) for w in want]} แต่ได้ {got!r}", f"{en}: should be about {[round(w, 6) for w in want]}, got {got!r}")


@check("cycle", th="วงรอบ 0 → 1 → 2 → 0 ได้ 1/3 ทุกโหนด", en="The cycle 0 → 1 → 2 → 0 gives 1/3 everywhere")
def _(sol):
    _run(sol, 3, [(0, 1), (1, 2), (2, 0)], [1 / 3] * 3, "วงรอบ", "Cycle")


@check("no-incoming", th="A ↔ B และ C → A: C ไม่มีลิงก์เข้าจึงได้แค่ 0.05", en="A ↔ B and C → A: C has no incoming links, so it gets only 0.05")
def _(sol):
    _run(sol, 3, [(0, 1), (1, 0), (2, 0)], [0.486486, 0.463514, 0.05], "C ไม่มีลิงก์เข้า", "C has no incoming links")


@check("dead-end", th="0 → 1, 0 → 2, 1 → 2: โหนด 2 เป็นทางตันและคะแนนยังรวมได้ 1", en="0 → 1, 0 → 2, 1 → 2: node 2 is a dead end and the scores still sum to 1")
def _(sol):
    _run(sol, 3, [(0, 1), (0, 2), (1, 2)], [0.197580, 0.281551, 0.520869], "มีทางตัน", "With a dead end")


@check("hub", th="ดาว: โหนด 1-4 ชี้ไปที่ 0 และ 0 ชี้กลับไปทุกโหนด", en="A star: nodes 1-4 point to 0 and 0 points back to all of them")
def _(sol):
    edges = [(i, 0) for i in range(1, 5)] + [(0, i) for i in range(1, 5)]
    _run(sol, 5, edges, [0.475676, 0.131081, 0.131081, 0.131081, 0.131081], "ดาว", "Star")
