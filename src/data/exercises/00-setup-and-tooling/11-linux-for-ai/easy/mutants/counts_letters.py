def to_octal(perms):
    return "".join(str(sum(ch != "-" for ch in perms[i:i + 3])) for i in (0, 3, 6))
