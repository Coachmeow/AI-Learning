import cmath
import math
import time


def _fn(sol):
    fn = sol.get("fft")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน fft", "Function fft was not found")
    return fn


def _dft(x):
    N = len(x)
    return [sum(x[n] * cmath.exp(-2j * cmath.pi * k * n / N) for n in range(N)) for k in range(N)]


def _ref_fft(x):
    N = len(x)
    if N == 1:
        return [complex(x[0])]
    e, o = _ref_fft(x[0::2]), _ref_fft(x[1::2])
    out = [0j] * N
    for k in range(N // 2):
        t = cmath.exp(-2j * cmath.pi * k / N) * o[k]
        out[k], out[k + N // 2] = e[k] + t, e[k] - t
    return out


def _match(sol, x, want, th, en, tol=1e-9):
    got = _fn(sol)(list(x))
    if not isinstance(got, list) or len(got) != len(want):
        raise Fail(f"{th}: ต้องคืน list ยาว {len(want)} แต่ได้ {got!r}", f"{en}: must return a list of length {len(want)}, got {got!r}")
    for k, (g, w) in enumerate(zip(got, want)):
        if abs(complex(g) - complex(w)) > tol:
            raise Fail(f"{th}: X[{k}] ควรเป็น {complex(w):.6g} แต่ได้ {g!r}", f"{en}: X[{k}] should be {complex(w):.6g}, got {g!r}")


def _signal(N, seed):
    return [math.sin(1.3 * n + seed) + 0.5 * math.cos(0.37 * n * n - seed) for n in range(N)]


@check("four", th="fft([1, 2, 3, 4]) ได้ [10, -2+2i, -2, -2-2i]", en="fft([1, 2, 3, 4]) gives [10, -2+2i, -2, -2-2i]")
def _(sol):
    _match(sol, [1, 2, 3, 4], [10, -2 + 2j, -2, -2 - 2j], "[1, 2, 3, 4]", "[1, 2, 3, 4]")


@check("single", th="N = 1: fft([5]) ได้ [5]", en="N = 1: fft([5]) gives [5]")
def _(sol):
    _match(sol, [5], [5], "N = 1", "N = 1")


@check("impulse", th="แรงกระตุ้นที่ n = 1 ใน N = 8 ได้ X[k] = e^(-2πik/8)", en="An impulse at n = 1 with N = 8 gives X[k] = e^(-2πik/8)")
def _(sol):
    _match(sol, [0, 1, 0, 0, 0, 0, 0, 0], [cmath.exp(-2j * cmath.pi * k / 8) for k in range(8)], "แรงกระตุ้นที่ n = 1", "Impulse at n = 1")


@check("random-64", th="N = 64 ตรงกับ DFT ตามนิยาม", en="N = 64 matches the DFT definition")
def _(sol):
    x = _signal(64, 0.4)
    _match(sol, x, _dft(x), "N = 64", "N = 64")


@check("not-power", th="ความยาว 6 และ list ว่างต้อง raise ValueError", en="Length 6 and an empty list must raise ValueError")
def _(sol):
    for x in ([1, 2, 3, 4, 5, 6], []):
        try:
            got = _fn(sol)(x)
        except ValueError:
            continue
        except Exception as e:
            raise Fail(f"ความยาว {len(x)}: ควร raise ValueError แต่เกิด {type(e).__name__}: {e}", f"Length {len(x)}: should raise ValueError, got {type(e).__name__}: {e}")
        raise Fail(f"ความยาว {len(x)}: ควร raise ValueError แต่คืน {got!r}", f"Length {len(x)}: should raise ValueError, returned {got!r}")


@check("complex-input", th="ขาเข้าเชิงซ้อนยาว 16 ตรงกับ DFT", en="A complex input of length 16 matches the DFT", hidden=True)
def _(sol):
    x = [complex(math.cos(0.7 * n), math.sin(0.3 * n * n)) for n in range(16)]
    _match(sol, x, _dft(x), "ขาเข้าเชิงซ้อน", "Complex input")


@check("no-mutation", th="ไม่แก้ไข x ที่รับเข้ามา", en="Does not modify the x it receives", hidden=True)
def _(sol):
    x = [1.0, 2.0, 3.0, 4.0]
    _fn(sol)(x)
    if x != [1.0, 2.0, 3.0, 4.0]:
        raise Fail(f"x ถูกแก้เป็น {x}", f"x was modified to {x}")


@check("speed", th="N = 1024 ต้องเร็วแบบ O(N log N): ช้ากว่า FFT อ้างอิงได้ไม่เกิน 30 เท่า", en="N = 1024 must run in O(N log N): at most 30 times slower than a reference FFT", hidden=True)
def _(sol):
    x = _signal(1024, 1.1)
    ref = float("inf")
    for _ in range(3):
        t0 = time.perf_counter()
        _ref_fft(list(x))
        ref = min(ref, time.perf_counter() - t0)
    t0 = time.perf_counter()
    got = _fn(sol)(list(x))
    mine = time.perf_counter() - t0
    if mine < 30 * ref and mine < 0.5:
        t0 = time.perf_counter()
        _fn(sol)(list(x))
        mine = min(mine, time.perf_counter() - t0)
    want = _ref_fft(list(x))
    if not isinstance(got, list) or len(got) != 1024 or any(abs(complex(g) - w) > 1e-8 for g, w in zip(got, want)):
        raise Fail("N = 1024: ผลลัพธ์ไม่ตรงกับ FFT อ้างอิง", "N = 1024: the result does not match the reference FFT")
    if mine > 30 * max(ref, 1e-4):
        raise Fail(f"ใช้เวลา {mine * 1000:.0f} ms เทียบกับ {ref * 1000:.1f} ms ของ FFT อ้างอิง ({mine / ref:.0f} เท่า): ดูเหมือนเป็น O(N²)", f"Took {mine * 1000:.0f} ms against {ref * 1000:.1f} ms for the reference FFT ({mine / ref:.0f}x): this looks like O(N²)")
