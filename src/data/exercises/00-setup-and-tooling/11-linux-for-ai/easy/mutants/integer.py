def to_octal(perms):
    return int("".join(str(sum(w for ch, w in zip(perms[i:i + 3], (4, 2, 1)) if ch != "-")) for i in (0, 3, 6)))
