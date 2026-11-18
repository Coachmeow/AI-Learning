def _fn(sol):
    fn = sol.get("resolve")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน resolve", "Function resolve was not found")
    return fn


def _expect(sol, index, reqs, want, label_th, label_en):
    got = _fn(sol)(index, dict(reqs))
    if got != want:
        raise Fail(f"{label_th}: ควรได้ {want} แต่ได้ {got!r}", f"{label_en}: should be {want}, got {got!r}")


def _raises(sol, index, reqs, label_th, label_en):
    try:
        got = _fn(sol)(index, dict(reqs))
    except ValueError:
        return
    raise Fail(f"{label_th}: ต้อง raise ValueError แต่ได้ {got!r}", f"{label_en}: must raise ValueError, got {got!r}")


NUMPY = {"1.24.0": {}, "1.26.4": {}, "2.1.0": {}}


@check("newest", th="เลือกเวอร์ชันใหม่ที่สุดที่ใช้ได้ รวม dependency ทางอ้อม", en="Picks the newest allowed versions, transitive ones included")
def _(sol):
    index = {"app": {"1.0": {"numpy": ">=1.26"}}, "numpy": NUMPY}
    _expect(sol, index, {"app": ""}, {"app": "1.0", "numpy": "2.1.0"}, "app ต้องการ numpy>=1.26", "app needs numpy>=1.26")


@check("shared-dep", th="เงื่อนไขจากสองแพ็กเกจที่ใช้ numpy ร่วมกันต้องเป็นจริงทั้งคู่", en="Two packages sharing numpy must both be satisfied")
def _(sol):
    index = {"app": {"1.0": {"numpy": ">=1.26"}}, "plot": {"1.0": {"numpy": "<2"}}, "numpy": NUMPY}
    _expect(sol, index, {"app": "", "plot": ""}, {"app": "1.0", "plot": "1.0", "numpy": "1.26.4"}, "app ต้องการ numpy>=1.26 และ plot ต้องการ numpy<2", "app needs numpy>=1.26 and plot needs numpy<2")


@check("backtrack", th="ย้อนกลับไปใช้ lib เวอร์ชันเก่าเมื่อเวอร์ชันใหม่ขัดกับ torch<2.2", en="Backs up to an older lib when the newest clashes with torch<2.2")
def _(sol):
    index = {
        "lib": {"2.0": {"torch": ">=2.3"}, "1.5": {"torch": ">=2.0"}},
        "torch": {"2.0.1": {}, "2.1.2": {}, "2.4.0": {}},
    }
    _expect(sol, index, {"lib": "", "torch": "<2.2"}, {"lib": "1.5", "torch": "2.1.2"}, "lib ล่าสุดต้องการ torch>=2.3", "the newest lib needs torch>=2.3")


@check("impossible", th="ไม่มีทางเลือกที่ใช้ได้ต้อง raise ValueError", en="No possible combination raises ValueError")
def _(sol):
    index = {"a": {"1.0": {"c": ">=2"}}, "b": {"1.0": {"c": "<2"}}, "c": {"1.0": {}, "2.0": {}}}
    _raises(sol, index, {"a": "", "b": ""}, "a ต้องการ c>=2 แต่ b ต้องการ c<2", "a needs c>=2 but b needs c<2")


@check("deep-backtrack", th="ย้อนกลับได้หลายชั้น", en="Backs up across several levels", hidden=True)
def _(sol):
    index = {
        "app": {"3.0": {"x": ">=2"}, "2.0": {"x": "<2"}},
        "x": {"1.0": {}, "2.0": {"y": ">=5"}},
        "y": {"1.0": {}},
    }
    _expect(sol, index, {"app": ""}, {"app": "2.0", "x": "1.0"}, "app 3.0 ต้องการ x>=2 ซึ่งต้องการ y>=5 ที่ไม่มี", "app 3.0 needs x>=2, which needs a y>=5 that does not exist")


@check("missing", th="แพ็กเกจที่ไม่มีใน index ต้อง raise ValueError", en="A package missing from the index raises ValueError", hidden=True)
def _(sol):
    _raises(sol, {"app": {"1.0": {"ghost": ""}}}, {"app": ""}, "app ต้องการ ghost ที่ไม่มีใน index", "app needs ghost, which is not in the index")


@check("numeric", th="เทียบเวอร์ชันเป็นตัวเลข (1.10 ใหม่กว่า 1.9)", en="Compares versions as numbers (1.10 is newer than 1.9)", hidden=True)
def _(sol):
    index = {"tool": {"1.9.0": {}, "1.10.0": {}, "1.2.0": {}}}
    _expect(sol, index, {"tool": ""}, {"tool": "1.10.0"}, "tool มี 1.9.0, 1.10.0, 1.2.0", "tool has 1.9.0, 1.10.0, 1.2.0")


@check("diamond", th="dependency แบบเพชร เงื่อนไขหลายข้อต่อแพ็กเกจเดียว", en="A diamond with several specs on one package", hidden=True)
def _(sol):
    index = {
        "top": {"1.0": {"left": "", "right": ""}},
        "left": {"1.0": {"base": ">=1.1,<3"}},
        "right": {"2.0": {"base": "!=2.0"}, "1.0": {"base": ""}},
        "base": {"1.0": {}, "1.1": {}, "2.0": {}, "3.0": {}},
    }
    _expect(sol, index, {"top": ""}, {"top": "1.0", "left": "1.0", "right": "2.0", "base": "1.1"}, "left ต้องการ base>=1.1,<3 และ right 2.0 ต้องการ base!=2.0", "left needs base>=1.1,<3 and right 2.0 needs base!=2.0")
