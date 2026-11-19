def numerical_derivative(f, x, h=1e-5):
    """Central-difference estimate of f'(x)."""
    return (f(x + h) - f(x)) / h
