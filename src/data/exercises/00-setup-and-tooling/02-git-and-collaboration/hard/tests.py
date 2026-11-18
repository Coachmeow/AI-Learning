FORK = {"A": [], "B": ["A"], "C": ["B"], "D": ["B"]}
# main: A-B-C-E (E merges D), experiment: D-F
MERGED = {"A": [], "B": ["A"], "C": ["B"], "D": ["B"], "E": ["C", "D"], "F": ["D"]}
# X and Y branch off B; each side merges the other: M1 = merge(X, Y), M2 = merge(Y, X)
CRISS = {"A": [], "B": ["A"], "X": ["B"], "Y": ["B"], "M1": ["X", "Y"], "M2": ["Y", "X"]}


def _fn(sol):
    fn = sol.get("merge_base")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน merge_base", "Function merge_base was not found")
    return fn


def _expect(sol, graph, a, b, want, label):
    got = _fn(sol)(graph, a, b)
    if list(got) != want:
        raise Fail(
            f"{label}: merge_base({a!r}, {b!r}) ควรได้ {want} แต่ได้ {got!r}",
            f"{label}: merge_base({a!r}, {b!r}) should be {want}, got {got!r}",
        )


@check("fork", th="สอง branch ที่แยกจาก B ได้ B", en="Two branches that split at B give B")
def _(sol):
    _expect(sol, FORK, "C", "D", ["B"], "fork")
    _expect(sol, FORK, "D", "C", ["B"], "fork")


@check("linear", th="commit ที่เป็นบรรพบุรุษของอีกตัวคือ merge base เอง", en="A commit that is an ancestor of the other is the merge base itself")
def _(sol):
    _expect(sol, FORK, "C", "B", ["B"], "linear")
    _expect(sol, FORK, "C", "C", ["C"], "same commit")


@check("after-merge", th="เดินตาม parent ทุกตัวของ merge commit", en="Follows every parent of a merge commit")
def _(sol):
    _expect(sol, MERGED, "E", "F", ["D"], "after merge")


@check("criss-cross", th="ประวัติแบบไขว้ได้ merge base 2 ตัว", en="A criss-cross history has two merge bases")
def _(sol):
    _expect(sol, CRISS, "M1", "M2", ["X", "Y"], "criss-cross")


@check("unknown", th="commit ที่ไม่รู้จักต้อง raise ValueError", en="An unknown commit raises ValueError")
def _(sol):
    try:
        got = _fn(sol)(FORK, "C", "Z")
    except ValueError:
        return
    raise Fail(f"'Z' ไม่อยู่ใน parents ต้อง raise ValueError แต่ได้ {got!r}", f"'Z' is not in parents and must raise ValueError, got {got!r}")


@check("unrelated", th="สองประวัติที่ไม่มีอะไรร่วมกันได้ []", en="Two unrelated histories give []", hidden=True)
def _(sol):
    graph = {"A": [], "B": ["A"], "P": [], "Q": ["P"]}
    _expect(sol, graph, "B", "Q", [], "unrelated")


@check("deep", th="ประวัติยาว 3000 commit ไม่ทำให้ recursion ล้น", en="A 3000-commit history doesn't overflow the recursion limit", hidden=True)
def _(sol):
    graph = {"c0": []}
    for i in range(1, 3000):
        graph[f"c{i}"] = [f"c{i - 1}"]
    graph["side"] = ["c10"]
    _expect(sol, graph, "c2999", "side", ["c10"], "deep")


@check("pure", th="ไม่แก้ dict parents ที่ส่งเข้ามา", en="Leaves the parents dict unchanged", hidden=True)
def _(sol):
    graph = {k: list(v) for k, v in MERGED.items()}
    _fn(sol)(graph, "E", "F")
    if graph != MERGED:
        raise Fail("ห้ามแก้ dict parents ที่ส่งเข้ามา", "Do not change the parents dict you are given")
