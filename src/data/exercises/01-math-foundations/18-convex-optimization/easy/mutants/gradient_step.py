def newton_1d(df, d2f, x0, steps):
    """Minimize with Newton's method; return [x0, x1, ..., x_steps]."""
    xs = [x0]
    x = x0
    for _ in range(steps):
        x = x - df(x)
        xs.append(x)
    return xs
