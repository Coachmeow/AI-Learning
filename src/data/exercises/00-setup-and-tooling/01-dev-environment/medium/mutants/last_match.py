import re


def parse_version(output):
    found = re.findall(r"\d+(?:\.\d+)+", output)
    if not found:
        raise ValueError(output)
    return tuple(int(p) for p in found[-1].split("."))
