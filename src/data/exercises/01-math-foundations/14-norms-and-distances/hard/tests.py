import math


def _run(sol, x, y, data):
    fn = sol.get("mahalanobis")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน mahalanobis", "Function mahalanobis was not found")
    return fn(list(x), list(y), [list(r) for r in data])


def _near(got, want, th, en):
    if not isinstance(got, (int, float)) or not math.isclose(got, want, rel_tol=1e-9, abs_tol=1e-9):
        raise Fail(f"{th}: ควรได้ {want:.6f} แต่ได้ {got!r}", f"{en}: should be {want:.6f}, got {got!r}")


def _cov(data):
    n, d = len(data), len(data[0])
    m = [sum(r[j] for r in data) / n for j in range(d)]
    return [[sum((r[i] - m[i]) * (r[j] - m[j]) for r in data) / (n - 1) for j in range(d)] for i in range(d)]


def _ref(x, y, data):
    S = _cov(data)
    a, b, c, e = S[0][0], S[0][1], S[1][0], S[1][1]
    det = a * e - b * c
    inv = [[e / det, -b / det], [-c / det, a / det]]
    dx = [x[0] - y[0], x[1] - y[1]]
    return math.sqrt(sum(dx[i] * inv[i][j] * dx[j] for i in range(2) for j in range(2)))


AXES = [[2, 0], [-2, 0], [0, 1], [0, -1], [2, 0], [-2, 0], [0, 1], [0, -1]]  # variances 16/7 and 4/7, no correlation
HW = [[150, 50], [160, 56], [170, 66], [180, 72], [190, 84], [165, 60], [175, 70], [185, 77]]


@check("axes", th="คุณลักษณะไม่สัมพันธ์กัน: หารด้วยความแปรปรวนของแต่ละตัว", en="Uncorrelated features: divide by each variance")
def _(sol):
    _near(_run(sol, [2, 1], [0, 0], AXES), math.sqrt(4 / (16 / 7) + 1 / (4 / 7)), "(2, 1) จาก (0, 0)", "(2, 1) from (0, 0)")


@check("correlated", th="ส่วนสูง-น้ำหนักที่สัมพันธ์กัน: คนตัวเตี้ยแต่หนักอยู่ไกลกว่า", en="Correlated height and weight: short but heavy is farther away")
def _(sol):
    mean = [sum(r[0] for r in HW) / 8, sum(r[1] for r in HW) / 8]
    tall_heavy, short_heavy = [190, 82], [152, 82]
    _near(_run(sol, tall_heavy, mean, HW), _ref(tall_heavy, mean, HW), "สูงและหนัก", "Tall and heavy")
    _near(_run(sol, short_heavy, mean, HW), _ref(short_heavy, mean, HW), "เตี้ยแต่หนัก", "Short but heavy")


@check("singular", th="คอลัมน์ที่เป็นผลคูณกันต้อง raise ValueError", en="A column that is a multiple of another raises ValueError")
def _(sol):
    fn = sol.get("mahalanobis")
    data = [[1, 2], [2, 4], [3, 6], [4, 8]]
    try:
        got = fn([1, 0], [0, 0], data)
    except ValueError:
        return
    except ZeroDivisionError:
        raise Fail("เกิด ZeroDivisionError: ต้องตรวจ pivot ที่เกือบเป็นศูนย์แล้ว raise ValueError", "ZeroDivisionError: check for a near-zero pivot and raise ValueError")
    raise Fail(f"ข้อมูลที่คอลัมน์ 2 = 2 x คอลัมน์ 1 ต้อง raise ValueError แต่ได้ {got!r}", f"Data where column 2 = 2 x column 1 must raise ValueError, got {got!r}")


@check("scales", th="คุณลักษณะที่สเกลต่างกันมาก (ความแปรปรวนราว 1e-6 กับ 15)", en="Features on very different scales (variances near 1e-6 and 15)", hidden=True)
def _(sol):
    data = [[0.001, 5.0], [-0.001, -5.0], [0.0011, 4.0], [-0.0009, -6.0], [0.0, 1.0], [0.0002, -1.0]]
    _near(_run(sol, [0.002, 1.0], [0, 0], data), _ref([0.002, 1.0], [0, 0], data), "สเกลต่างกันมาก", "Very different scales")


@check("three-d", th="ข้อมูล 3 มิติ ที่ S เป็นเมทริกซ์เอกลักษณ์คูณค่าคงที่: เท่ากับยุคลิดหารด้วยส่วนเบี่ยงเบน", en="3D data whose S is a multiple of the identity: Euclidean over the standard deviation", hidden=True)
def _(sol):
    data = []
    for i in range(3):
        for s in (1, -1):
            p = [0.0, 0.0, 0.0]
            p[i] = 3.0 * s
            data.append(p)
    # each variance = 18 / 5, covariances 0
    _near(_run(sol, [1, 2, 2], [0, 0, 0], data), 3 / math.sqrt(18 / 5), "3 มิติ", "3D")
