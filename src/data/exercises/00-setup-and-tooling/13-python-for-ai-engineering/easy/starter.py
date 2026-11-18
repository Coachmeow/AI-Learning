def make_grid(rows, cols, value=0):
    """A rows x cols list of lists filled with `value`; every row is a separate list."""
    # TODO: build a NEW row for each of the `rows` rows (don't multiply the outer list)
    return [[value] * cols] * rows
