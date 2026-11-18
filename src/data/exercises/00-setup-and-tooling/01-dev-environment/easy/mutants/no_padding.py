def to_numbers(version):
    return [int(part) for part in version.split(".")]


def is_new_enough(version, minimum):
    return to_numbers(version) >= to_numbers(minimum)
