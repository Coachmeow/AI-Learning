def parse_env(text):
    env = {}
    for n, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:]
        name, eq, value = line.partition("=")
        if not eq or not name.strip():
            raise ValueError(f"line {n}")
        env[name.strip()] = value.strip()
    return env
