import math


def metropolis(log_target, x0, steps, uniforms):
    """(chain, acceptance_rate) of a random-walk Metropolis chain driven by the given steps and uniforms."""
    if len(steps) != len(uniforms):
        raise ValueError("steps and uniforms must have the same length")
    x = x0
    lp = log_target(x)
    if not math.isfinite(lp):
        raise ValueError("x0 must be inside the support")
    chain = []
    accepted = 0
    for step, u in zip(steps, uniforms):
        proposal = x + step
        lp_new = log_target(proposal)
        delta = lp_new - lp
        if u < math.exp(min(0.0, delta)):
            x, lp = proposal, lp_new
            accepted += 1
        chain.append(x)
    return chain, (accepted / len(steps) if steps else 0.0)
