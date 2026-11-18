"""Exercise checker shared by the browser (Pyodide) and scripts/check-exercises.py.

tests.py files use two helpers that this module injects:

    @check("id", th="คำอธิบายไทย", en="English description", hidden=False)
    def _(sol):
        ...  # sol is the learner's module namespace (a dict)
        if bad:
            raise Fail(th="ข้อความไทย", en="English message")
"""

import json
import traceback


class Fail(Exception):
    def __init__(self, th, en=None):
        super().__init__(en or th)
        self.th = th
        self.en = en or th


def _short_error(exc):
    return "".join(traceback.format_exception_only(type(exc), exc)).strip()


def run_checks(user_code, tests_code):
    sol = {"__name__": "solution"}
    try:
        exec(compile(user_code, "solution.py", "exec"), sol)
    except Exception as exc:  # syntax errors and top-level crashes
        tb = traceback.format_exc().splitlines()
        lines = [l for l in tb if "solution.py" in l or not l.startswith("  ")][-4:]
        return {"error": "\n".join(lines) or _short_error(exc)}

    checks = []

    def check(cid, th, en, hidden=False):
        def deco(fn):
            checks.append({"id": cid, "title": {"th": th, "en": en}, "hidden": hidden, "fn": fn})
            return fn

        return deco

    env = {"__name__": "tests", "Fail": Fail, "check": check}
    exec(compile(tests_code, "tests.py", "exec"), env)

    results = []
    for c in checks:
        r = {"id": c["id"], "title": c["title"], "hidden": c["hidden"], "ok": False}
        try:
            c["fn"](sol)
            r["ok"] = True
        except Fail as f:
            r["th"], r["en"] = f.th, f.en
        except NotImplementedError:
            r["th"] = "ยังไม่ได้เขียนโค้ดส่วนนี้ (NotImplementedError)"
            r["en"] = "Not implemented yet (NotImplementedError)"
        except Exception as exc:
            msg = _short_error(exc)
            r["th"] = "เกิดข้อผิดพลาดขณะตรวจ: " + msg
            r["en"] = "Error while checking: " + msg
        results.append(r)
    return {"results": results}


def run_checks_json(user_code, tests_code):
    return json.dumps(run_checks(user_code, tests_code), ensure_ascii=False)
