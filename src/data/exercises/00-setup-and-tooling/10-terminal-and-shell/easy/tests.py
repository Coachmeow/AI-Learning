LOG = """starting run lr=0.001
epoch 1 loss: 1.0000
epoch 2 loss: 0.5000
WARNING: loss is noisy 9
epoch 3 loss: 0.3333
done
"""


def _fn(sol):
    fn = sol.get("extract_losses")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน extract_losses", "Function extract_losses was not found")
    return fn


@check("values", th="ดึงค่า loss ออกมาเป็น float ครบทุกบรรทัด", en="Pulls every loss value out as a float")
def _(sol):
    got = _fn(sol)(LOG)
    if got != [1.0, 0.5, 0.3333] or not all(type(x) is float for x in got):
        raise Fail(f"ควรได้ [1.0, 0.5, 0.3333] (float) แต่ได้ {got!r}", f"Expected [1.0, 0.5, 0.3333] (floats), got {got!r}")


@check("only-loss-colon", th="ข้ามบรรทัดที่ไม่มี 'loss:' แม้จะมีคำว่า loss", en="Skips lines without 'loss:', even if they say loss")
def _(sol):
    got = _fn(sol)("WARNING: loss is noisy 9\nepoch 7 loss: 0.25\n")
    if got != [0.25]:
        raise Fail(f"ควรได้ [0.25] แต่ได้ {got!r}", f"Expected [0.25], got {got!r}")


@check("last-field", th="ใช้คำสุดท้ายของบรรทัด ไม่ใช่ตัวเลขตัวแรก", en="Uses the last word, not the first number")
def _(sol):
    got = _fn(sol)("epoch 42 step 9000 loss: 0.125\n")
    if got != [0.125]:
        raise Fail(f"ควรได้ [0.125] แต่ได้ {got!r}", f"Expected [0.125], got {got!r}")


@check("empty", th="log ที่ไม่มี loss ได้ list ว่าง", en="A log without losses gives an empty list")
def _(sol):
    if _fn(sol)("no numbers here\n") != []:
        raise Fail("ควรได้ []", "Expected []")
