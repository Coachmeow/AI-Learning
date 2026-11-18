IDS = [f"review-{i}" for i in range(12)]


def _fn(sol):
    fn = sol.get("hash_split")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน hash_split", "Function hash_split was not found")
    return fn


@check("exact", th="แต่ละ id ไปอยู่ชุดตาม bucket ของ md5", en="Each id lands where its md5 bucket says")
def _(sol):
    got = _fn(sol)(IDS, val_frac=0.3, test_frac=0.2)
    want = {
        "train": ["review-0", "review-1", "review-2", "review-5", "review-7", "review-11"],
        "val": ["review-3", "review-6", "review-8", "review-9"],
        "test": ["review-4", "review-10"],
    }
    if got != want:
        raise Fail(f"val_frac=0.3, test_frac=0.2 ควรได้ {want} แต่ได้ {got!r}", f"val_frac=0.3, test_frac=0.2 should give {want}, got {got!r}")


@check("stable", th="เพิ่มข้อมูลใหม่แล้ว id เดิมยังอยู่ชุดเดิม", en="Adding new data never moves existing ids")
def _(sol):
    old = [f"img-{i}" for i in range(1000)]
    before = _fn(sol)(old)
    after = _fn(sol)(old + [f"img-new-{i}" for i in range(500)])
    for name in ("train", "val", "test"):
        kept = [x for x in after[name] if not x.startswith("img-new-")]
        if kept != before[name]:
            raise Fail(f"หลังเพิ่มข้อมูลใหม่ ชุด {name} ของ id เดิมเปลี่ยนไป", f"After adding new data, the old ids in {name} changed")


@check("proportions", th="สัดส่วนใกล้ 80/10/10 เมื่อมีข้อมูลมาก", en="Proportions are close to 80/10/10 with lots of data")
def _(sol):
    got = _fn(sol)([f"doc-{i}" for i in range(10000)])
    sizes = {k: len(v) for k, v in got.items()}
    if sum(sizes.values()) != 10000 or not (850 <= sizes["test"] <= 1150 and 850 <= sizes["val"] <= 1150):
        raise Fail(f"ควรได้ val และ test ราว 1,000 ตัว และรวมกันครบ 10,000 แต่ได้ {sizes}", f"Expected about 1,000 each in val and test and 10,000 in total, got {sizes}")


@check("order", th="ในแต่ละชุดคงลำดับเดิมของ ids", en="Each split keeps the original order of ids")
def _(sol):
    ids = [f"z-{i}" for i in range(300, 0, -1)]
    got = _fn(sol)(ids)
    for name, part in got.items():
        pos = [ids.index(x) for x in part]
        if pos != sorted(pos):
            raise Fail(f"ชุด {name} ไม่ได้เรียงตามลำดับเดิม", f"The {name} split is not in the original order")
