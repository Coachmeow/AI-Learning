import math


def _win(sol, N, want, th, en):
    fn = sol.get("hann_window")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน hann_window", "Function hann_window was not found")
    got = fn(N)
    if not isinstance(got, list) or len(got) != len(want) or not all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(got, want)):
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("five", th="N = 5 ได้ [0, 0.5, 1, 0.5, 0]", en="N = 5 gives [0, 0.5, 1, 0.5, 0]")
def _(sol):
    _win(sol, 5, [0.0, 0.5, 1.0, 0.5, 0.0], "N = 5", "N = 5")


@check("four", th="N = 4 ได้ [0, 0.75, 0.75, 0]", en="N = 4 gives [0, 0.75, 0.75, 0]")
def _(sol):
    _win(sol, 4, [0.0, 0.75, 0.75, 0.0], "N = 4", "N = 4")


@check("ends", th="N = 64: ปลายทั้งสองเป็นศูนย์และสมมาตร", en="N = 64: both ends are zero and the window is symmetric")
def _(sol):
    fn = sol.get("hann_window")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน hann_window", "Function hann_window was not found")
    w = fn(64)
    if not isinstance(w, list) or len(w) != 64:
        raise Fail(f"ต้องคืน list ยาว 64 แต่ได้ {w!r}", f"Must return a list of length 64, got {w!r}")
    if abs(w[0]) > 1e-12 or abs(w[-1]) > 1e-12:
        raise Fail(f"ปลายควรเป็น 0 แต่ได้ {w[0]} และ {w[-1]}", f"The ends should be 0, got {w[0]} and {w[-1]}")
    if any(abs(w[n] - w[63 - n]) > 1e-12 for n in range(64)):
        raise Fail("window ต้องสมมาตร: w[n] = w[N - 1 - n]", "The window must be symmetric: w[n] = w[N - 1 - n]")
