class GradientDescent:
    def __init__(self, lr=0.001):
        self.lr = lr

    def step(self, params, grads):
        # TODO: return a NEW list where each parameter moves
        # against its gradient, scaled by self.lr
        raise NotImplementedError
