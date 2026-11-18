import re


def parse_version(output):
    """Return the first version number in `output` as a tuple of ints.

    parse_version("Python 3.12.4")                          -> (3, 12, 4)
    parse_version("v22.11.0")                               -> (22, 11, 0)
    parse_version("rustc 1.82.0 (f6e511eec 2024-10-15)")    -> (1, 82, 0)
    Raises ValueError when there is no version number.
    """
    raise NotImplementedError
