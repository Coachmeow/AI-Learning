import math

XS = [-2, -1, 0, 1, 2] * 4
SQ = [x * x for x in XS]


def _fn(sol, name):
    fn = sol.get(name)
    if fn is None:
        raise Fail(f"ไม่พบฟังก์ชัน {name}", f"Function {name} was not found")
    return fn


def _mi(sol, xs, ys, want, th, en):
    got = _fn(sol, "mutual_information")(xs, ys)
    if not isinstance(got, (int, float)) or not math.isclose(got, want, abs_tol=1e-9):
        raise Fail(f"{th}: ควรได้ {want:.6f} บิต แต่ได้ {got!r}", f"{en}: should be {want:.6f} bits, got {got!r}")


def _H(probs):
    return -sum(p * math.log2(p) for p in probs if p > 0)


@check("copy", th="X กับสำเนาของตัวเอง: I = H(X) = 2 บิต", en="X with a copy of itself: I = H(X) = 2 bits")
def _(sol):
    xs = [0, 1, 2, 3] * 3
    _mi(sol, xs, list(xs), 2.0, "สำเนา", "Copy")


@check("independent", th="ทุกคู่เกิดเท่ากัน: I = 0", en="Every pair equally often: I = 0")
def _(sol):
    _mi(sol, [0, 0, 1, 1] * 2, [0, 1, 0, 1] * 2, 0.0, "อิสระต่อกัน", "Independent")


@check("table", th="ตัวอย่างจากตาราง [[0.4, 0.1], [0.1, 0.4]]: ประมาณ 0.278 บิต", en="Samples from [[0.4, 0.1], [0.1, 0.4]]: about 0.278 bits")
def _(sol):
    xs = [0] * 5 + [1] * 5
    ys = [0, 0, 0, 0, 1, 1, 1, 1, 1, 0]
    _mi(sol, xs, ys, 1 - _H([0.8, 0.2]), "ตาราง 0.4/0.1", "Table 0.4/0.1")


@check("nonlinear", th="y = x * x: สหสัมพันธ์เป็นศูนย์ แต่ I = H(Y)", en="y = x * x: zero correlation, but I = H(Y)")
def _(sol):
    _mi(sol, XS, SQ, _H([0.2, 0.4, 0.4]), "y = x * x", "y = x * x")


@check("rank", th="จัดอันดับ: MI มากไปน้อย และ MI เท่ากันเรียงตามชื่อ", en="Ranking: MI from high to low, equal MI sorted by name")
def _(sol):
    parity = [x % 2 for x in XS]
    noise = [0, 1] * 10
    feats = {"parity": parity, "noise": noise, "b_dup": list(parity), "x": XS, "a_dup": list(parity)}
    got = _fn(sol, "rank_features")(feats, SQ)
    names = [t[0] for t in got] if isinstance(got, list) else got
    want = ["x", "a_dup", "b_dup", "parity", "noise"]
    if names != want:
        raise Fail(f"ลำดับควรเป็น {want} (a_dup, b_dup และ parity เป็นคอลัมน์เดียวกัน MI จึงเท่ากัน) แต่ได้ {names!r}",
                   f"The order should be {want} (a_dup, b_dup and parity are the same column, so their MI is equal), got {names!r}")


@check("strings", th="ค่าเป็นข้อความก็ได้", en="Values can be strings", hidden=True)
def _(sol):
    weather = ["sun", "sun", "rain", "rain", "sun", "rain", "sun", "sun"]
    umbrella = ["no", "no", "yes", "yes", "no", "yes", "yes", "no"]
    pxy = {("sun", "no"): 4 / 8, ("sun", "yes"): 1 / 8, ("rain", "yes"): 3 / 8}
    want = sum(p * math.log2(p / ({"sun": 5 / 8, "rain": 3 / 8}[x] * {"no": 4 / 8, "yes": 4 / 8}[y])) for (x, y), p in pxy.items())
    _mi(sol, weather, umbrella, want, "สภาพอากาศกับร่ม", "Weather and umbrella")


@check("lengths", th="ความยาวไม่เท่ากันหรือว่างต้อง raise ValueError", en="Different lengths or empty lists raise ValueError", hidden=True)
def _(sol):
    fn = _fn(sol, "mutual_information")
    for xs, ys in (([1, 2, 3], [1, 2]), ([], [])):
        try:
            got = fn(xs, ys)
        except ValueError:
            continue
        except ZeroDivisionError:
            raise Fail(f"mutual_information({xs}, {ys}) เกิด ZeroDivisionError แต่ต้อง raise ValueError", f"mutual_information({xs}, {ys}) gave ZeroDivisionError; it must raise ValueError")
        raise Fail(f"mutual_information({xs}, {ys}) ต้อง raise ValueError แต่ได้ {got!r}", f"mutual_information({xs}, {ys}) must raise ValueError, got {got!r}")
