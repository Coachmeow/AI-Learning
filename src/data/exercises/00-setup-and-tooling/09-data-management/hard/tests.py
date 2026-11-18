import math
import string

_STRIP = str.maketrans("", "", string.punctuation)


def _norm(t):
    return " ".join(t.lower().translate(_STRIP).split())


REVIEWS = []
for i in range(60):
    REVIEWS.append(f"Review number {i} was fine")
    if i % 6 == 0:
        REVIEWS.append(f"  REVIEW number {i} was fine!!  ")


def _fn(sol):
    fn = sol.get("leak_free_split")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน leak_free_split", "Function leak_free_split was not found")
    return fn


def _no_leak(train, test):
    shared = {_norm(t) for t in train} & {_norm(t) for t in test}
    if shared:
        raise Fail(f"ข้อความซ้ำอยู่ทั้งใน train และ test: {sorted(shared)[:2]}", f"Duplicate texts appear in both train and test: {sorted(shared)[:2]}")


@check("no-leak", th="ข้อความที่ซ้ำกัน (ต่างกันแค่ตัวพิมพ์ ช่องว่าง เครื่องหมาย) อยู่ชุดเดียวกัน", en="Duplicates (differing only in case, spaces, punctuation) stay together")
def _(sol):
    for seed in range(5):
        train, test = _fn(sol)(REVIEWS, 0.25, seed)
        _no_leak(train, test)


@check("size", th="ชุด test มีอย่างน้อย ceil(n * test_frac) และไม่เกินเพราะกลุ่มสุดท้าย", en="Test holds at least ceil(n * test_frac), overshooting only by the last group")
def _(sol):
    train, test = _fn(sol)(REVIEWS, 0.25, 3)
    target = math.ceil(len(REVIEWS) * 0.25)
    if len(train) + len(test) != len(REVIEWS) or not (target <= len(test) <= target + 1):
        raise Fail(f"ควรได้ test {target} หรือ {target + 1} ตัวจาก {len(REVIEWS)} แต่ได้ train {len(train)} test {len(test)}", f"Expected {target} or {target + 1} test texts out of {len(REVIEWS)}, got train {len(train)} test {len(test)}")
    pairs = []
    for i in range(10):
        pairs += [f"pair {i}", f"Pair {i}."]
    train, test = _fn(sol)(pairs, 0.25, 0)
    if len(test) != 6:
        raise Fail(f"ข้อความ 20 ตัวเป็นคู่ซ้ำ 10 คู่ เป้าคือ 5 จึงต้องหยิบ 3 คู่ (6 ตัว) แต่ได้ test {len(test)} ตัว", f"20 texts in 10 duplicate pairs with a target of 5 must take 3 pairs (6 texts), got {len(test)} test texts")


@check("deterministic", th="seed เดียวกันได้ผลเหมือนเดิม", en="The same seed gives the same result")
def _(sol):
    a = _fn(sol)(REVIEWS, 0.2, 11)
    b = _fn(sol)(list(REVIEWS), 0.2, 11)
    if a != b:
        raise Fail("เรียกสองครั้งด้วย seed=11 แล้วได้ผลไม่เหมือนกัน", "Two calls with seed=11 gave different results")


@check("order", th="ทั้ง train และ test คงลำดับเดิม", en="Train and test both keep the original order")
def _(sol):
    train, test = _fn(sol)(REVIEWS, 0.3, 5)
    for name, part in (("train", train), ("test", test)):
        pos = [REVIEWS.index(t) for t in part]
        if pos != sorted(pos):
            raise Fail(f"ชุด {name} ไม่ได้เรียงตามลำดับเดิม", f"The {name} split is not in the original order")


@check("big-group", th="กลุ่มใหญ่ไม่ถูกตัดครึ่ง แม้จะทำให้ test เกินเป้า", en="A large group is never cut in half, even if test overshoots", hidden=True)
def _(sol):
    texts = ["Same text."] * 8 + [f"other {i}" for i in range(12)]
    for seed in range(8):
        train, test = _fn(sol)(texts, 0.1, seed)
        _no_leak(train, test)
        if len(test) < 2:
            raise Fail(f"seed={seed}: test ควรมีอย่างน้อย 2 ตัว แต่ได้ {len(test)}", f"seed={seed}: test should hold at least 2 texts, got {len(test)}")


@check("edge", th="ไม่มีข้อมูลหรือ test_frac=0 ก็ทำงานได้", en="Works with no data or with test_frac=0", hidden=True)
def _(sol):
    if tuple(_fn(sol)([], 0.2, 1)) != ([], []):
        raise Fail("ข้อมูลว่างควรได้ ([], [])", "Empty input should give ([], [])")
    train, test = _fn(sol)(["a", "b", "c"], 0.0, 1)
    if test or train != ["a", "b", "c"]:
        raise Fail(f"test_frac=0 ควรได้ train ครบทุกตัวและ test ว่าง แต่ได้ {train!r}, {test!r}", f"test_frac=0 should keep everything in train, got {train!r}, {test!r}")
