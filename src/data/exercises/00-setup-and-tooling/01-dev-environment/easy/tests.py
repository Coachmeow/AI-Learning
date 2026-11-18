def _fn(sol):
    fn = sol.get("is_new_enough")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน is_new_enough", "Function is_new_enough was not found")
    return fn


def _expect(fn, version, minimum, want):
    got = fn(version, minimum)
    if got is not want:
        raise Fail(
            f"is_new_enough({version!r}, {minimum!r}) ควรได้ {want} แต่ได้ {got!r}",
            f"is_new_enough({version!r}, {minimum!r}) should be {want}, got {got!r}",
        )


@check("newer", th="เวอร์ชันที่ใหม่กว่าผ่าน", en="A newer version passes")
def _(sol):
    _expect(_fn(sol), "3.12.4", "3.11", True)
    _expect(_fn(sol), "22.11.0", "20", True)


@check("older", th="เวอร์ชันที่เก่ากว่าไม่ผ่าน", en="An older version fails")
def _(sol):
    _expect(_fn(sol), "18.19.0", "20", False)
    _expect(_fn(sol), "3.10.2", "3.11", False)


@check("numeric", th="เทียบเป็นตัวเลข ไม่ใช่ตัวอักษร (3.9 เก่ากว่า 3.11)", en="Compares numbers, not text (3.9 is older than 3.11)")
def _(sol):
    _expect(_fn(sol), "3.9.18", "3.11", False)
    _expect(_fn(sol), "3.11.0", "3.9", True)


@check("equal", th="เวอร์ชันเท่ากันถือว่าผ่าน แม้เขียนจำนวนส่วนไม่เท่ากัน", en="Equal versions pass, even with a different number of parts")
def _(sol):
    _expect(_fn(sol), "3.11", "3.11.0", True)
    _expect(_fn(sol), "3.11.0", "3.11", True)
    _expect(_fn(sol), "20", "20", True)


@check("minor-patch", th="ดูเลขรองและเลขแพตช์ด้วย ไม่ใช่แค่เลขหลัก", en="Looks at the minor and patch numbers, not only the major")
def _(sol):
    _expect(_fn(sol), "3.10.1", "3.10.2", False)
    _expect(_fn(sol), "1.82.0", "1.75", True)
