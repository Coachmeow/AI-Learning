LESSON = """Host gpu-box
    HostName 203.0.113.50
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes
"""

LAYERED = """# lab machines
Host gpu-* lab
    User researcher
    Port 2222

Host gpu-a100
    HostName 10.0.0.12
    User admin

Host * !bastion
    ServerAliveInterval 60
    User ubuntu

Host *
    IdentityFile ~/.ssh/id_ed25519
"""


def _fn(sol):
    fn = sol.get("ssh_options")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน ssh_options", "Function ssh_options was not found")
    return fn


def _expect(sol, config, alias, want, th, en):
    got = _fn(sol)(config, alias)
    if got != want:
        raise Fail(f"{th}: ssh_options(..., {alias!r}) ควรได้ {want} แต่ได้ {got!r}", f"{en}: ssh_options(..., {alias!r}) should be {want}, got {got!r}")


@check("lesson", th="อ่าน config ของบทเรียนได้ (keyword เป็นตัวพิมพ์เล็ก)", en="Reads the lesson's config (keywords in lowercase)")
def _(sol):
    _expect(sol, LESSON, "gpu-box", {"hostname": "203.0.113.50", "user": "ubuntu", "identityfile": "~/.ssh/id_ed25519", "forwardagent": "yes"}, "config ของบทเรียน", "The lesson's config")


@check("first-wins", th="ค่าแรกที่พบชนะ บล็อกที่ตรงทีหลังไม่ทับ", en="The first value found wins; later matching blocks don't override it")
def _(sol):
    _expect(sol, LAYERED, "gpu-a100", {"user": "researcher", "port": "2222", "hostname": "10.0.0.12", "serveraliveinterval": "60", "identityfile": "~/.ssh/id_ed25519"}, "gpu-a100 ตรงกับ gpu-* ก่อน", "gpu-a100 matches gpu-* first")


@check("wildcard", th="รูปแบบ * และหลายรูปแบบในบรรทัดเดียว", en="* patterns and several patterns on one line")
def _(sol):
    _expect(sol, LAYERED, "lab", {"user": "researcher", "port": "2222", "serveraliveinterval": "60", "identityfile": "~/.ssh/id_ed25519", "hostname": "lab"}, "lab", "lab")


@check("default-hostname", th="ไม่มี HostName ใช้ alias แทน", en="Without HostName the alias is used")
def _(sol):
    _expect(sol, LESSON, "other-box", {"hostname": "other-box"}, "ไม่ตรงบล็อกไหนเลย", "No block matches")


@check("negation", th="!bastion ทำให้บล็อกนั้นไม่มีผลกับ bastion", en="!bastion keeps that block from applying to bastion", hidden=True)
def _(sol):
    _expect(sol, LAYERED, "bastion", {"identityfile": "~/.ssh/id_ed25519", "hostname": "bastion"}, "bastion", "bastion")


@check("equals-and-case", th="รองรับ Keyword=value และ keyword ตัวพิมพ์ปนกัน", en="Handles Keyword=value and mixed-case keywords", hidden=True)
def _(sol):
    cfg = "HOST box\n  hostName=192.0.2.7\n  USER = alice\n"
    _expect(sol, cfg, "box", {"hostname": "192.0.2.7", "user": "alice"}, "Keyword=value", "Keyword=value")


@check("global", th="ตัวเลือกก่อน Host แรกใช้กับทุกเครื่องและชนะเพราะมาก่อน", en="Options before the first Host apply everywhere and win by coming first", hidden=True)
def _(sol):
    cfg = "User everyone\nHost box\n  User alice\n  Port 22\n"
    _expect(sol, cfg, "box", {"user": "everyone", "port": "22", "hostname": "box"}, "User ก่อน Host แรก", "User before the first Host")
