import math


def _fn(sol):
    fn = sol.get("fiedler_split")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน fiedler_split", "Function fiedler_split was not found")
    return fn


def _run(sol, n, edges, labels, value, th, en):
    got = _fn(sol)(n, list(edges))
    if not isinstance(got, (tuple, list)) or len(got) != 2:
        raise Fail(f"ต้องคืน (labels, fiedler_value) แต่ได้ {got!r}", f"Must return (labels, fiedler_value), got {got!r}")
    lab, val = got
    if labels is not None and list(lab) != labels:
        raise Fail(f"{th}: labels ควรเป็น {labels} แต่ได้ {lab!r}", f"{en}: labels should be {labels}, got {lab!r}")
    if not isinstance(val, (int, float)) or not math.isclose(val, value, abs_tol=1e-6):
        raise Fail(f"{th}: ค่า Fiedler ควรเป็น {value} แต่ได้ {val!r}", f"{en}: the Fiedler value should be {value}, got {val!r}")


def _raises(sol, n, edges, th, en):
    try:
        got = _fn(sol)(n, list(edges))
    except ValueError:
        return
    except Exception as e:
        raise Fail(f"{th}: ควร raise ValueError แต่เกิด {type(e).__name__}: {e}", f"{en}: should raise ValueError, got {type(e).__name__}: {e}")
    raise Fail(f"{th}: ควร raise ValueError แต่คืน {got!r}", f"{en}: should raise ValueError, returned {got!r}")


_BRIDGED = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (2, 3)]


@check("bridged", th="สามเหลี่ยมสองรูปที่เชื่อมด้วย 2 – 3: แบ่งเป็น {0, 1, 2} กับ {3, 4, 5}, λ₂ ≈ 0.438447", en="Two triangles joined by 2 – 3: split into {0, 1, 2} and {3, 4, 5}, λ₂ ≈ 0.438447")
def _(sol):
    _run(sol, 6, _BRIDGED, [0, 0, 0, 1, 1, 1], 0.438447, "สามเหลี่ยมสองรูป", "Two triangles")


@check("path", th="เส้นทาง 6 โหนด: แบ่งตรงกลาง λ₂ = 2 - 2cos(π/6) ≈ 0.267949", en="A 6-node path: split in the middle, λ₂ = 2 - 2cos(π/6) ≈ 0.267949")
def _(sol):
    _run(sol, 6, [(i, i + 1) for i in range(5)], [0, 0, 0, 1, 1, 1], 0.267949, "เส้นทาง 6 โหนด", "6-node path")


@check("disconnected", th="กราฟที่ไม่เชื่อมต่อกันต้อง raise ValueError", en="A disconnected graph must raise ValueError")
def _(sol):
    _raises(sol, 6, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)], "สามเหลี่ยมสองรูปที่แยกกัน", "Two separate triangles")


@check("cliques", th="K₅ สองกลุ่มที่เชื่อมกันด้วยสองเส้น: λ₂ ≈ 0.627719", en="Two K₅ joined by two edges: λ₂ ≈ 0.627719", hidden=True)
def _(sol):
    edges = [(i, j) for i in range(5) for j in range(i + 1, 5)]
    edges += [(i + 5, j + 5) for i in range(5) for j in range(i + 1, 5)]
    edges += [(0, 5), (1, 6)]
    _run(sol, 10, edges, [0] * 5 + [1] * 5, 0.627719, "K₅ สองกลุ่ม", "Two K₅")


@check("complete", th="กราฟบริบูรณ์ K₄ มี λ₂ = 4", en="The complete graph K₄ has λ₂ = 4", hidden=True)
def _(sol):
    _run(sol, 4, [(i, j) for i in range(4) for j in range(i + 1, 4)], None, 4.0, "K₄", "K₄")


@check("tiny", th="n = 1 ต้อง raise ValueError", en="n = 1 must raise ValueError", hidden=True)
def _(sol):
    _raises(sol, 1, [], "n = 1", "n = 1")
