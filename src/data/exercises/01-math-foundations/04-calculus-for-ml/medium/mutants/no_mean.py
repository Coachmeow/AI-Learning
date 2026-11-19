def fit_line(xs, ys, lr=0.01, epochs=1000):
    """Fit y = w*x + b by full-batch gradient descent on the MSE, starting from w = b = 0."""
    w = b = 0.0
    n = len(xs)
    for _ in range(epochs):
        dw = db = 0.0
        for x, y in zip(xs, ys):
            error = w * x + b - y
            dw += 2 * error * x
            db += 2 * error
        w -= lr * dw
        b -= lr * db
    return w, b
