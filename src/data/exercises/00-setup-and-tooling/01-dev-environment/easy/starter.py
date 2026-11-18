def to_numbers(version):
    return [int(part) for part in version.split(".")]


def is_new_enough(version, minimum):
    found = to_numbers(version)
    need = to_numbers(minimum)
    # TODO: pad the shorter list with zeros so both have the same length,
    # then compare them
    raise NotImplementedError
