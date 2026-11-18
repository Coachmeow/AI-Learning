def _fn(sol):
    fn = sol.get("apply_chmod")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน apply_chmod", "Function apply_chmod was not found")
    return fn


def _expect(fn, perms, spec, want):
    got = fn(perms, spec)
    if got != want:
        raise Fail(f"apply_chmod({perms!r}, {spec!r}) ควรได้ {want!r} แต่ได้ {got!r}", f"apply_chmod({perms!r}, {spec!r}) should be {want!r}, got {got!r}")


@check("plus-x", th="+x ให้ทุกคนรันได้ (chmod +x train.sh)", en="+x lets everyone run it (chmod +x train.sh)")
def _(sol):
    _expect(_fn(sol), "rw-r--r--", "+x", "rwxr-xr-x")


@check("octal", th="เลขฐานแปด 755 และ 644 แทนที่ทั้งหมด", en="Octal 755 and 644 replace everything")
def _(sol):
    _expect(_fn(sol), "---------", "755", "rwxr-xr-x")
    _expect(_fn(sol), "rwxrwxrwx", "644", "rw-r--r--")


@check("who", th="เลือกได้ว่าเปลี่ยนของใคร (u, g, o)", en="Picks whose permissions change (u, g, o)")
def _(sol):
    _expect(_fn(sol), "rw-r--r--", "u+x", "rwxr--r--")
    _expect(_fn(sol), "rw-rw-rw-", "go-w", "rw-r--r--")


@check("equals", th="= ตั้งให้มีเฉพาะสิทธิ์ที่ระบุ", en="= sets exactly the listed permissions")
def _(sol):
    _expect(_fn(sol), "rwxrwxrwx", "o=r", "rwxrwxr--")
    _expect(_fn(sol), "rwxr-xr-x", "a=r", "r--r--r--")


@check("commas", th="หลายข้อคั่นด้วยจุลภาค ทำตามลำดับ", en="Comma-separated clauses apply in order")
def _(sol):
    _expect(_fn(sol), "rw-rw-rw-", "u+x,go-w", "rwxr--r--")


@check("invalid", th="รูปแบบที่ไม่รองรับต้อง raise ValueError", en="An unsupported spec raises ValueError")
def _(sol):
    for bad in ("u+z", "999", "x+u"):
        try:
            got = _fn(sol)("rw-r--r--", bad)
        except ValueError:
            continue
        raise Fail(f"{bad!r} ไม่ใช่รูปแบบที่ถูกต้อง ต้อง raise ValueError แต่ได้ {got!r}", f"{bad!r} is not valid and must raise ValueError, got {got!r}")
