LESSON = """FROM --platform=linux/amd64 nvidia/cuda:12.4.1-devel-ubuntu22.04

ENV PYTHONUNBUFFERED=1

RUN python -m pip install --no-cache-dir \\
    torch==2.6.0+cu124 \\
    --index-url https://download.pytorch.org/whl/cu124

WORKDIR /workspace
EXPOSE 8888
CMD ["python"]
"""


def _fn(sol):
    fn = sol.get("parse_dockerfile")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน parse_dockerfile", "Function parse_dockerfile was not found")
    return fn


def _expect(got, want):
    if [tuple(x) for x in (got or [])] != want:
        raise Fail(f"ควรได้ {want} แต่ได้ {got!r}", f"Expected {want}, got {got!r}")


@check("lesson", th="อ่าน Dockerfile ย่อจากบทเรียนได้ครบ 6 คำสั่ง", en="Reads a short version of the lesson's Dockerfile into 6 instructions")
def _(sol):
    got = _fn(sol)(LESSON)
    _expect(got, [
        ("FROM", "--platform=linux/amd64 nvidia/cuda:12.4.1-devel-ubuntu22.04"),
        ("ENV", "PYTHONUNBUFFERED=1"),
        ("RUN", "python -m pip install --no-cache-dir torch==2.6.0+cu124 --index-url https://download.pytorch.org/whl/cu124"),
        ("WORKDIR", "/workspace"),
        ("EXPOSE", "8888"),
        ("CMD", "[\"python\"]"),
    ])


@check("continuation", th="รวมบรรทัดที่ลงท้ายด้วย \\ โดยไม่เหลือ \\", en="Joins lines ending in \\ without leaving the \\")
def _(sol):
    _expect(_fn(sol)("RUN apt-get update && \\\n    apt-get install -y git\n"), [("RUN", "apt-get update && apt-get install -y git")])


@check("comments", th="ข้ามคอมเมนต์ทั้งนอกและในการต่อบรรทัด", en="Skips comments, also inside a continuation")
def _(sol):
    text = "# base image\nFROM python:3.12-slim\nRUN pip install \\\n    # the web server\n    flask\n"
    _expect(_fn(sol)(text), [("FROM", "python:3.12-slim"), ("RUN", "pip install flask")])


@check("uppercase", th="แปลงชื่อคำสั่งเป็นตัวพิมพ์ใหญ่", en="Uppercases the instruction name")
def _(sol):
    _expect(_fn(sol)("from python:3.12-slim\nworkdir /app\n"), [("FROM", "python:3.12-slim"), ("WORKDIR", "/app")])
