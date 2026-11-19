import math


class Dual:
    """A value and its derivative, for forward-mode autodiff."""

    def __init__(self, val, der=0.0):
        self.val = val
        self.der = der

    @staticmethod
    def _lift(o):
        return o if isinstance(o, Dual) else Dual(o, 0.0)

    def __add__(self, other):
        o = Dual._lift(other)
        return Dual(self.val + o.val, self.der + o.der)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        o = Dual._lift(other)
        return Dual(self.val - o.val, self.der - o.der)

    def __rsub__(self, other):
        return Dual._lift(other) - self

    def __mul__(self, other):
        o = Dual._lift(other)
        return Dual(self.val * o.val, self.der * o.der)

    def __rmul__(self, other):
        return self * other


def dual_sin(d):
    return Dual(math.sin(d.val), math.cos(d.val) * d.der)


def derivative(f, x):
    out = f(Dual(x, 1.0))
    return out.der if isinstance(out, Dual) else 0.0
