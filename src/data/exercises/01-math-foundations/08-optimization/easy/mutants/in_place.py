# Wrong: edits the caller's list in place.
class GradientDescent:
    def __init__(self, lr=0.001):
        self.lr = lr

    def step(self, params, grads):
        for i, g in enumerate(grads):
            params[i] -= self.lr * g
        return params
