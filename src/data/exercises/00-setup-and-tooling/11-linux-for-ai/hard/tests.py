K, M, G = 1024, 1024 ** 2, 1024 ** 3

FILES = {
    "train.py": 4 * K,
    "data/imdb/train.parquet": int(1.5 * G),
    "data/imdb/test.parquet": 512 * M,
    "data/mnist/images.bin": 9 * G,
    "checkpoints/epoch_01/model.safetensors": 14 * G,
    "checkpoints/epoch_02/model.safetensors": 14 * G,
    "logs/train.log": 300,
}


def _fns(sol):
    h, s = sol.get("human"), sol.get("space_hogs")
    if h is None or s is None:
        raise Fail("ต้องมีทั้งฟังก์ชัน human และ space_hogs", "Both human and space_hogs are needed")
    return h, s


def _expect_list(got, want, th, en):
    if [tuple(x) for x in (got or [])] != want:
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("human", th="แปลงขนาดเป็นแบบอ่านง่ายตามกติกา", en="Formats sizes by the rules")
def _(sol):
    h, _ = _fns(sol)
    cases = [(300, "300B"), (1023, "1023B"), (1536, "1.5K"), (int(1.5 * G), "1.5G"), (14 * G, "14G"), (512 * M, "512M"), (2 * 1024 ** 4, "2.0T")]
    for n, want in cases:
        got = h(n)
        if got != want:
            raise Fail(f"human({n}) ควรได้ {want!r} แต่ได้ {got!r}", f"human({n}) should be {want!r}, got {got!r}")


@check("depth-1", th="--max-depth=1 ได้รากและโฟลเดอร์ชั้นแรก เรียงจากใหญ่ไปเล็ก", en="--max-depth=1 gives the root and first-level folders, largest first")
def _(sol):
    _, s = _fns(sol)
    _expect_list(s(FILES, 1, 10), [("39G", "."), ("28G", "checkpoints"), ("11G", "data"), ("300B", "logs")], "max_depth=1", "max_depth=1")


@check("depth-2-top", th="--max-depth=2 แล้วเลือกแค่ 4 อันดับแรก", en="--max-depth=2, keeping only the top 4")
def _(sol):
    _, s = _fns(sol)
    _expect_list(s(FILES, 2, 4), [("39G", "."), ("28G", "checkpoints"), ("14G", "checkpoints/epoch_01"), ("14G", "checkpoints/epoch_02")], "max_depth=2, top=4", "max_depth=2, top=4")


@check("numeric-order", th="เรียงตามขนาดจริง ไม่ใช่ตามข้อความ (9.0G น้อยกว่า 14G)", en="Sorts by real size, not by text (9.0G is less than 14G)")
def _(sol):
    _, s = _fns(sol)
    files = {"a/x": 9 * G, "b/y": 14 * G}
    _expect_list(s(files, 1, 3), [("23G", "."), ("14G", "b"), ("9.0G", "a")], "9G กับ 14G", "9G and 14G")


@check("root-only", th="--max-depth=0 ได้แค่ราก", en="--max-depth=0 gives only the root", hidden=True)
def _(sol):
    _, s = _fns(sol)
    _expect_list(s(FILES, 0, 5), [("39G", ".")], "max_depth=0", "max_depth=0")


@check("deep", th="นับไฟล์ในโฟลเดอร์ลึกๆ เข้าโฟลเดอร์แม่ทุกชั้น", en="Files deep down count towards every parent", hidden=True)
def _(sol):
    _, s = _fns(sol)
    files = {"a/b/c/d/e.bin": 2 * M, "a/f.bin": 1 * M}
    _expect_list(s(files, 3, 10), [("3.0M", "."), ("3.0M", "a"), ("2.0M", "a/b"), ("2.0M", "a/b/c")], "โฟลเดอร์ซ้อนกันหลายชั้น", "Nested folders")
