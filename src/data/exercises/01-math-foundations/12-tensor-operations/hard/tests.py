import math

A = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
B = [[7.0, 8.0, 9.0], [10.0, 11.0, 12.0]]


def _run(sol, subs, *arrays):
    fn = sol.get("einsum")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน einsum", "Function einsum was not found")
    return fn(subs, *arrays)


def _close(got, want):
    if isinstance(want, list):
        return isinstance(got, list) and len(got) == len(want) and all(_close(g, w) for g, w in zip(got, want))
    return isinstance(got, (int, float)) and math.isclose(got, want, abs_tol=1e-9)


def _is(sol, subs, arrays, want):
    got = _run(sol, subs, *arrays)
    if not _close(got, want):
        raise Fail(f"einsum(\"{subs}\") ควรได้ {want} แต่ได้ {got!r}", f"einsum(\"{subs}\") should be {want}, got {got!r}")


@check("dot", th="\"i,i->\": dot product ได้ 32", en="\"i,i->\": the dot product, 32")
def _(sol):
    _is(sol, "i,i->", ([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]), 32.0)


@check("matmul", th="\"ik,kj->ij\": การคูณเมทริกซ์ 3x2 @ 2x3", en="\"ik,kj->ij\": a 3x2 @ 2x3 matrix product")
def _(sol):
    want = [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(3)] for i in range(3)]
    _is(sol, "ik,kj->ij", (A, B), want)


@check("outer-transpose", th="\"i,j->ij\" และ \"ij->ji\"", en="\"i,j->ij\" and \"ij->ji\"")
def _(sol):
    _is(sol, "i,j->ij", ([1.0, 2.0], [3.0, 4.0, 5.0]), [[3.0, 4.0, 5.0], [6.0, 8.0, 10.0]])
    _is(sol, "ij->ji", (A,), [[1.0, 3.0, 5.0], [2.0, 4.0, 6.0]])


@check("trace", th="\"ii->\": trace ของ [[1, 2], [3, 4]] ได้ 5", en="\"ii->\": the trace of [[1, 2], [3, 4]] is 5")
def _(sol):
    _is(sol, "ii->", ([[1.0, 2.0], [3.0, 4.0]],), 5.0)


@check("batch", th="\"bij,bjk->bik\": batch ของการคูณเมทริกซ์", en="\"bij,bjk->bik\": a batch of matrix products", hidden=True)
def _(sol):
    X = [[[1.0, 0.0], [2.0, 1.0]], [[0.5, -1.0], [3.0, 2.0]]]
    Y = [[[1.0, 2.0], [3.0, 4.0]], [[2.0, 0.0], [1.0, -1.0]]]
    want = [[[sum(X[b][i][j] * Y[b][j][k] for j in range(2)) for k in range(2)] for i in range(2)] for b in range(2)]
    _is(sol, "bij,bjk->bik", (X, Y), want)


@check("diagonal-sum", th="\"ii->i\" (เส้นทแยงมุม) และ \"ij->\" (รวมทั้งหมด)", en="\"ii->i\" (the diagonal) and \"ij->\" (sum everything)", hidden=True)
def _(sol):
    _is(sol, "ii->i", ([[1.0, 2.0], [3.0, 4.0]],), [1.0, 4.0])
    _is(sol, "ij->", (A,), 21.0)


@check("size-mismatch", th="ขนาดของตัวอักษรเดียวกันไม่ตรงกันต้อง raise ValueError", en="A letter with mismatched sizes raises ValueError", hidden=True)
def _(sol):
    fn = sol.get("einsum")
    try:
        got = fn("ik,kj->ij", A, A)
    except ValueError:
        return
    raise Fail(f"\"ik,kj->ij\" กับ 3x2 และ 3x2 (k = 2 กับ 3) ต้อง raise ValueError แต่ได้ {got!r}", f"\"ik,kj->ij\" on 3x2 and 3x2 (k is 2 and 3) must raise ValueError, got {got!r}")
