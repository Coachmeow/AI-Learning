import re


def parse_version(output):
    m = re.search(r"\d+(?:\.\d+)+", output)
    if m is None:
        return None
    return tuple(int(p) for p in m.group(0).split("."))
