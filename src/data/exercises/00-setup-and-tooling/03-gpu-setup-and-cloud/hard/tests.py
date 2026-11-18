class FakeGPU:
    """fn() queues `work` seconds on a pretend GPU and returns at once; sync() waits for it."""

    def __init__(self, works, launch=0.001):
        self.works = list(works)
        self.launch = launch
        self.now = 0.0
        self.pending = 0.0
        self.calls = 0

    def clock(self):
        return self.now

    def fn(self):
        self.calls += 1
        self.now += self.launch
        self.pending += self.works.pop(0)

    def sync(self):
        self.now += self.pending
        self.pending = 0.0


class FakeCPU:
    """fn() does `work` seconds of blocking work."""

    def __init__(self, works):
        self.works = list(works)
        self.now = 0.0

    def clock(self):
        return self.now

    def fn(self):
        self.now += self.works.pop(0)


def _fn(sol):
    fn = sol.get("benchmark")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน benchmark", "Function benchmark was not found")
    return fn


def _close(got, want, label_th, label_en):
    if not isinstance(got, float) or abs(got - want) > 1e-9:
        raise Fail(f"{label_th}: ควรได้ {want} แต่ได้ {got!r}", f"{label_en}: should be {want}, got {got!r}")


@check("cpu-median", th="งานบน CPU ได้ค่ามัธยฐานของเวลา", en="Blocking work gives the median time")
def _(sol):
    cpu = FakeCPU([3.0, 1.0, 2.0])
    got = _fn(sol)(cpu.fn, repeats=3, warmup=0, clock=cpu.clock)
    _close(got, 2.0, "เวลา 3, 1, 2 วินาที", "Times 3, 1, 2 seconds")


@check("warmup", th="ไม่จับเวลารอบ warmup", en="Warmup calls are not timed")
def _(sol):
    cpu = FakeCPU([100.0, 100.0, 1.0, 2.0, 3.0])
    got = _fn(sol)(cpu.fn, repeats=3, warmup=2, clock=cpu.clock)
    _close(got, 2.0, "warmup 2 รอบที่ช้า 100 วินาที", "Two slow 100-second warmup calls")


@check("gpu-sync", th="รอ GPU ทำงานเสร็จก่อนหยุดจับเวลา", en="Waits for the GPU before stopping the timer")
def _(sol):
    gpu = FakeGPU([0.0, 0.5, 0.5, 0.5])
    got = _fn(sol)(gpu.fn, repeats=3, warmup=1, sync=gpu.sync, clock=gpu.clock)
    _close(got, 0.501, "GPU ทำงานครั้งละ 0.5 วินาที (+ สั่งงาน 0.001)", "GPU work of 0.5 s per call (+ 0.001 to launch)")


@check("bad-repeats", th="repeats น้อยกว่า 1 ต้อง raise ValueError", en="repeats below 1 raises ValueError")
def _(sol):
    cpu = FakeCPU([1.0] * 5)
    try:
        got = _fn(sol)(cpu.fn, repeats=0, warmup=0, clock=cpu.clock)
    except ValueError:
        return
    raise Fail(f"repeats=0 ต้อง raise ValueError แต่ได้ {got!r}", f"repeats=0 must raise ValueError, got {got!r}")


@check("sync-before-start", th="sync ก่อนเริ่มจับเวลา งาน warmup ที่ค้างจะไม่ถูกนับ", en="Syncs before starting, so leftover warmup work is not counted", hidden=True)
def _(sol):
    gpu = FakeGPU([100.0, 1.0, 2.0, 3.0])
    got = _fn(sol)(gpu.fn, repeats=3, warmup=1, sync=gpu.sync, clock=gpu.clock)
    _close(got, 2.001, "งาน warmup 100 วินาทีที่ยังค้างบน GPU", "100 s of warmup work still queued on the GPU")


@check("even", th="จำนวนครั้งเป็นเลขคู่ ใช้ค่าเฉลี่ยของสองตัวกลาง", en="An even count uses the mean of the two middle values", hidden=True)
def _(sol):
    cpu = FakeCPU([4.0, 1.0, 3.0, 2.0])
    got = _fn(sol)(cpu.fn, repeats=4, warmup=0, clock=cpu.clock)
    _close(got, 2.5, "เวลา 4, 1, 3, 2 วินาที", "Times 4, 1, 3, 2 seconds")


@check("outlier", th="ค่ามัธยฐานไม่ถูกดึงด้วยครั้งที่ช้าผิดปกติ", en="One unusually slow run does not drag the result", hidden=True)
def _(sol):
    cpu = FakeCPU([1.0, 1.0, 50.0, 1.0, 1.0])
    got = _fn(sol)(cpu.fn, repeats=5, warmup=0, clock=cpu.clock)
    _close(got, 1.0, "เวลา 1, 1, 50, 1, 1 วินาที", "Times 1, 1, 50, 1, 1 seconds")


@check("call-count", th="เรียก fn รวม warmup + repeats ครั้งพอดี", en="Calls fn exactly warmup + repeats times", hidden=True)
def _(sol):
    gpu = FakeGPU([0.1] * 10)
    _fn(sol)(gpu.fn, repeats=4, warmup=2, sync=gpu.sync, clock=gpu.clock)
    if gpu.calls != 6:
        raise Fail(f"ควรเรียก fn 6 ครั้ง (warmup 2 + repeats 4) แต่เรียก {gpu.calls} ครั้ง", f"fn should be called 6 times (2 warmup + 4 repeats), got {gpu.calls}")
