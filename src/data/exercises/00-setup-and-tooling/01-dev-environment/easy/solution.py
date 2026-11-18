def to_numbers(version):
    return [int(part) for part in version.split(".")]


def is_new_enough(version, minimum):
    found = to_numbers(version)
    need = to_numbers(minimum)
    n = max(len(found), len(need))
    found = found + [0] * (n - len(found))
    need = need + [0] * (n - len(need))
    return found >= need
