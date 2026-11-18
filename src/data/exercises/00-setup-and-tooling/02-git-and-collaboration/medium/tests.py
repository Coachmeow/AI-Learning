def _fn(sol):
    fn = sol.get("is_ignored")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน is_ignored", "Function is_ignored was not found")
    return fn


def _expect(fn, path, patterns, want):
    got = fn(path, patterns)
    if got is not want:
        raise Fail(
            f"is_ignored({path!r}, {patterns!r}) ควรได้ {want} แต่ได้ {got!r}",
            f"is_ignored({path!r}, {patterns!r}) should be {want}, got {got!r}",
        )


@check("name", th="รูปแบบอย่าง *.pt กันไฟล์ทุกระดับความลึก", en="A pattern like *.pt matches files at any depth")
def _(sol):
    fn = _fn(sol)
    _expect(fn, "model.pt", ["*.pt"], True)
    _expect(fn, "runs/3/best.pt", ["*.pt"], True)
    _expect(fn, "model.pth", ["*.pt"], False)
    _expect(fn, "notes.txt", ["*.pt", "*.safetensors"], False)


@check("comments", th="ข้ามบรรทัดว่างและคอมเมนต์ #", en="Skips blank lines and # comments")
def _(sol):
    fn = _fn(sol)
    _expect(fn, "#notes.txt", ["# model files", "#notes.txt", ""], False)
    _expect(fn, "a.pt", ["# model files", "", "*.pt"], True)


@check("dir", th="รูปแบบที่ลงท้าย / กันทุกอย่างในโฟลเดอร์ชื่อนั้น", en="A pattern ending in / excludes everything inside that folder")
def _(sol):
    fn = _fn(sol)
    _expect(fn, "checkpoints/epoch1.pt", ["checkpoints/"], True)
    _expect(fn, "exp/checkpoints/last.bin", ["checkpoints/"], True)


@check("dir-not-file", th="รูปแบบโฟลเดอร์ไม่กันไฟล์ที่ชื่อเหมือนกัน", en="A folder pattern does not exclude a file with that name")
def _(sol):
    _expect(_fn(sol), "checkpoints", ["checkpoints/"], False)
    _expect(_fn(sol), "src/checkpoints", ["checkpoints/"], False)


@check("anchored", th="รูปแบบที่ขึ้นต้น / เทียบจากรากเท่านั้น", en="A pattern starting with / matches from the root only")
def _(sol):
    fn = _fn(sol)
    _expect(fn, "data.csv", ["/data.csv"], True)
    _expect(fn, "raw/data.csv", ["/data.csv"], False)
    _expect(fn, "model.pt", ["/*.pt"], True)
    _expect(fn, "runs/best.pt", ["/*.pt"], False)
