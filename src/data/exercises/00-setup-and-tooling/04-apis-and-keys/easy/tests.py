def _fn(sol):
    fn = sol.get("mask_key")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน mask_key", "Function mask_key was not found")
    return fn


def _expect(fn, key, want):
    got = fn(key)
    if got != want:
        raise Fail(f"mask_key({key!r}) ควรได้ {want!r} แต่ได้ {got!r}", f"mask_key({key!r}) should be {want!r}, got {got!r}")


@check("anthropic", th="ซ่อน key ของ Anthropic ได้ถูกต้อง", en="Masks an Anthropic key correctly")
def _(sol):
    _expect(_fn(sol), "sk-ant-api03-Xy7Qa9Lm2Pz8Rt4W", "sk-ant-...Rt4W")


@check("openai", th="ใช้ได้กับ key แบบอื่นด้วย", en="Works for other key formats too")
def _(sol):
    _expect(_fn(sol), "sk-proj-abcdefghij0123", "sk-proj...0123")


@check("short", th="key ที่สั้น (ไม่เกิน 12 ตัว) ซ่อนทั้งหมด", en="A short key (12 characters or fewer) is fully hidden")
def _(sol):
    _expect(_fn(sol), "sk-1234", "***")
    _expect(_fn(sol), "abcdefghijkl", "***")
    _expect(_fn(sol), "abcdefghijklm", "abcdefg...jklm")


@check("hidden-middle", th="ไม่มีส่วนกลางของ key หลุดออกมา", en="No part of the middle of the key leaks")
def _(sol):
    key = "sk-ant-SECRETSECRETSECRET-wxyz"
    got = _fn(sol)(key)
    if "SECRET" in got:
        raise Fail(f"ผลลัพธ์ยังมีส่วนกลางของ key: {got!r}", f"The result still shows the middle of the key: {got!r}")
