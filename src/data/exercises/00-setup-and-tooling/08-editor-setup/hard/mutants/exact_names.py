import re


def ssh_options(config, alias):
    options, applies = {}, True
    for raw in config.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = re.split(r"\s*=\s*|\s+", line, maxsplit=1)
        key, value = parts[0].lower(), (parts[1].strip() if len(parts) > 1 else "")
        if key == "host":
            applies = alias in value.split()
            continue
        if applies:
            options.setdefault(key, value)
    options.setdefault("hostname", alias)
    return options
