def _fn(sol):
    fn = sol.get("to_octal")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน to_octal", "Function to_octal was not found")
    return fn


def _expect(fn, perms, want):
    got = fn(perms)
    if got != want:
        raise Fail(f"to_octal({perms!r}) ควรได้ {want!r} แต่ได้ {got!r}", f"to_octal({perms!r}) should be {want!r}, got {got!r}")


@check("lesson", th="ตัวอย่างจากบทเรียน rwxr-xr-- = 754", en="The lesson's example rwxr-xr-- = 754")
def _(sol):
    _expect(_fn(sol), "rwxr-xr--", "754")


@check("common", th="ค่าที่ใช้บ่อย 755 และ 644", en="The common values 755 and 644")
def _(sol):
    _expect(_fn(sol), "rwxr-xr-x", "755")
    _expect(_fn(sol), "rw-r--r--", "644")


@check("weights", th="w มีค่า 2 และ x มีค่า 1 (ไม่ใช่นับจำนวนตัวอักษร)", en="w counts 2 and x counts 1 (not a letter count)")
def _(sol):
    _expect(_fn(sol), "-w---x--x", "211")
    _expect(_fn(sol), "rw-------", "600")


@check("string", th="คืนเป็นสตริง 3 หลัก แม้ขึ้นต้นด้วย 0", en="Returns a 3-digit string, even with a leading 0")
def _(sol):
    _expect(_fn(sol), "------rwx", "007")
