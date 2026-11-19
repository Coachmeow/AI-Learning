import math


def _check(sol, args, want, th, en):
    fn = sol.get("bayes")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน bayes", "Function bayes was not found")
    got = fn(*args)
    if not isinstance(got, (int, float)) or not math.isclose(got, want, abs_tol=1e-4):
        raise Fail(f"{th}: ควรได้ประมาณ {want} แต่ได้ {got!r}", f"{en}: should be about {want}, got {got!r}")


@check("medical", th="ชุดตรวจโรคในบทเรียน: ประมาณ 0.0098", en="The lesson's medical test: about 0.0098")
def _(sol):
    _check(sol, (0.0001, 0.99, 0.01), 0.0098, "bayes(0.0001, 0.99, 0.01)", "bayes(0.0001, 0.99, 0.01)")


@check("spam", th="ตัวอย่างสแปม \"lottery\": ประมาณ 0.9554", en="The \"lottery\" spam example: about 0.9554")
def _(sol):
    _check(sol, (0.3, 0.05, 0.001), 0.9554, "bayes(0.3, 0.05, 0.001)", "bayes(0.3, 0.05, 0.001)")


@check("common", th="โรคที่พบบ่อย (prior 0.2)", en="A common condition (prior 0.2)")
def _(sol):
    _check(sol, (0.2, 0.9, 0.1), 0.18 / 0.26, "bayes(0.2, 0.9, 0.1)", "bayes(0.2, 0.9, 0.1)")
