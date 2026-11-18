import re
import shlex

_OP = re.compile(r"(&|1|2)?(>>|>)(&[12])?(.*)")


def resolve_redirects(command):
    """{"argv": [...], "stdout": (target, mode), "stderr": (target, mode)}, applying redirects left to right."""
    words = shlex.split(command)
    state = {1: ("terminal", "w"), 2: ("terminal", "w")}
    argv = []
    i = 0
    while i < len(words):
        m = _OP.fullmatch(words[i])
        if not m:
            argv.append(words[i])
            i += 1
            continue
        fd, kind, dup, rest = m.groups()
        if dup:
            src, dst = int(dup[1]), int(fd or 1)
            state[dst] = state[src]
            i += 1
            continue
        target = rest
        if not target:
            if i + 1 >= len(words):
                raise ValueError(f"missing file name after {words[i]!r}")
            target = words[i + 1]
            i += 1
        mode = "a" if kind == ">>" else "w"
        fds = (1, 2) if fd == "&" else (int(fd or 1),)
        for f in fds:
            state[f] = (target, mode)
        i += 1
    return {"argv": argv, "stdout": state[1], "stderr": state[2]}
