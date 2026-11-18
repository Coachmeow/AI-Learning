def _fn(sol):
    fn = sol.get("make_grid")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน make_grid", "Function make_grid was not found")
    return fn


@check("shape", th="ขนาดและค่าถูกต้อง", en="The right size and values")
def _(sol):
    got = _fn(sol)(2, 3)
    if got != [[0, 0, 0], [0, 0, 0]]:
        raise Fail(f"make_grid(2, 3) ควรได้ [[0, 0, 0], [0, 0, 0]] แต่ได้ {got!r}", f"make_grid(2, 3) should be [[0, 0, 0], [0, 0, 0]], got {got!r}")
    if _fn(sol)(1, 2, value=0.5) != [[0.5, 0.5]]:
        raise Fail("make_grid(1, 2, value=0.5) ควรได้ [[0.5, 0.5]]", "make_grid(1, 2, value=0.5) should be [[0.5, 0.5]]")


@check("independent", th="แก้แถวหนึ่งแล้วแถวอื่นไม่เปลี่ยน", en="Changing one row leaves the others alone")
def _(sol):
    grid = _fn(sol)(3, 2)
    try:
        grid[0][0] = 1
    except TypeError:
        raise Fail("แต่ละแถวต้องเป็น list ที่แก้ค่าได้", "Each row must be a list you can change")
    if grid != [[1, 0], [0, 0], [0, 0]]:
        raise Fail(f"หลัง grid[0][0] = 1 ควรได้ [[1, 0], [0, 0], [0, 0]] แต่ได้ {grid!r}", f"After grid[0][0] = 1 the grid should be [[1, 0], [0, 0], [0, 0]], got {grid!r}")


@check("rows-are-lists", th="ทุกแถวเป็น list คนละตัว", en="Every row is a separate list object")
def _(sol):
    grid = _fn(sol)(4, 1)
    if len({id(r) for r in grid}) != 4 or not all(isinstance(r, list) for r in grid):
        raise Fail("แถวทั้ง 4 ต้องเป็น list คนละตัว", "All 4 rows must be different list objects")
