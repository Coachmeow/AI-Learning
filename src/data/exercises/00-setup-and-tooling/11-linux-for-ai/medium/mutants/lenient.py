import re

_WHO = {"u": 0, "g": 1, "o": 2}


def apply_chmod(perms, spec):
    """apply_chmod('rw-r--r--', 'u+x') -> 'rwxr--r--'. Supports octal and symbolic modes."""
    groups = [{ch for ch in perms[i:i + 3] if ch != "-"} for i in (0, 3, 6)]
    if re.fullmatch(r"[0-7]{3}", spec):
        groups = [{ch for ch, w in zip("rwx", (4, 2, 1)) if int(d) & w} for d in spec]
    else:
        for clause in spec.split(","):
            m = re.fullmatch(r"([ugoa]*)([+=-])([rwx]*)", clause)
            if not m:
                continue
            who, op, bits = m.groups()
            who = "ugo" if who in ("", "a") or "a" in who else who
            for w in set(who):
                g = groups[_WHO[w]]
                if op == "+":
                    g |= set(bits)
                elif op == "-":
                    g -= set(bits)
                else:
                    groups[_WHO[w]] = set(bits)
    return "".join("".join(ch if ch in g else "-" for ch in "rwx") for g in groups)
