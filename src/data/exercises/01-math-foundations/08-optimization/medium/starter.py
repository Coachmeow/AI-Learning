class SGDMomentum:
    def __init__(self, lr=0.001, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.velocity = None

    def step(self, params, grads):
        """Update the velocity, then move each parameter by lr * velocity.

        velocity = momentum * velocity + grad   (velocity starts at zeros)
        param    = param - lr * velocity
        """
        raise NotImplementedError
