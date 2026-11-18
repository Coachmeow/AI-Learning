# Wrong: the velocity lives on the class, so every optimizer shares it.
class SGDMomentum:
    velocity = []

    def __init__(self, lr=0.001, momentum=0.9):
        self.lr = lr
        self.momentum = momentum

    def step(self, params, grads):
        if not SGDMomentum.velocity:
            SGDMomentum.velocity.extend([0.0] * len(params))
        for i, g in enumerate(grads):
            SGDMomentum.velocity[i] = self.momentum * SGDMomentum.velocity[i] + g
        return [p - self.lr * v for p, v in zip(params, SGDMomentum.velocity)]
