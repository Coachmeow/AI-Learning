def parse_env(text):
    env = {}
    for n, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        name, eq, value = line.partition("=")
        name, value = name.strip(), value.strip()
        if not eq or not name:
            raise ValueError(f"line {n}")
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        env[name] = value
    return env
