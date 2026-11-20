import math


def temperature_softmax(logits, temperature):
    """Softmax of the logits divided by the temperature."""
    scaled = list(logits)  # TODO: divide every logit by the temperature
    m = max(scaled)
    exps = [math.exp(z - m) for z in scaled]
    total = sum(exps)
    return [e / total for e in exps]
