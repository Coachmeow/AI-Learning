import math


def _run(sol, pairs):
    fn = sol.get("perplexity")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน perplexity", "Function perplexity was not found")
    try:
        return fn(pairs)
    except OverflowError:
        raise Fail("เกิด OverflowError: ลบ logit ที่มากที่สุดออกก่อนยกกำลัง", "OverflowError: subtract the largest logit before exponentiating")


def _near(got, want, th, en):
    if not isinstance(got, (int, float)) or not math.isclose(got, want, rel_tol=1e-6):
        raise Fail(f"{th}: ควรได้ประมาณ {want} แต่ได้ {got!r}", f"{en}: should be about {want}, got {got!r}")


def _logits(probs):
    return [math.log(p) for p in probs]


@check("uniform", th="logits เท่ากันหมดบน 5 โทเค็น: perplexity 5", en="Equal logits over 5 tokens: perplexity 5")
def _(sol):
    _near(_run(sol, [(i, [0.0] * 5) for i in range(5)]), 5.0, "uniform 5", "uniform 5")


@check("geometric", th="ความน่าจะเป็น 0.5, 0.25, 0.125 ได้ perplexity 4", en="Probabilities 0.5, 0.25, 0.125 give perplexity 4")
def _(sol):
    pairs = [(0, _logits([0.5, 0.5])), (0, _logits([0.25, 0.75])), (0, _logits([0.125, 0.875]))]
    _near(_run(sol, pairs), 4.0, "0.5, 0.25, 0.125", "0.5, 0.25, 0.125")


@check("empty", th="รายการว่างต้อง raise ValueError", en="An empty list raises ValueError")
def _(sol):
    fn = sol.get("perplexity")
    try:
        got = fn([])
    except ValueError:
        return
    except ZeroDivisionError:
        raise Fail("รายการว่างทำให้เกิด ZeroDivisionError แต่ต้อง raise ValueError", "An empty list gave ZeroDivisionError; it must raise ValueError")
    raise Fail(f"รายการว่างต้อง raise ValueError แต่ได้ {got!r}", f"An empty list must raise ValueError, got {got!r}")


@check("large-logits", th="logits ใหญ่ (1000) ไม่ล้น", en="Large logits (1000) don't overflow", hidden=True)
def _(sol):
    pairs = [(1, [1000.0, 1000.0 + math.log(3.0)]), (0, [1000.0, 1000.0])]
    want = math.exp((-math.log(0.75) - math.log(0.5)) / 2)
    _near(_run(sol, pairs), want, "logits 1000", "logits 1000")


@check("lesson", th="logits [5.0, 2.0, 0.5] กับ target 1 สองโทเค็น", en="Two tokens of logits [5.0, 2.0, 0.5] with target 1", hidden=True)
def _(sol):
    z = [5.0, 2.0, 0.5]
    loss = math.log(sum(math.exp(v) for v in z)) - z[1]
    _near(_run(sol, [(1, z), (1, z)]), math.exp(loss), "[5.0, 2.0, 0.5]", "[5.0, 2.0, 0.5]")
