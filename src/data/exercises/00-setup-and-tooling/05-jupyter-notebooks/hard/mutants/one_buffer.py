import io
from contextlib import redirect_stdout


def _python_only(source):
    lines = ("".join(source) if isinstance(source, list) else source).split("\n")
    if lines and lines[0].lstrip().startswith("%%"):
        lines = lines[1:]
    return "\n".join(l for l in lines if l.lstrip()[:1] not in ("%", "!"))


def restart_and_run_all(nb):
    ns, results = {}, []
    buf = io.StringIO()
    for i, cell in enumerate(nb["cells"]):
        if cell.get("cell_type") != "code":
            continue
        try:
            with redirect_stdout(buf):
                exec(_python_only(cell["source"]), ns)
        except Exception as e:
            results.append({"index": i, "ok": False, "output": buf.getvalue(), "error": type(e).__name__})
            break
        results.append({"index": i, "ok": True, "output": buf.getvalue(), "error": None})
    return results
