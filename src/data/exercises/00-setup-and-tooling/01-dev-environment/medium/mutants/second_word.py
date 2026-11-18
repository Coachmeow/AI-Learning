def parse_version(output):
    parts = output.split()
    word = parts[1] if len(parts) > 1 else parts[0]
    return tuple(int(p) for p in word.split("."))
