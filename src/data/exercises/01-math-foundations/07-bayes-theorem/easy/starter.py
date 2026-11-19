def bayes(prior, likelihood, false_positive_rate):
    """P(condition | positive result)."""
    evidence = 1.0  # TODO: the total probability of a positive result
    return likelihood * prior / evidence
