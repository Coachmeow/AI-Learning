def parse_env(text):
    """Parse the contents of a .env file into a dict of name -> value."""
    env = {}
    for n, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        name, eq, value = line.partition("=")
        name, value = name.strip(), value.strip()
        if not eq or not name:
            raise ValueError(f"line {n}: expected NAME=value, got {raw!r}")
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        env[name] = value
    return env
