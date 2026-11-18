def parse_env(text):
    env = {}
    for n, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:]
        parts = line.split("=")
        if len(parts) < 2 or not parts[0].strip():
            raise ValueError(f"line {n}")
        value = parts[1].strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        env[parts[0].strip()] = value
    return env
