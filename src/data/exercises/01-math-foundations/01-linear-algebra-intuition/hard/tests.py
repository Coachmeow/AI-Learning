def _fn(sol):
    fn = sol.get("matrix_rank")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน matrix_rank", "Function matrix_rank was not found")
    return fn


def _expect(sol, rows, want, th, en):
    got = _fn(sol)([list(r) for r in rows])
    if got != want:
        raise Fail(f"{th}: แรงก์ควรเป็น {want} แต่ได้ {got!r}", f"{en}: the rank should be {want}, got {got!r}")


@check("full", th="เมทริกซ์เอกลักษณ์ 3x3 มีแรงก์ 3", en="The 3x3 identity has rank 3")
def _(sol):
    _expect(sol, [[1, 0, 0], [0, 1, 0], [0, 0, 1]], 3, "เมทริกซ์เอกลักษณ์", "Identity")


@check("deficient", th="แถวที่เป็นผลคูณของแถวอื่นไม่เพิ่มแรงก์", en="A row that is a multiple of another adds no rank")
def _(sol):
    _expect(sol, [[1, 2], [2, 4]], 1, "[[1, 2], [2, 4]]", "[[1, 2], [2, 4]]")
    _expect(sol, [[1, 0, 0], [0, 1, 0], [2, 1, 0]], 2, "v3 = 2*v1 + v2", "v3 = 2*v1 + v2")


@check("swap", th="pivot เป็นศูนย์ต้องสลับแถว", en="A zero in the pivot position needs a row swap")
def _(sol):
    _expect(sol, [[0, 1], [1, 0]], 2, "[[0, 1], [1, 0]]", "[[0, 1], [1, 0]]")


@check("floats", th="ใช้ค่าคลาดเคลื่อน ไม่เทียบศูนย์ตรงๆ (0.3 - 3*0.1 ไม่เท่ากับ 0 พอดี)", en="Uses a tolerance, not an exact zero test (0.3 - 3*0.1 is not exactly 0)")
def _(sol):
    _expect(sol, [[0.1, 0.2], [0.3, 0.6]], 1, "[[0.1, 0.2], [0.3, 0.6]]", "[[0.1, 0.2], [0.3, 0.6]]")


@check("negative-pivot", th="ค่า pivot ที่ติดลบก็ใช้ได้", en="A negative pivot value works too")
def _(sol):
    _expect(sol, [[-2, 1], [4, 3]], 2, "[[-2, 1], [4, 3]]", "[[-2, 1], [4, 3]]")
    _expect(sol, [[-1, 0], [0, -1]], 2, "[[-1, 0], [0, -1]]", "[[-1, 0], [0, -1]]")


@check("non-square", th="เมทริกซ์ที่ไม่ใช่จัตุรัสและเมทริกซ์ศูนย์", en="Non-square matrices and the zero matrix", hidden=True)
def _(sol):
    _expect(sol, [[1, 2, 3], [2, 4, 6]], 1, "2x3", "2x3")
    _expect(sol, [[1, 0], [0, 1], [1, 1]], 2, "3x2", "3x2")
    _expect(sol, [[0, 0], [0, 0]], 0, "เมทริกซ์ศูนย์", "Zero matrix")


@check("product", th="ผลคูณของเมทริกซ์ 5x2 กับ 2x4 มีแรงก์ 2", en="A 5x2 times 2x4 product has rank 2", hidden=True)
def _(sol):
    left = [[0.3, 1.7], [2.1, -0.4], [0.9, 0.9], [-1.3, 2.2], [0.5, 0.1]]
    right = [[1.1, 0.2, -0.7, 3.0], [0.4, 2.5, 1.3, -0.6]]
    prod = [[sum(l[k] * right[k][j] for k in range(2)) for j in range(4)] for l in left]
    _expect(sol, prod, 2, "ผลคูณแรงก์ 2", "A rank-2 product")


@check("no-mutation", th="ไม่แก้เมทริกซ์ที่ส่งเข้ามา", en="Leaves the input matrix unchanged", hidden=True)
def _(sol):
    rows = [[0, 1], [1, 0]]
    _fn(sol)(rows)
    if rows != [[0, 1], [1, 0]]:
        raise Fail(f"เมทริกซ์ที่ส่งเข้ามาถูกแก้เป็น {rows}", f"The input matrix was changed to {rows}")
