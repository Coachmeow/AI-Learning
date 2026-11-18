def _fn(sol):
    fn = sol.get("batches")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน batches", "Function batches was not found")
    return fn


class Counting:
    """An iterable that counts how many items were read from it."""

    def __init__(self, n):
        self.n, self.read = n, 0

    def __iter__(self):
        for i in range(self.n):
            self.read += 1
            yield i


@check("sizes", th="batch สุดท้ายเล็กกว่าได้ (เหมือนบทเรียน)", en="The last batch may be smaller (as in the lesson)")
def _(sol):
    got = [list(b) for b in _fn(sol)(range(10), 4)]
    if got != [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]:
        raise Fail(f"batches(range(10), 4) ควรได้ [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]] แต่ได้ {got!r}", f"batches(range(10), 4) should give [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]], got {got!r}")


@check("drop-last", th="drop_last=True ทิ้ง batch ที่ไม่เต็ม", en="drop_last=True drops the partial batch")
def _(sol):
    got = [list(b) for b in _fn(sol)(range(10), 4, drop_last=True)]
    if got != [[0, 1, 2, 3], [4, 5, 6, 7]]:
        raise Fail(f"ควรได้ [[0, 1, 2, 3], [4, 5, 6, 7]] แต่ได้ {got!r}", f"Expected [[0, 1, 2, 3], [4, 5, 6, 7]], got {got!r}")


@check("generator-input", th="รับ generator ได้", en="Accepts a generator")
def _(sol):
    squares = (i * i for i in range(7))
    got = [len(b) for b in _fn(sol)(squares, 3)]
    if got != [3, 3, 1]:
        raise Fail(f"ขนาด batch ควรเป็น [3, 3, 1] แต่ได้ {got!r}", f"Batch sizes should be [3, 3, 1], got {got!r}")


@check("lazy", th="batch แรกอ่านข้อมูลแค่ batch_size ตัว", en="The first batch reads only batch_size items")
def _(sol):
    src = Counting(1000)
    it = _fn(sol)(src, 4)
    first = next(iter(it))
    if list(first) != [0, 1, 2, 3] or src.read > 4:
        raise Fail(f"batch แรกควรเป็น [0, 1, 2, 3] โดยอ่านข้อมูลไม่เกิน 4 ตัว แต่ได้ {list(first)!r} และอ่านไป {src.read} ตัว", f"The first batch should be [0, 1, 2, 3] after reading at most 4 items; got {list(first)!r} after {src.read} reads")


@check("eager-error", th="batch_size=0 ต้อง raise ValueError ตั้งแต่ตอนเรียก", en="batch_size=0 raises ValueError at call time")
def _(sol):
    try:
        _fn(sol)(range(10), 0)
    except ValueError:
        return
    raise Fail("batches(range(10), 0) ต้อง raise ValueError ทันที ไม่ใช่รอจนวนลูป", "batches(range(10), 0) must raise ValueError right away, not once the loop starts")
