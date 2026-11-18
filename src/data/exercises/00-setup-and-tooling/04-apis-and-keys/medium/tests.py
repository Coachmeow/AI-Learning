def _fn(sol):
    fn = sol.get("parse_env")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน parse_env", "Function parse_env was not found")
    return fn


def _expect(fn, text, want):
    got = fn(text)
    if got != want:
        raise Fail(f"parse_env({text!r}) ควรได้ {want!r} แต่ได้ {got!r}", f"parse_env({text!r}) should be {want!r}, got {got!r}")


@check("basic", th="อ่านไฟล์ .env ตัวอย่างของบทเรียนได้", en="Reads the lesson's example .env")
def _(sol):
    _expect(_fn(sol), "ANTHROPIC_API_KEY=sk-ant-...\nOPENAI_API_KEY=sk-...\n", {"ANTHROPIC_API_KEY": "sk-ant-...", "OPENAI_API_KEY": "sk-..."})


@check("skip", th="ข้ามบรรทัดว่างและคอมเมนต์", en="Skips blank lines and comments")
def _(sol):
    _expect(_fn(sol), "# keys for local dev\n\n   # indented comment\nLLM_MODEL=claude-sonnet-5\n", {"LLM_MODEL": "claude-sonnet-5"})


@check("first-equals", th="แยกที่ = ตัวแรก ค่ามี = อยู่ข้างในได้", en="Splits at the first =, so values may contain =")
def _(sol):
    _expect(_fn(sol), "DB_URL=postgres://u:p@host/db?sslmode=require\n", {"DB_URL": "postgres://u:p@host/db?sslmode=require"})


@check("export-spaces", th="ตัด export และช่องว่างรอบชื่อกับค่า", en="Drops export and spaces around names and values")
def _(sol):
    _expect(_fn(sol), "export ANTHROPIC_API_KEY = sk-ant-123\n  OTHER=  x  \n", {"ANTHROPIC_API_KEY": "sk-ant-123", "OTHER": "x"})


@check("quotes", th="ตัดเครื่องหมายคำพูดคู่ที่ตรงกันหัวท้าย", en="Removes a matching pair of surrounding quotes")
def _(sol):
    _expect(_fn(sol), "A=\"hello world\"\nB='single'\nC=\"\"\n", {"A": "hello world", "B": "single", "C": ""})


@check("mismatched", th="ไม่ตัดเครื่องหมายคำพูดที่ไม่ตรงกัน", en="Leaves quotes that don't match")
def _(sol):
    _expect(_fn(sol), "A=\"open\nB=it's\n", {"A": "\"open", "B": "it's"})


@check("later-wins", th="ชื่อซ้ำ ค่าบรรทัดหลังชนะ", en="When a name repeats, the later line wins")
def _(sol):
    _expect(_fn(sol), "MODEL=a\nMODEL=b\n", {"MODEL": "b"})


@check("bad-line", th="บรรทัดที่ไม่มี = ต้อง raise ValueError พร้อมเลขบรรทัด", en="A line without = raises ValueError with the line number")
def _(sol):
    try:
        got = _fn(sol)("A=1\n# ok\nOOPS\n")
    except ValueError as e:
        if "3" not in str(e):
            raise Fail(f"ข้อความ error ควรบอกเลขบรรทัด 3 แต่ได้ {str(e)!r}", f"The error should mention line 3, got {str(e)!r}")
        return
    raise Fail(f"บรรทัด 'OOPS' ต้อง raise ValueError แต่ได้ {got!r}", f"The line 'OOPS' must raise ValueError, got {got!r}")
