def _fn(sol):
    fn = sol.get("run_args")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน run_args", "Function run_args was not found")
    return fn


def _expect(got, want):
    if got != want:
        raise Fail(f"ควรได้ {want} แต่ได้ {got!r}", f"Expected {want}, got {got!r}")


@check("lesson", th="ประกอบคำสั่งรัน Jupyter ของบทเรียนได้", en="Builds the lesson's Jupyter run command")
def _(sol):
    got = _fn(sol)("ai-dev", {"/home/me/course": "/workspace", "/home/me/models": "/models"}, {8888: 8888})
    _expect(got, ["docker", "run", "--rm", "--gpus", "all", "-v", "/home/me/course:/workspace", "-v", "/home/me/models:/models", "-p", "8888:8888", "ai-dev"])


@check("host-left", th="ฝั่งเครื่องหลักอยู่ซ้ายของ :", en="The host side is left of the :")
def _(sol):
    got = _fn(sol)("api", {}, {5001: 5000}, gpus=False)
    _expect(got, ["docker", "run", "--rm", "-p", "5001:5000", "api"])


@check("separate-args", th="ตัวเลือกกับค่าแยกเป็นคนละอาร์กิวเมนต์", en="Each flag and its value are separate arguments")
def _(sol):
    got = _fn(sol)("x", {"/d": "/data"}, {}, gpus=False)
    _expect(got, ["docker", "run", "--rm", "-v", "/d:/data", "x"])


@check("empty", th="ไม่มี volume และพอร์ต ได้แค่คำสั่งพื้นฐาน", en="With no volumes or ports you get the bare command")
def _(sol):
    _expect(_fn(sol)("python:3.12-slim", {}, {}, gpus=False), ["docker", "run", "--rm", "python:3.12-slim"])
