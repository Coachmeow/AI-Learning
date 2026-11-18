NB = {
    "nbformat": 4,
    "cells": [
        {"cell_type": "markdown", "source": ["# My Experiment\n", "Testing learning rate 0.01"]},
        {"cell_type": "code", "execution_count": 1, "source": ["import numpy as np\n", "data = np.random.randn(1000)\n", "data.mean(), data.std()"]},
        {"cell_type": "code", "execution_count": 2, "source": "%timeit np.random.randn(10000)"},
        {"cell_type": "markdown", "source": "Done."},
    ],
}


def _fn(sol):
    fn = sol.get("code_cells")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน code_cells", "Function code_cells was not found")
    return fn


@check("only-code", th="คืนเฉพาะเซลล์โค้ด", en="Returns code cells only")
def _(sol):
    got = _fn(sol)(NB)
    if not isinstance(got, list) or len(got) != 2:
        raise Fail(f"notebook นี้มีเซลล์โค้ด 2 เซลล์ ควรได้ list ยาว 2 แต่ได้ {got!r}", f"This notebook has 2 code cells, expected a list of 2, got {got!r}")


@check("join-lines", th="ต่อ list ของบรรทัดเป็นสตริงเดียวโดยไม่เพิ่มบรรทัดว่าง", en="Joins a list of lines into one string without extra blank lines")
def _(sol):
    got = _fn(sol)(NB)[0]
    want = "import numpy as np\ndata = np.random.randn(1000)\ndata.mean(), data.std()"
    if got != want:
        raise Fail(f"เซลล์แรกควรได้ {want!r} แต่ได้ {got!r}", f"The first cell should be {want!r}, got {got!r}")


@check("string-source", th="source ที่เป็นสตริงอยู่แล้วใช้ได้ตามเดิม", en="A source that is already a string is kept as is")
def _(sol):
    got = _fn(sol)(NB)[1]
    if got != "%timeit np.random.randn(10000)":
        raise Fail(f"เซลล์ที่สองควรได้ '%timeit np.random.randn(10000)' แต่ได้ {got!r}", f"The second cell should be '%timeit np.random.randn(10000)', got {got!r}")


@check("empty", th="notebook ที่ไม่มีเซลล์โค้ดได้ list ว่าง", en="A notebook without code cells gives an empty list")
def _(sol):
    got = _fn(sol)({"cells": [{"cell_type": "markdown", "source": "hi"}]})
    if got != []:
        raise Fail(f"ควรได้ [] แต่ได้ {got!r}", f"Expected [], got {got!r}")
