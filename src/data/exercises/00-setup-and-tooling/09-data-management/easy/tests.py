def _fn(sol):
    fn = sol.get("seeded_split")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน seeded_split", "Function seeded_split was not found")
    return fn


@check("sizes", th="ขนาด train/test ถูกต้องและครบทุกตัว", en="Train/test sizes are right and nothing is lost")
def _(sol):
    items = list(range(100))
    train, test = _fn(sol)(items, 0.2, 42)
    if len(test) != 20 or len(train) != 80 or sorted(train + test) != items:
        raise Fail(f"ควรได้ train 80 ตัว test 20 ตัว รวมกันครบ 0-99 แต่ได้ {len(train)} กับ {len(test)}", f"Expected 80 train and 20 test covering 0-99, got {len(train)} and {len(test)}")


@check("reproducible", th="seed เดียวกันได้ผลเหมือนเดิม", en="The same seed gives the same split")
def _(sol):
    items = [f"review-{i}" for i in range(200)]
    a = _fn(sol)(items, 0.1, 7)
    b = _fn(sol)(list(items), 0.1, 7)
    if a != b:
        raise Fail("เรียกสองครั้งด้วย seed=7 แล้วได้ผลไม่เหมือนกัน", "Two calls with seed=7 gave different splits")


@check("shuffled", th="สลับลำดับจริง และ seed ต่างกันได้ผลต่างกัน", en="Really shuffles, and different seeds differ")
def _(sol):
    items = list(range(200))
    train, test = _fn(sol)(items, 0.1, 1)
    if test == items[:20]:
        raise Fail("test เป็น 20 ตัวแรกตามลำดับเดิม แปลว่ายังไม่ได้สลับ", "test is the first 20 items in their original order, so nothing was shuffled")
    if _fn(sol)(items, 0.1, 2) == (train, test):
        raise Fail("seed=1 และ seed=2 ได้ผลเหมือนกัน", "seed=1 and seed=2 gave the same split")


@check("no-mutation", th="ไม่แก้ list ที่ส่งเข้ามา", en="Leaves the input list unchanged")
def _(sol):
    items = list(range(50))
    _fn(sol)(items, 0.2, 3)
    if items != list(range(50)):
        raise Fail("list ที่ส่งเข้ามาถูกสลับลำดับไปด้วย ให้สลับสำเนาแทน", "The list you were given got shuffled; shuffle a copy instead")
