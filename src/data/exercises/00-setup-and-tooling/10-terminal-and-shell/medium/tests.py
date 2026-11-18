LOG = "\n".join(
    [f"epoch {i} loss: {1 / i:.4f}" for i in range(1, 13)]
    + ["ERROR cuda out of memory", "final accuracy 0.91"]
) + "\n"


def _fn(sol):
    fn = sol.get("run_pipeline")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน run_pipeline", "Function run_pipeline was not found")
    return fn


def _expect(sol, command, want, text=LOG):
    got = _fn(sol)(text, command)
    if got != want:
        raise Fail(f"{command!r} ควรได้ {want!r} แต่ได้ {got!r}", f"{command!r} should give {want!r}, got {got!r}")


@check("count", th="grep loss | wc -l นับบรรทัดที่มี loss", en="grep loss | wc -l counts the loss lines")
def _(sol):
    _expect(sol, "grep loss | wc -l", "12\n")


@check("invert", th="grep -v เก็บบรรทัดที่ไม่ตรง", en="grep -v keeps the lines that don't match")
def _(sol):
    _expect(sol, "grep -v loss", "ERROR cuda out of memory\nfinal accuracy 0.91\n")


@check("awk-head-tail", th="awk $NF, head และ tail", en="awk $NF, head and tail")
def _(sol):
    _expect(sol, "grep loss: | awk '{print $NF}' | head -n 3", "1.0000\n0.5000\n0.3333\n")
    _expect(sol, "grep loss | tail -n 2 | awk '{print $2}'", "11\n12\n")


@check("defaults", th="head ที่ไม่ระบุ -n ได้ 10 บรรทัด", en="head without -n gives 10 lines")
def _(sol):
    _expect(sol, "head | wc -l", "10\n")


@check("numeric-sort", th="sort -n เรียงตามค่าตัวเลข และ -r กลับลำดับ", en="sort -n sorts by numeric value and -r reverses")
def _(sol):
    _expect(sol, "sort -n -r | head -n 3", "12\n10\n9\n", text="9\n10\n2\n12\n")
    _expect(sol, "sort", "10\n12\n2\n9\n", text="9\n10\n2\n12\n")


@check("quoted", th="รูปแบบในเครื่องหมายคำพูดที่มีช่องว่าง", en="A quoted pattern with a space")
def _(sol):
    _expect(sol, "grep 'final accuracy' | awk '{print $NF}'", "0.91\n")


@check("empty-and-errors", th="ไม่มีผลลัพธ์ได้ \"\" และคำสั่งที่ไม่รองรับต้อง raise ValueError", en="No output gives \"\" and an unsupported command raises ValueError")
def _(sol):
    _expect(sol, "grep nothing-matches", "")
    try:
        got = _fn(sol)(LOG, "grep loss | rm -rf /")
    except ValueError:
        return
    raise Fail(f"คำสั่ง rm ไม่รองรับ ต้อง raise ValueError แต่ได้ {got!r}", f"rm is unsupported and must raise ValueError, got {got!r}")
