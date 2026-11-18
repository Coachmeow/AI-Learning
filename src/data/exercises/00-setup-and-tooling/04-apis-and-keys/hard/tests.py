class Server:
    """Replies with the given (status, headers, body) tuples in order and counts calls."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = 0

    def send(self, request):
        self.calls += 1
        if not self.replies:
            raise AssertionError("send() was called more often than expected")
        return self.replies.pop(0)


class Sleeper:
    def __init__(self):
        self.waits = []

    def __call__(self, seconds):
        self.waits.append(seconds)


def _run(sol, replies, **kw):
    fn = sol.get("call_with_retry")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน call_with_retry", "Function call_with_retry was not found")
    server, sleeper = Server(replies), Sleeper()
    try:
        out = fn(server.send, {"q": 1}, sleep=sleeper, **kw)
        return out, None, server, sleeper
    except Exception as e:  # noqa: BLE001
        if type(e).__name__ != "ApiError":
            raise
        return None, e, server, sleeper


OK = (200, {}, {"text": "hi"})


def _waits(sleeper, want, label_th, label_en):
    got = [float(w) for w in sleeper.waits]
    if got != want:
        raise Fail(f"{label_th}: ควรรอ {want} แต่รอ {got}", f"{label_en}: should wait {want}, waited {got}")


@check("success", th="สำเร็จครั้งแรกคืน body โดยไม่รอ", en="Returns the body at once on success")
def _(sol):
    out, err, server, sleeper = _run(sol, [OK])
    if err or out != {"text": "hi"} or server.calls != 1:
        raise Fail(f"ควรได้ {{'text': 'hi'}} จากการเรียกครั้งเดียว แต่ได้ {out!r} / {err!r}", f"Should return {{'text': 'hi'}} after one call, got {out!r} / {err!r}")
    _waits(sleeper, [], "สำเร็จทันที", "Immediate success")


@check("backoff", th="เจอ 503 ซ้ำๆ รอแบบเพิ่มเป็นสองเท่า 1, 2, 4", en="Repeated 503s wait 1, 2, 4 seconds (doubling)")
def _(sol):
    out, err, server, sleeper = _run(sol, [(503, {}, None)] * 3 + [OK])
    if out != {"text": "hi"}:
        raise Fail(f"หลัง 503 สามครั้งควรสำเร็จในครั้งที่สี่ แต่ได้ {out!r} / {err!r}", f"After three 503s the fourth call should succeed, got {out!r} / {err!r}")
    _waits(sleeper, [1.0, 2.0, 4.0], "503 สามครั้ง", "Three 503s")


@check("no-retry-401", th="401 ไม่ลองใหม่ raise ApiError ทันที", en="401 is not retried: ApiError right away")
def _(sol):
    out, err, server, sleeper = _run(sol, [(401, {}, {"error": "invalid x-api-key"}), OK])
    if err is None or getattr(err, "status", None) != 401 or server.calls != 1:
        raise Fail(f"401 ต้อง raise ApiError(status=401) หลังเรียกครั้งเดียว แต่ได้ {out!r} / {err!r} (เรียก {server.calls} ครั้ง)", f"401 must raise ApiError(status=401) after one call, got {out!r} / {err!r} ({server.calls} calls)")
    _waits(sleeper, [], "401", "401")


@check("give-up", th="ลองใหม่ครบ max_retries แล้วยอมแพ้ด้วย ApiError", en="Gives up with ApiError after max_retries retries")
def _(sol):
    out, err, server, sleeper = _run(sol, [(429, {}, None)] * 3, max_retries=2, base=0.5)
    if err is None or getattr(err, "status", None) != 429 or server.calls != 3:
        raise Fail(f"max_retries=2 ควรเรียก 3 ครั้งแล้ว raise ApiError(429) แต่เรียก {server.calls} ครั้ง ได้ {out!r} / {err!r}", f"max_retries=2 should call 3 times then raise ApiError(429); called {server.calls} times, got {out!r} / {err!r}")
    _waits(sleeper, [0.5, 1.0], "429 ทุกครั้ง base=0.5", "Always 429 with base=0.5")


@check("retry-after", th="ทำตาม header retry-after", en="Honours the retry-after header", hidden=True)
def _(sol):
    out, err, server, sleeper = _run(sol, [(429, {"retry-after": "7"}, None), (529, {}, None), OK])
    _waits(sleeper, [7.0, 2.0], "429 ที่มี retry-after: 7 แล้ว 529", "429 with retry-after: 7, then 529")


@check("header-case", th="ชื่อ header เป็นตัวพิมพ์ใหญ่ก็หาเจอ (Retry-After)", en="Finds the header in any letter case (Retry-After)", hidden=True)
def _(sol):
    out, err, server, sleeper = _run(sol, [(503, {"Retry-After": "0.25"}, None), OK])
    _waits(sleeper, [0.25], "Retry-After: 0.25", "Retry-After: 0.25")


@check("no-final-sleep", th="ไม่รอหลังความพยายามครั้งสุดท้าย", en="No wait after the final attempt", hidden=True)
def _(sol):
    out, err, server, sleeper = _run(sol, [(500, {}, None)] * 2, max_retries=1)
    if server.calls != 2:
        raise Fail(f"max_retries=1 ควรเรียก send 2 ครั้ง แต่เรียก {server.calls} ครั้ง", f"max_retries=1 should call send twice, called {server.calls} times")
    _waits(sleeper, [1.0], "500 สองครั้ง max_retries=1", "Two 500s with max_retries=1")


@check("other-4xx", th="400 และ 404 ก็ไม่ลองใหม่", en="400 and 404 are not retried either", hidden=True)
def _(sol):
    for status in (400, 404):
        out, err, server, sleeper = _run(sol, [(status, {}, None), OK])
        if err is None or getattr(err, "status", None) != status or server.calls != 1:
            raise Fail(f"{status} ต้อง raise ApiError ทันที แต่ได้ {out!r} / {err!r}", f"{status} must raise ApiError at once, got {out!r} / {err!r}")
