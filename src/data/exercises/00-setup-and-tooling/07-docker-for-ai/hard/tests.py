GOOD = [
    "FROM python:3.12-slim",
    "WORKDIR /app",
    "COPY requirements.txt .",
    "RUN pip install -r requirements.txt",
    "COPY . .",
    "CMD [\"python\", \"serve.py\"]",
]
BAD = [
    "FROM python:3.12-slim",
    "WORKDIR /app",
    "COPY . .",
    "RUN pip install -r requirements.txt",
    "CMD [\"python\", \"serve.py\"]",
]
C, R = "cached", "rebuild"


def _fn(sol):
    fn = sol.get("rebuild_plan")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน rebuild_plan", "Function rebuild_plan was not found")
    return fn


def _expect(sol, old, new, changed, want, th, en):
    got = _fn(sol)(list(old), list(new), set(changed))
    if list(got) != want:
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("unchanged", th="ไม่มีอะไรเปลี่ยน ใช้แคชทั้งหมด", en="Nothing changed: everything is cached")
def _(sol):
    _expect(sol, GOOD, GOOD, [], [C] * 6, "ไม่มีไฟล์เปลี่ยน", "No files changed")


@check("good-order", th="แก้โค้ด: Dockerfile ที่เรียงดี build ใหม่แค่ท้ายๆ", en="A code edit only rebuilds the tail of a well-ordered Dockerfile")
def _(sol):
    _expect(sol, GOOD, GOOD, ["serve.py"], [C, C, C, C, R, R], "แก้ serve.py", "Edited serve.py")


@check("bad-order", th="COPY . ก่อน pip install ทำให้ติดตั้งแพ็กเกจใหม่ทุกครั้ง", en="COPY . before pip install reinstalls the packages every time")
def _(sol):
    _expect(sol, BAD, BAD, ["serve.py"], [C, C, R, R, R], "แก้ serve.py ใน Dockerfile ที่เรียงไม่ดี", "Edited serve.py with the badly ordered Dockerfile")


@check("requirements", th="แก้ requirements.txt build ใหม่ตั้งแต่ COPY requirements.txt", en="Editing requirements.txt rebuilds from COPY requirements.txt")
def _(sol):
    _expect(sol, GOOD, GOOD, ["requirements.txt"], [C, C, R, R, R, R], "แก้ requirements.txt", "Edited requirements.txt")


@check("edited-instruction", th="แก้คำสั่งใน Dockerfile build ใหม่ตั้งแต่บรรทัดนั้น", en="Editing an instruction rebuilds from that line")
def _(sol):
    new = list(GOOD)
    new[3] = "RUN pip install --no-cache-dir -r requirements.txt"
    _expect(sol, GOOD, new, [], [C, C, C, R, R, R], "เปลี่ยนคำสั่ง RUN", "Changed the RUN line")


@check("folder", th="ต้นทางที่เป็นโฟลเดอร์นับไฟล์ข้างใน", en="A folder source covers the files inside it", hidden=True)
def _(sol):
    ins = ["FROM python:3.12-slim", "COPY src/ /app/src/", "COPY configs /app/configs", "RUN echo done"]
    _expect(sol, ins, ins, ["configs/train.yaml"], [C, C, R, R], "แก้ configs/train.yaml", "Edited configs/train.yaml")
    _expect(sol, ins, ins, ["src/model.py"], [C, R, R, R], "แก้ src/model.py", "Edited src/model.py")


@check("not-prefix", th="src ไม่ครอบคลุม src2/a.py หรือ srcfile.txt", en="src does not cover src2/a.py or srcfile.txt", hidden=True)
def _(sol):
    ins = ["FROM python:3.12-slim", "COPY src /app/src", "RUN echo done"]
    _expect(sol, ins, ins, ["src2/a.py", "srcfile.txt"], [C, C, C], "แก้ไฟล์นอกโฟลเดอร์ src", "Edited files outside src")


@check("destination", th="ปลายทางและตัวเลือก -- ไม่นับเป็นต้นทาง", en="The destination and -- options are not sources", hidden=True)
def _(sol):
    ins = ["FROM python:3.12-slim", "COPY --chown=app:app requirements.txt app", "RUN echo ok"]
    _expect(sol, ins, ins, ["app/main.py"], [C, C, C], "แก้ไฟล์ในปลายทาง app/", "Edited a file under the destination app/")


@check("longer", th="คำสั่งที่เพิ่มต่อท้ายต้อง build ใหม่", en="Instructions appended at the end are rebuilt", hidden=True)
def _(sol):
    _expect(sol, GOOD[:4], GOOD, [], [C, C, C, C, R, R], "เพิ่มสองคำสั่งท้ายไฟล์", "Two instructions appended")
