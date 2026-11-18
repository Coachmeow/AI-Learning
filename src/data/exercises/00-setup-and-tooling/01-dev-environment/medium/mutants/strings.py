import re


def parse_version(output):
    m = re.search(r"\d+(?:\.\d+)+", output)
    if m is None:
        raise ValueError(output)
    return tuple(m.group(0).split("."))
