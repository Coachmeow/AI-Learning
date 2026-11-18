import io
from contextlib import redirect_stdout


def _python_only(source):
    lines = ("".join(source) if isinstance(source, list) else source).split("\n")
    if lines and lines[0].lstrip().startswith("%%"):
        lines = lines[1:]
    return "\n".join(line for line in lines if line.lstrip()[:1] not in ("%", "!"))


def restart_and_run_all(nb):
    """Run nb's code cells top to bottom in a fresh namespace."""
    ns = {"__name__": "__main__"}
    results = []
    for i, cell in enumerate(nb["cells"]):
        if cell.get("cell_type") != "code":
            continue
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                exec(_python_only(cell["source"]), ns)
        except Exception as e:  # noqa: BLE001
            results.append({"index": i, "ok": False, "output": buf.getvalue(), "error": type(e).__name__})
            break
        results.append({"index": i, "ok": True, "output": buf.getvalue(), "error": None})
    return results
