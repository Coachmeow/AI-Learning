import shlex


def _count(args, default=10):
    if "-n" in args:
        return int(args[args.index("-n") + 1])
    return default


def _stage(lines, args):
    name, opts = args[0], args[1:]
    if name == "grep":
        invert = "-v" in opts
        pattern = [a for a in opts if a != "-v"][0]
        return [l for l in lines if (pattern in l) != invert]
    if name == "wc" and opts == ["-l"]:
        return [str(len(lines))]
    if name == "head":
        return lines[: _count(opts)]
    if name == "tail":
        n = _count(opts)
        return lines[-n:] if n else []
    if name == "sort":
        key = (lambda l: float(l.split()[0])) if "-n" in opts else None
        return sorted(lines, key=key, reverse="-r" in opts)
    if name == "awk" and len(opts) == 1:
        prog = opts[0].strip()
        if prog.startswith("{print $") and prog.endswith("}"):
            field = prog[len("{print $"):-1].strip()
            out = []
            for l in lines:
                words = l.split()
                if field == "NF":
                    out.append(words[0] if words else "")
                else:
                    k = int(field)
                    out.append(words[k - 1] if 0 < k <= len(words) else "")
            return out
    raise ValueError(f"unsupported command: {' '.join(args)}")


def run_pipeline(text, command):
    """Run a small `a | b | c` shell pipeline over `text`; return the output as a string."""
    lines = text.splitlines()
    for stage in command.split("|"):
        args = shlex.split(stage)
        if not args:
            raise ValueError("empty stage")
        lines = _stage(lines, args)
    return "\n".join(lines) + "\n" if lines else ""
