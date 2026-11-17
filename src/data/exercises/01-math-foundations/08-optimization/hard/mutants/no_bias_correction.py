# Wrong: skips bias correction, so early steps are about 3.16x too large.
class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.lr, self.beta1, self.beta2, self.epsilon = lr, beta1, beta2, epsilon
        self.m = self.v = None

    def step(self, params, grads):
        if self.m is None:
            self.m = [0.0] * len(params)
            self.v = [0.0] * len(params)
        self.m = [self.beta1 * m + (1 - self.beta1) * g for m, g in zip(self.m, grads)]
        self.v = [self.beta2 * v + (1 - self.beta2) * g ** 2 for v, g in zip(self.v, grads)]
        return [p - self.lr * m / (v ** 0.5 + self.epsilon) for p, m, v in zip(params, self.m, self.v)]
