class FakeClock:
    def __init__(self, *ticks):
        self.ticks = list(ticks)

    def __call__(self):
        return self.ticks.pop(0)


def _cls(sol):
    cls = sol.get("Timer")
    if cls is None:
        raise Fail("ไม่พบคลาส Timer", "Class Timer was not found")
    return cls


@check("elapsed", th="จดเวลาที่ผ่านไปเป็นค่าบวก", en="Records the elapsed time as a positive number")
def _(sol):
    times = {}
    with _cls(sol)("data loading", times, clock=FakeClock(10.0, 12.5)) as t:
        pass
    if getattr(t, "elapsed", None) != 2.5 or times != {"data loading": [2.5]}:
        raise Fail(f"ควรได้ elapsed=2.5 และ times={{'data loading': [2.5]}} แต่ได้ {getattr(t, 'elapsed', None)!r}, {times!r}", f"Expected elapsed=2.5 and times={{'data loading': [2.5]}}, got {getattr(t, 'elapsed', None)!r}, {times!r}")


@check("accumulates", th="ชื่อเดียวกันหลายครั้งเก็บครบทุกครั้ง", en="Repeated names keep every timing")
def _(sol):
    times = {}
    clock = FakeClock(0.0, 1.0, 1.0, 1.5, 2.0, 5.0)
    for name in ("forward pass", "forward pass", "backward pass"):
        with _cls(sol)(name, times, clock=clock):
            pass
    want = {"forward pass": [1.0, 0.5], "backward pass": [3.0]}
    if times != want:
        raise Fail(f"ควรได้ {want} แต่ได้ {times!r}", f"Expected {want}, got {times!r}")


@check("exceptions", th="ไม่กลืน exception ที่เกิดในบล็อก with แต่ยังจดเวลาไว้", en="Doesn't swallow exceptions from the with block, but still records the time")
def _(sol):
    times = {}
    try:
        with _cls(sol)("broken step", times, clock=FakeClock(0.0, 0.25)):
            raise RuntimeError("CUDA out of memory")
    except RuntimeError:
        if times != {"broken step": [0.25]}:
            raise Fail(f"เวลาของช่วงที่ error ควรถูกจดไว้ แต่ได้ {times!r}", f"The failing section should still be recorded, got {times!r}")
        return
    raise Fail("RuntimeError ถูกกลืนหายไป __exit__ ต้องไม่คืน True", "The RuntimeError was swallowed; __exit__ must not return True")
