import math


def _fn(sol, name):
    fn = sol.get(name)
    if fn is None:
        raise Fail(f"ไม่พบฟังก์ชัน {name}", f"Function {name} was not found")
    return fn


def _close(got, want, th, en):
    if not isinstance(got, list) or len(got) != len(want) or not all(abs(complex(g) - complex(w)) <= 1e-9 for g, w in zip(got, want)):
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("impulse", th="dft([1, 0, 0, 0]) ได้ 1 ทุกช่อง", en="dft([1, 0, 0, 0]) is all ones")
def _(sol):
    _close(_fn(sol, "dft")([1, 0, 0, 0]), [1, 1, 1, 1], "แรงกระตุ้น", "Impulse")


@check("ramp", th="dft([1, 2, 3, 4]) ได้ [10, -2+2i, -2, -2-2i]", en="dft([1, 2, 3, 4]) gives [10, -2+2i, -2, -2-2i]")
def _(sol):
    _close(_fn(sol, "dft")([1, 2, 3, 4]), [10, -2 + 2j, -2, -2 - 2j], "[1, 2, 3, 4]", "[1, 2, 3, 4]")


@check("peaks", th="แบบฝึกหัดที่ 3: ยอดขนาด 16 ที่ bin 3 และ 8 ที่ bin 7", en="Exercise 3: peaks of 16 at bin 3 and 8 at bin 7")
def _(sol):
    x = [math.sin(2 * math.pi * 3 * n / 32) + 0.5 * math.sin(2 * math.pi * 7 * n / 32) for n in range(32)]
    X = _fn(sol, "dft")(x)
    if not isinstance(X, list) or len(X) != 32:
        raise Fail(f"ต้องคืน list ยาว 32 แต่ได้ {X!r}", f"Must return a list of length 32, got {X!r}")
    mags = [abs(v) for v in X]
    want = {3: 16.0, 7: 8.0, 25: 8.0, 29: 16.0}
    for k in range(32):
        if abs(mags[k] - want.get(k, 0.0)) > 1e-9:
            raise Fail(f"|X[{k}]| ควรเป็น {want.get(k, 0.0)} แต่ได้ {mags[k]:.6g}", f"|X[{k}]| should be {want.get(k, 0.0)}, got {mags[k]:.6g}")


@check("complex-input", th="ขาเข้าเชิงซ้อน: dft([1j, 0]) ได้ [1j, 1j]", en="Complex input: dft([1j, 0]) gives [1j, 1j]")
def _(sol):
    _close(_fn(sol, "dft")([1j, 0]), [1j, 1j], "[1j, 0]", "[1j, 0]")


@check("inverse", th="idft([10, -2+2i, -2, -2-2i]) ได้ [1, 2, 3, 4]", en="idft([10, -2+2i, -2, -2-2i]) gives [1, 2, 3, 4]")
def _(sol):
    _close(_fn(sol, "idft")([10, -2 + 2j, -2, -2 - 2j]), [1, 2, 3, 4], "DFT ผกผัน", "Inverse DFT")


@check("round-trip", th="idft(dft(x)) ได้ x กลับมาสำหรับสัญญาณเชิงซ้อนยาว 12", en="idft(dft(x)) gives x back for a complex signal of length 12")
def _(sol):
    x = [complex(math.cos(1.7 * n) + n % 3, math.sin(0.9 * n * n)) for n in range(12)]
    _close(_fn(sol, "idft")(_fn(sol, "dft")(list(x))), x, "ไปแล้วกลับ", "Round trip")


@check("empty", th="list ว่างได้ list ว่าง", en="An empty list gives an empty list")
def _(sol):
    for name in ("dft", "idft"):
        got = _fn(sol, name)([])
        if got != []:
            raise Fail(f"{name}([]) ควรได้ [] แต่ได้ {got!r}", f"{name}([]) should be [], got {got!r}")
