import io
from contextlib import redirect_stdout


def _python_only(source):
    lines = ("".join(source) if isinstance(source, list) else source).split("\n")
    if lines and lines[0].lstrip().startswith("%%"):
        lines = lines[1:]
    return "\n".join(l for l in lines if l.lstrip()[:1] not in ("%", "!"))


def restart_and_run_all(nb):
    ns, results = {}, []
    for i, cell in enumerate(nb["cells"]):
        if cell.get("cell_type") != "code":
            continue
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                exec(_python_only(cell["source"]), ns)
            results.append({"index": i, "ok": True, "output": buf.getvalue(), "error": None})
        except Exception as e:
            results.append({"index": i, "ok": False, "output": buf.getvalue(), "error": type(e).__name__})
    return results
