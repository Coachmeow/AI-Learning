import math


def _fn(sol):
    fn = sol.get("weights_gb")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน weights_gb", "Function weights_gb was not found")
    return fn


def _expect(fn, params, dtype, want):
    got = fn(params, dtype)
    if not isinstance(got, (int, float)) or not math.isclose(got, want, rel_tol=1e-9):
        raise Fail(
            f"weights_gb({params:,}, {dtype!r}) ควรได้ {want} GB แต่ได้ {got!r}",
            f"weights_gb({params:,}, {dtype!r}) should be {want} GB, got {got!r}",
        )


@check("fp16", th="โมเดล 7B แบบ fp16 ใช้ 14 GB", en="A 7B model in fp16 needs 14 GB")
def _(sol):
    _expect(_fn(sol), 7_000_000_000, "fp16", 14.0)


@check("fp32", th="fp32 ใช้ 4 byte ต่อพารามิเตอร์", en="fp32 uses 4 bytes per parameter")
def _(sol):
    _expect(_fn(sol), 1_000_000_000, "fp32", 4.0)


@check("int", th="int8 และ int4 ใช้หน่วยความจำน้อยลง", en="int8 and int4 use less memory")
def _(sol):
    _expect(_fn(sol), 7_000_000_000, "int8", 7.0)
    _expect(_fn(sol), 70_000_000_000, "int4", 35.0)


@check("units", th="ใช้ GB = 10⁹ byte ตามหลักของบทเรียน", en="Uses GB = 10⁹ bytes, as in the lesson")
def _(sol):
    _expect(_fn(sol), 12_000_000_000, "bf16", 24.0)
