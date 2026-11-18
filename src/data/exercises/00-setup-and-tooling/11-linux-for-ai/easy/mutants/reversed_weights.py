def to_octal(perms):
    return "".join(str(sum(w for ch, w in zip(perms[i:i + 3], (1, 2, 4)) if ch != "-")) for i in (0, 3, 6))
