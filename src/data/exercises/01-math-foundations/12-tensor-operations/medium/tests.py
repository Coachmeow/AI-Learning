def _run(sol, a, b):
    fn = sol.get("broadcast_shape")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน broadcast_shape", "Function broadcast_shape was not found")
    return fn(a, b)


def _is(sol, a, b, want):
    got = _run(sol, a, b)
    if got is None or tuple(got) != want:
        raise Fail(f"broadcast_shape({a}, {b}) ควรเป็น {want} แต่ได้ {got!r}", f"broadcast_shape({a}, {b}) should be {want}, got {got!r}")


def _fails(sol, a, b):
    try:
        got = _run(sol, a, b)
    except ValueError:
        return
    raise Fail(f"broadcast_shape({a}, {b}) ต้อง raise ValueError แต่ได้ {got!r}", f"broadcast_shape({a}, {b}) must raise ValueError, got {got!r}")


@check("lesson", th="(8, 1, 6, 1) กับ (7, 1, 5) ได้ (8, 7, 6, 5)", en="(8, 1, 6, 1) with (7, 1, 5) gives (8, 7, 6, 5)")
def _(sol):
    _is(sol, (8, 1, 6, 1), (7, 1, 5), (8, 7, 6, 5))


@check("column-row", th="(3, 1) กับ (4,) ได้ (3, 4)", en="(3, 1) with (4,) gives (3, 4)")
def _(sol):
    _is(sol, (3, 1), (4,), (3, 4))
    _is(sol, (4,), (3, 1), (3, 4))


@check("incompatible", th="(3,) กับ (4,) ต้อง raise ValueError", en="(3,) with (4,) raises ValueError")
def _(sol):
    _fails(sol, (3,), (4,))


@check("bias", th="bias (768,) กับ batch (16, 128, 768)", en="A bias (768,) with a batch (16, 128, 768)")
def _(sol):
    _is(sol, (16, 128, 768), (768,), (16, 128, 768))


@check("scalar", th="สเกลาร์ () กับ (2, 3)", en="A scalar () with (2, 3)", hidden=True)
def _(sol):
    _is(sol, (), (2, 3), (2, 3))


@check("size-zero", th="(0,) กับ (1,) ได้ (0,) ไม่ใช่ (1,)", en="(0,) with (1,) gives (0,), not (1,)", hidden=True)
def _(sol):
    _is(sol, (0,), (1,), (0,))
    _is(sol, (1, 3), (0, 1), (0, 3))


@check("inner-mismatch", th="ไม่ตรงกันที่มิติด้านใน (2, 3, 4) กับ (5, 4)", en="An inner mismatch (2, 3, 4) with (5, 4)", hidden=True)
def _(sol):
    _fails(sol, (2, 3, 4), (5, 4))
