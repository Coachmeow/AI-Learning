def _code(src):
    return {"cell_type": "code", "execution_count": None, "source": src}


MD = {"cell_type": "markdown", "source": "# notes"}


def _fn(sol):
    fn = sol.get("restart_and_run_all")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน restart_and_run_all", "Function restart_and_run_all was not found")
    return fn


def _run(sol, cells):
    got = _fn(sol)({"cells": cells})
    if not isinstance(got, list) or not all(isinstance(r, dict) for r in got):
        raise Fail(f"ต้องคืน list ของ dict แต่ได้ {got!r}", f"Must return a list of dicts, got {got!r}")
    return got


def _field(results, n, key):
    return [r.get(key) for r in results][n]


@check("shared-vars", th="เซลล์ใช้ตัวแปรร่วมกันและเก็บผลพิมพ์แยกเซลล์", en="Cells share variables and keep their printed output apart")
def _(sol):
    res = _run(sol, [_code("x = 2"), _code(["y = x * 10\n", "print(y)"]), _code("print(x + y)")])
    outs = [r.get("output") for r in res]
    if outs != ["", "20\n", "22\n"] or not all(r.get("ok") is True and r.get("error") is None for r in res):
        raise Fail(f"ผลพิมพ์ควรเป็น ['', '20\\n', '22\\n'] และ ok ทุกเซลล์ แต่ได้ {res!r}", f"Outputs should be ['', '20\\n', '22\\n'] with every cell ok, got {res!r}")


@check("stop-on-error", th="หยุดหลังเซลล์แรกที่ error และบอกชื่อ error", en="Stops after the first failing cell and names the error")
def _(sol):
    res = _run(sol, [_code("print('a')"), _code("print(undefined_name)"), _code("print('never')")])
    if len(res) != 2 or res[1].get("ok") is not False or res[1].get("error") != "NameError":
        raise Fail(f"ควรได้ 2 ผลลัพธ์ โดยตัวที่สองเป็น ok=False, error='NameError' แต่ได้ {res!r}", f"Expected 2 results, the second with ok=False and error='NameError', got {res!r}")


@check("line-magics", th="ตัดบรรทัด % และ ! ออกก่อนรัน", en="Removes % and ! lines before running")
def _(sol):
    res = _run(sol, [_code("%matplotlib inline\nprint(1)"), _code("!pip install scikit-learn"), _code("  %env CUDA_VISIBLE_DEVICES\nprint(2)")])
    if [r.get("output") for r in res] != ["1\n", "", "2\n"] or not all(r.get("ok") for r in res):
        raise Fail(f"ควรได้ผลพิมพ์ ['1\\n', '', '2\\n'] และไม่มี error แต่ได้ {res!r}", f"Expected outputs ['1\\n', '', '2\\n'] and no errors, got {res!r}")


@check("cell-magic", th="cell magic (%%time) ตัดแค่บรรทัดแรก แล้วรันส่วนที่เหลือ", en="A cell magic (%%time) drops only its first line and runs the rest")
def _(sol):
    res = _run(sol, [_code("%%time\nz = 5\nprint(z)")])
    if len(res) != 1 or res[0].get("output") != "5\n":
        raise Fail(f"ควรพิมพ์ '5\\n' แต่ได้ {res!r}", f"Should print '5\\n', got {res!r}")


@check("fresh-kernel", th="ทุกการเรียกเริ่มจาก namespace ใหม่ เหมือนรีสตาร์ต kernel", en="Every call starts from a fresh namespace, like a restarted kernel", hidden=True)
def _(sol):
    _run(sol, [_code("leftover = 42")])
    res = _run(sol, [_code("print(leftover)")])
    if len(res) != 1 or res[0].get("error") != "NameError":
        raise Fail("ตัวแปรจากการเรียกครั้งก่อนยังใช้ได้ แปลว่าไม่ได้เริ่ม namespace ใหม่", "A variable from the previous call is still there, so the namespace was not fresh")


@check("indexes", th="index อ้างถึงตำแหน่งจริงใน nb['cells'] และข้าม markdown", en="Indexes point into nb['cells'] and markdown is skipped", hidden=True)
def _(sol):
    res = _run(sol, [MD, _code("a = 1"), MD, _code("print(a)")])
    if [r.get("index") for r in res] != [1, 3]:
        raise Fail(f"index ควรเป็น [1, 3] แต่ได้ {[r.get('index') for r in res]}", f"Indexes should be [1, 3], got {[r.get('index') for r in res]}")


@check("syntax-error", th="เซลล์ที่ไวยากรณ์ผิดได้ error='SyntaxError'", en="A cell with a syntax error reports error='SyntaxError'", hidden=True)
def _(sol):
    res = _run(sol, [_code("def broken(:\n    pass"), _code("print('after')")])
    if len(res) != 1 or res[0].get("error") != "SyntaxError":
        raise Fail(f"ควรหยุดที่เซลล์แรกด้วย SyntaxError แต่ได้ {res!r}", f"Should stop at the first cell with SyntaxError, got {res!r}")


@check("partial-output", th="เก็บสิ่งที่พิมพ์ไว้ก่อน error ด้วย", en="Keeps what a failing cell printed before the error", hidden=True)
def _(sol):
    res = _run(sol, [_code("print('before')\n1 / 0")])
    if len(res) != 1 or res[0].get("output") != "before\n" or res[0].get("error") != "ZeroDivisionError":
        raise Fail(f"ควรได้ output='before\\n' และ error='ZeroDivisionError' แต่ได้ {res!r}", f"Expected output='before\\n' and error='ZeroDivisionError', got {res!r}")
