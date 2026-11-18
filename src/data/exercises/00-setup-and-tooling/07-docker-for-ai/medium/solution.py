def parse_dockerfile(text):
    """Return [(INSTRUCTION, argument), ...] for a Dockerfile, joining continued lines."""
    out, pending = [], []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.endswith("\\"):
            pending.append(line[:-1].rstrip())
            continue
        pending.append(line)
        full = " ".join(p for p in pending if p)
        pending = []
        parts = full.split(None, 1)
        out.append((parts[0].upper(), parts[1].strip() if len(parts) > 1 else ""))
    if pending:
        full = " ".join(p for p in pending if p)
        parts = full.split(None, 1)
        out.append((parts[0].upper(), parts[1].strip() if len(parts) > 1 else ""))
    return out
