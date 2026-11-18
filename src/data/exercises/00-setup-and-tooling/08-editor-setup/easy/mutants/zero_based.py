def long_lines(text, limit=88):
    return [(n, len(l)) for n, l in enumerate(text.splitlines()) if len(l) > limit]
