def to_octal(perms):
    """'rwxr-xr--' -> '754'."""
    digits = []
    for i in (0, 3, 6):
        group = perms[i:i + 3]
        # TODO: add 4 for r, 2 for w, 1 for x (a '-' adds nothing)
        value = 0
        digits.append(str(value))
    return "".join(digits)
