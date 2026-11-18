import io
from contextlib import redirect_stdout


def restart_and_run_all(nb):
    """Run nb's code cells top to bottom in a fresh namespace.

    Returns [{"index": i, "ok": bool, "output": str, "error": None or "ExceptionName"}, ...]
    and stops after the first cell that raises.
    """
    raise NotImplementedError
