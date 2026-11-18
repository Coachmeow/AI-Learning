class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        # TODO: set up the state you need (m, v and the step count t)

    def step(self, params, grads):
        """Return the updated params as a new list.

        Keep m (running mean of gradients) and v (running mean of squared
        gradients) for every parameter, count steps in t, and use bias
        correction before the update.
        """
        raise NotImplementedError
