import re


def parse_version(output):
    """Return the first version number in `output` as a tuple of ints."""
    m = re.search(r"\d+(?:\.\d+)+", output)
    if m is None:
        raise ValueError(f"no version number in {output!r}")
    return tuple(int(p) for p in m.group(0).split("."))
