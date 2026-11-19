import math


def _check(sol, probs, want, th, en):
    fn = sol.get("entropy")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน entropy", "Function entropy was not found")
    try:
        got = fn(probs)
    except ValueError as e:
        raise Fail(f"entropy({probs}) เกิด ValueError: {e} (ต้องข้ามค่าที่เป็น 0)", f"entropy({probs}) raised ValueError: {e} (skip the zeros)")
    if not isinstance(got, (int, float)) or not math.isclose(got, want, abs_tol=1e-4):
        raise Fail(f"{th}: ควรได้ประมาณ {want} บิต แต่ได้ {got!r}", f"{en}: should be about {want} bits, got {got!r}")


@check("fair-coin", th="เหรียญเที่ยงตรง: 1 บิต", en="A fair coin: 1 bit")
def _(sol):
    _check(sol, [0.5, 0.5], 1.0, "[0.5, 0.5]", "[0.5, 0.5]")


@check("biased-coin", th="เหรียญเอนเอียง 99%: ประมาณ 0.0808 บิต", en="A 99% biased coin: about 0.0808 bits")
def _(sol):
    _check(sol, [0.99, 0.01], 0.0808, "[0.99, 0.01]", "[0.99, 0.01]")


@check("die", th="ลูกเต๋าเที่ยงตรง: log2(6) ≈ 2.585 บิต", en="A fair die: log2(6) ≈ 2.585 bits")
def _(sol):
    _check(sol, [1 / 6] * 6, math.log2(6), "ลูกเต๋า", "Die")


@check("zeros", th="ค่าที่เป็น 0 ไม่มีผล", en="Zero probabilities contribute nothing")
def _(sol):
    _check(sol, [0.5, 0.0, 0.5, 0.0], 1.0, "[0.5, 0.0, 0.5, 0.0]", "[0.5, 0.0, 0.5, 0.0]")
