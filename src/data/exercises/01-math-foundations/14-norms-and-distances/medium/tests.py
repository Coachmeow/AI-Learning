def _is(sol, a, b, want):
    fn = sol.get("edit_distance")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน edit_distance", "Function edit_distance was not found")
    got = fn(a, b)
    if got != want:
        raise Fail(f"edit_distance({a!r}, {b!r}) ควรเป็น {want} แต่ได้ {got!r}", f"edit_distance({a!r}, {b!r}) should be {want}, got {got!r}")


@check("kitten", th="\"kitten\" กับ \"sitting\": 3", en="\"kitten\" and \"sitting\": 3")
def _(sol):
    _is(sol, "kitten", "sitting", 3)


@check("shift", th="\"flaw\" กับ \"lawn\": 2 (ลบ f แล้วแทรก n)", en="\"flaw\" and \"lawn\": 2 (delete f, insert n)")
def _(sol):
    _is(sol, "flaw", "lawn", 2)


@check("empty", th="สตริงว่าง", en="Empty strings")
def _(sol):
    _is(sol, "", "abc", 3)
    _is(sol, "abc", "", 3)
    _is(sol, "", "", 0)


@check("same-substitute", th="สตริงเดียวกันได้ 0 และแทนที่ตัวเดียวได้ 1", en="The same string gives 0, one substitution gives 1", hidden=True)
def _(sol):
    _is(sol, "distance", "distance", 0)
    _is(sol, "cat", "cut", 1)


@check("longer", th="สตริงที่ยาวขึ้นและสลับลำดับได้", en="Longer strings, in either order", hidden=True)
def _(sol):
    _is(sol, "intention", "execution", 5)
    _is(sol, "execution", "intention", 5)
    _is(sol, "sunday", "saturday", 3)


@check("middle-delete", th="ลบตัวอักษรตรงกลาง: \"abcd\" กับ \"abd\" ได้ 1", en="Deleting a middle character: \"abcd\" and \"abd\" give 1")
def _(sol):
    _is(sol, "abcd", "abd", 1)
    _is(sol, "abd", "abcd", 1)
