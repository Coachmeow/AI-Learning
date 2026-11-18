import re
from fnmatch import fnmatchcase


def _block_applies(patterns, alias):
    hit = False
    for p in patterns:
        if p.startswith("!"):
            if fnmatchcase(alias, p[1:]):
                return False
        elif fnmatchcase(alias, p):
            hit = True
    return hit


def ssh_options(config, alias):
    """Options `ssh <alias>` would use: {lowercase keyword: value}, first value wins."""
    options = {}
    applies = True
    for raw in config.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = re.split(r"\s*=\s*|\s+", line, maxsplit=1)
        key = parts[0].lower()
        value = parts[1].strip() if len(parts) > 1 else ""
        if key == "host":
            applies = _block_applies(value.split(), alias)
            continue
        if applies:
            options.setdefault(key, value)
    options.setdefault("hostname", alias)
    return options
