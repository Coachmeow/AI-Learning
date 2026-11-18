def _fn(sol):
    fn = sol.get("blob_hash")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน blob_hash", "Function blob_hash was not found")
    return fn


def _expect(fn, content, want):
    got = fn(content)
    if got != want:
        raise Fail(
            f"blob_hash({content!r}) ควรได้ {want} (ค่าเดียวกับ git hash-object) แต่ได้ {got!r}",
            f"blob_hash({content!r}) should be {want} (what git hash-object prints), got {got!r}",
        )


@check("empty", th="ไฟล์เปล่าได้ id เดียวกับ git", en="An empty file gets git's id")
def _(sol):
    _expect(_fn(sol), b"", "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")


@check("hello", th="ไฟล์ที่มีข้อความ hello ได้ id เดียวกับ git", en="A file containing hello gets git's id")
def _(sol):
    _expect(_fn(sol), b"hello\n", "ce013625030ba8dba906f756967f9e9ca394464a")


@check("bytes", th="นับขนาดเป็น byte ไม่ใช่จำนวนตัวอักษร (ไฟล์ภาษาไทย)", en="Counts the size in bytes, not characters (a Thai file)")
def _(sol):
    _expect(_fn(sol), "สวัสดี\n".encode("utf-8"), "56d6550e59af4df8e5bf737685ac5c9afad08ad7")


@check("format", th="คืนค่าเป็นสตริงฐานสิบหก 40 ตัว", en="Returns a 40-character hex string")
def _(sol):
    got = _fn(sol)(b"x")
    if not (isinstance(got, str) and len(got) == 40 and all(c in "0123456789abcdef" for c in got)):
        raise Fail(f"ต้องได้สตริงฐานสิบหก 40 ตัว (SHA-1) แต่ได้ {got!r}", f"Expected a 40-character hex string (SHA-1), got {got!r}")
