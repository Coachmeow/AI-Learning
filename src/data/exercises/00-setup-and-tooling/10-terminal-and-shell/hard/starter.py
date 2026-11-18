import re
import shlex


def resolve_redirects(command):
    """{"argv": [...], "stdout": (target, mode), "stderr": (target, mode)}, applying redirects left to right."""
    raise NotImplementedError
