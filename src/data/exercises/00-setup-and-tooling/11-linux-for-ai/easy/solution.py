def to_octal(perms):
    """'rwxr-xr--' -> '754'."""
    digits = []
    for i in (0, 3, 6):
        group = perms[i:i + 3]
        value = sum(w for ch, w in zip(group, (4, 2, 1)) if ch != "-")
        digits.append(str(value))
    return "".join(digits)
