import re
from fnmatch import fnmatchcase


def ssh_options(config, alias):
    """Options `ssh <alias>` would use: {lowercase keyword: value}, first value wins."""
    raise NotImplementedError
