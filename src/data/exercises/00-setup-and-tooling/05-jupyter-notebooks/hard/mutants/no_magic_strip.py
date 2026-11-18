import io
from contextlib import redirect_stdout


def restart_and_run_all(nb):
    ns, results = {}, []
    for i, cell in enumerate(nb["cells"]):
        if cell.get("cell_type") != "code":
            continue
        src = cell["source"]
        src = "".join(src) if isinstance(src, list) else src
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                exec(src, ns)
        except Exception as e:
            results.append({"index": i, "ok": False, "output": buf.getvalue(), "error": type(e).__name__})
            break
        results.append({"index": i, "ok": True, "output": buf.getvalue(), "error": None})
    return results
