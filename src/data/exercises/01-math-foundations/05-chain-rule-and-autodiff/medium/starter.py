import math


class Dual:
    """A value and its derivative, for forward-mode autodiff."""

    def __init__(self, val, der=0.0):
        self.val = val
        self.der = der


def dual_sin(d):
    raise NotImplementedError


def derivative(f, x):
    raise NotImplementedError
