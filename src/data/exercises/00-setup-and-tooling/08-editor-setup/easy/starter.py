def long_lines(text, limit=88):
    """(line_number, length) for every line longer than `limit`; numbers start at 1."""
    result = []
    for number, line in enumerate(text.splitlines(), start=1):
        # TODO: record (number, len(line)) when the line is longer than `limit`
        pass
    return result
