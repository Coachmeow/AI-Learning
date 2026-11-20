def newton_1d(df, d2f, x0, steps):
    """Minimize with Newton's method; return [x0, x1, ..., x_steps]."""
    xs = [x0]
    x = x0
    for _ in range(steps):
        x = x  # TODO: the Newton update, using df(x) and d2f(x)
        xs.append(x)
    return xs
