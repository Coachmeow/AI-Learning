import math

TRAIN = [(1.0, 100.0), (2.0, 300.0), (3.0, 500.0)]


def _fn(sol):
    fn = sol.get("make_standardizer")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน make_standardizer", "Function make_standardizer was not found")
    return fn


def _close(got, want, th, en):
    if not isinstance(got, list) or len(got) != len(want) or not all(math.isclose(g, w, rel_tol=1e-9, abs_tol=1e-9) for g, w in zip(got, want)):
        raise Fail(f"{th}: ควรได้ {[round(w, 4) for w in want]} แต่ได้ {got!r}", f"{en}: should be {[round(w, 4) for w in want]}, got {got!r}")


@check("lesson", th="ตัวอย่างของบทเรียน: แถว train ได้ ±1.225 และ 0", en="The lesson's example: training rows give ±1.225 and 0")
def _(sol):
    st = _fn(sol)(TRAIN)
    k = math.sqrt(1.5)
    _close(st(TRAIN[0]), [-k, -k], "แถวแรก", "First row")
    _close(st(TRAIN[1]), [0.0, 0.0], "แถวกลาง", "Middle row")


@check("test-row", th="แถวของชุด test ใช้ค่าสถิติจากชุด train", en="A test row uses the training statistics")
def _(sol):
    st = _fn(sol)(TRAIN)
    _close(st((4.0, 700.0)), [math.sqrt(6), math.sqrt(6)], "(4.0, 700.0)", "(4.0, 700.0)")


@check("constant", th="คอลัมน์ค่าคงที่ใช้ตัวหาร 1 ไม่หารด้วยศูนย์", en="A constant column uses a scale of 1 instead of dividing by zero")
def _(sol):
    st = _fn(sol)([(1.0, 5.0), (3.0, 5.0)])
    _close(st((2.0, 7.0)), [0.0, 2.0], "คอลัมน์ที่สองคงที่ที่ 5", "The second column is always 5")


@check("length", th="แถวที่ยาวไม่เท่าจำนวนคอลัมน์ต้อง raise ValueError", en="A row of the wrong length raises ValueError")
def _(sol):
    st = _fn(sol)(TRAIN)
    try:
        got = st((1.0,))
    except ValueError:
        return
    raise Fail(f"standardize((1.0,)) มีค่าเดียวแต่มี 2 คอลัมน์ ต้อง raise ValueError แต่ได้ {got!r}", f"standardize((1.0,)) has one value for 2 columns and must raise ValueError, got {got!r}")


@check("frozen-stats", th="แก้ rows ทีหลังแล้วผลไม่เปลี่ยน (ค่าสถิติคำนวณครั้งเดียว)", en="Changing rows later doesn't change results (statistics computed once)", hidden=True)
def _(sol):
    rows = [list(r) for r in TRAIN]
    st = _fn(sol)(rows)
    rows.append([100.0, 100000.0])
    rows[0][0] = -50.0
    _close(st((2.0, 300.0)), [0.0, 0.0], "หลังแก้ rows", "After changing rows")


@check("population", th="ใช้ส่วนเบี่ยงเบนของประชากร (หารด้วย n)", en="Uses the population standard deviation (divide by n)", hidden=True)
def _(sol):
    values = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    st = _fn(sol)([(v,) for v in values])
    _close(st((9.0,)), [2.0], "ค่าเฉลี่ย 5 ส่วนเบี่ยงเบน 2", "Mean 5, std 2")


@check("empty", th="rows ว่างต้อง raise ValueError", en="Empty rows raise ValueError", hidden=True)
def _(sol):
    try:
        _fn(sol)([])
    except ValueError:
        return
    raise Fail("make_standardizer([]) ต้อง raise ValueError", "make_standardizer([]) must raise ValueError")
