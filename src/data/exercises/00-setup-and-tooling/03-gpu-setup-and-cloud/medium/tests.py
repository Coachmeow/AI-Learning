def _fn(sol):
    fn = sol.get("best_dtype")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน best_dtype", "Function best_dtype was not found")
    return fn


def _expect(fn, args, want):
    got = fn(*args)
    if got != want:
        call = ", ".join(repr(a) for a in args)
        raise Fail(f"best_dtype({call}) ควรได้ {want!r} แต่ได้ {got!r}", f"best_dtype({call}) should be {want!r}, got {got!r}")


@check("precise", th="เลือกชนิดที่ละเอียดที่สุดที่ใส่ได้", en="Picks the most precise type that fits")
def _(sol):
    _expect(_fn(sol), (1_000_000_000, 8), "fp32")
    _expect(_fn(sol), (7_000_000_000, 24), "fp16")


@check("margin", th="เผื่อที่ตาม margin: 7B fp16 (14 GB) ไม่พอใน 16 GB ที่เผื่อ 20%", en="Keeps the margin: 7B in fp16 (14 GB) does not fit 16 GB with 20% kept free")
def _(sol):
    _expect(_fn(sol), (7_000_000_000, 16), "int8")
    _expect(_fn(sol), (7_000_000_000, 16, 0.0), "fp16")


@check("none", th="ไม่มีชนิดไหนใส่ได้ คืน None", en="Returns None when nothing fits")
def _(sol):
    _expect(_fn(sol), (70_000_000_000, 24), None)


@check("exact", th="ขนาดเท่างบพอดีถือว่าใส่ได้", en="Weights exactly equal to the budget fit")
def _(sol):
    _expect(_fn(sol), (4_000_000_000, 10, 0.2), "fp16")


@check("bad-margin", th="margin นอกช่วง [0, 1) ต้อง raise ValueError", en="A margin outside [0, 1) raises ValueError")
def _(sol):
    for bad in (1.0, -0.1, 1.5):
        try:
            got = _fn(sol)(1_000_000_000, 8, bad)
        except ValueError:
            continue
        raise Fail(f"margin={bad} ต้อง raise ValueError แต่ได้ {got!r}", f"margin={bad} must raise ValueError, got {got!r}")
