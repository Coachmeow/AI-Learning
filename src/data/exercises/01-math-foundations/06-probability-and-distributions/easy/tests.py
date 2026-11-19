import math


def _sm(sol, logits):
    fn = sol.get("softmax")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน softmax", "Function softmax was not found")
    try:
        return fn(logits)
    except OverflowError:
        raise Fail(f"softmax({logits}) ล้น (OverflowError): ต้องลบค่ามากสุดออกก่อนยกกำลัง", f"softmax({logits}) overflowed: subtract the largest logit before exponentiating")


def _close(got, want, th, en):
    if not isinstance(got, list) or len(got) != len(want) or not all(math.isclose(g, w, abs_tol=1e-6) for g, w in zip(got, want)):
        raise Fail(f"{th}: ควรได้ประมาณ {want} แต่ได้ {got!r}", f"{en}: should be about {want}, got {got!r}")


@check("basic", th="softmax([2.0, 1.0, 0.1])", en="softmax([2.0, 1.0, 0.1])")
def _(sol):
    _close(_sm(sol, [2.0, 1.0, 0.1]), [0.659001, 0.242433, 0.098566], "[2.0, 1.0, 0.1]", "[2.0, 1.0, 0.1]")


@check("large", th="logits ใหญ่ [1000, 1001, 1002] ไม่ล้น", en="Large logits [1000, 1001, 1002] don't overflow")
def _(sol):
    _close(_sm(sol, [1000.0, 1001.0, 1002.0]), [0.090031, 0.244728, 0.665241], "[1000, 1001, 1002]", "[1000, 1001, 1002]")


@check("wide", th="logits ห่างกันมาก [-1000, 0, 1000]", en="Widely spread logits [-1000, 0, 1000]")
def _(sol):
    _close(_sm(sol, [-1000.0, 0.0, 1000.0]), [0.0, 0.0, 1.0], "[-1000, 0, 1000]", "[-1000, 0, 1000]")
