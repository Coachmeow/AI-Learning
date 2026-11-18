def parse_dockerfile(text):
    out = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.rstrip("\\").split(None, 1)
        out.append((parts[0].upper(), parts[1].strip() if len(parts) > 1 else ""))
    return out
