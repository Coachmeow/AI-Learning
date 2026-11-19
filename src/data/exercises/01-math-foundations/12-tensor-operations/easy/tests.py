def _is(sol, shape, want):
    fn = sol.get("compute_strides")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน compute_strides", "Function compute_strides was not found")
    got = fn(shape)
    if tuple(got) != want:
        raise Fail(f"compute_strides({shape}) ควรเป็น {want} แต่ได้ {got!r}", f"compute_strides({shape}) should be {want}, got {got!r}")


@check("matrix", th="(3, 4) ได้ (4, 1)", en="(3, 4) gives (4, 1)")
def _(sol):
    _is(sol, (3, 4), (4, 1))


@check("three-d", th="(2, 3, 4) ได้ (12, 4, 1)", en="(2, 3, 4) gives (12, 4, 1)")
def _(sol):
    _is(sol, (2, 3, 4), (12, 4, 1))


@check("image-batch", th="(32, 3, 224, 224) แบบ NCHW", en="(32, 3, 224, 224) in NCHW")
def _(sol):
    _is(sol, (32, 3, 224, 224), (3 * 224 * 224, 224 * 224, 224, 1))


@check("small", th="เวกเตอร์และสเกลาร์", en="A vector and a scalar")
def _(sol):
    _is(sol, (5,), (1,))
    _is(sol, (), ())
