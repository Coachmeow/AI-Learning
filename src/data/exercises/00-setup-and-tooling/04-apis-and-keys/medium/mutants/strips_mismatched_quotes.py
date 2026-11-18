def parse_env(text):
    env = {}
    for n, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:]
        name, eq, value = line.partition("=")
        name, value = name.strip(), value.strip()
        if not eq or not name:
            raise ValueError(f"line {n}")
        env[name] = value.strip("\"'")
    return env
