T = ("terminal", "w")


def _fn(sol):
    fn = sol.get("resolve_redirects")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน resolve_redirects", "Function resolve_redirects was not found")
    return fn


def _expect(sol, command, argv, out, err):
    got = _fn(sol)(command)
    want = {"argv": argv, "stdout": out, "stderr": err}
    if not isinstance(got, dict) or {k: (tuple(v) if k != "argv" else list(v)) for k, v in got.items()} != want:
        raise Fail(f"{command!r} ควรได้ {want} แต่ได้ {got!r}", f"{command!r} should give {want}, got {got!r}")


@check("plain", th="ไม่มีการเปลี่ยนทิศทาง ทั้งสองไปที่ terminal", en="No redirects: both go to the terminal")
def _(sol):
    _expect(sol, "python train.py --epochs 100", ["python", "train.py", "--epochs", "100"], T, T)


@check("separate-files", th="> และ 2> แยกไฟล์กัน (จากบทเรียน)", en="> and 2> to separate files (from the lesson)")
def _(sol):
    _expect(sol, "python train.py > output.log 2> errors.log", ["python", "train.py"], ("output.log", "w"), ("errors.log", "w"))


@check("both-same-file", th="> file 2>&1 ส่งทั้งคู่ลงไฟล์เดียว", en="> file 2>&1 sends both to one file")
def _(sol):
    _expect(sol, "python train.py > train_full.log 2>&1", ["python", "train.py"], ("train_full.log", "w"), ("train_full.log", "w"))


@check("order-matters", th="2>&1 > file: stderr ยังไปที่ terminal เพราะทำจากซ้ายไปขวา", en="2>&1 > file: stderr stays on the terminal because redirects run left to right")
def _(sol):
    _expect(sol, "python train.py 2>&1 > train.log", ["python", "train.py"], ("train.log", "w"), T)


@check("append", th=">> และ 2>> เปิดแบบต่อท้าย", en=">> and 2>> open in append mode")
def _(sol):
    _expect(sol, "python eval.py >> results.log 2>> errors.log", ["python", "eval.py"], ("results.log", "a"), ("errors.log", "a"))


@check("glued", th="ตัวดำเนินการติดกับชื่อไฟล์ได้", en="Operators can be glued to the file name", hidden=True)
def _(sol):
    _expect(sol, "nohup python train.py >train.log 2>>err.log", ["nohup", "python", "train.py"], ("train.log", "w"), ("err.log", "a"))


@check("ampersand", th="&> และ &>> ส่งทั้งสองไปไฟล์เดียว", en="&> and &>> send both to one file", hidden=True)
def _(sol):
    _expect(sol, "make all &> build.log", ["make", "all"], ("build.log", "w"), ("build.log", "w"))
    _expect(sol, "make all &>> build.log", ["make", "all"], ("build.log", "a"), ("build.log", "a"))


@check("to-stderr", th="1>&2 ส่ง stdout ไปที่ที่ stderr ชี้อยู่", en="1>&2 points stdout where stderr points", hidden=True)
def _(sol):
    _expect(sol, "echo warn 2> warn.log 1>&2", ["echo", "warn"], ("warn.log", "w"), ("warn.log", "w"))
    _expect(sol, "echo warn >&2", ["echo", "warn"], T, T)


@check("missing-name", th="ตัวดำเนินการที่ไม่มีชื่อไฟล์ต้อง raise ValueError", en="An operator without a file name raises ValueError", hidden=True)
def _(sol):
    try:
        got = _fn(sol)("python train.py >")
    except ValueError:
        return
    raise Fail(f"'>' ท้ายคำสั่งไม่มีชื่อไฟล์ ต้อง raise ValueError แต่ได้ {got!r}", f"A trailing '>' has no file name and must raise ValueError, got {got!r}")
