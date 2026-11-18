def make_grid(rows, cols, value=0):
    """A rows x cols list of lists filled with `value`; every row is a separate list."""
    return [[value] * cols for _ in range(rows)]
