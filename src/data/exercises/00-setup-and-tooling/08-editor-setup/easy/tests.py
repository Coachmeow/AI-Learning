def _fn(sol):
    fn = sol.get("long_lines")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน long_lines", "Function long_lines was not found")
    return fn


def _expect(got, want, th, en):
    if [tuple(x) for x in (got or [])] != want:
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("finds", th="หาบรรทัดที่ยาวเกิน 88 พร้อมเลขบรรทัดที่เริ่มจาก 1", en="Finds lines over 88 with line numbers from 1")
def _(sol):
    text = "import torch\n" + "x = " + "1 + " * 30 + "1\n" + "print(x)\n"
    _expect(_fn(sol)(text), [(2, 125)], "บรรทัดที่ 2 ยาว 125 ตัว", "Line 2 is 125 characters")


@check("exact", th="ยาวเท่า limit พอดีไม่นับ", en="A line exactly at the limit does not count")
def _(sol):
    text = "a" * 88 + "\n" + "b" * 89 + "\n"
    _expect(_fn(sol)(text), [(2, 89)], "บรรทัดยาว 88 และ 89", "Lines of 88 and 89")


@check("limit", th="ใช้ limit ที่ส่งเข้ามา เช่น 120", en="Uses the limit you pass, such as 120")
def _(sol):
    text = "c" * 100 + "\n" + "d" * 121
    _expect(_fn(sol)(text, limit=120), [(2, 121)], "limit=120", "limit=120")


@check("none", th="ไม่มีบรรทัดยาวเกิน ได้ list ว่าง", en="No long lines gives an empty list")
def _(sol):
    _expect(_fn(sol)("short\nlines\n"), [], "บรรทัดสั้นทั้งหมด", "All short lines")
