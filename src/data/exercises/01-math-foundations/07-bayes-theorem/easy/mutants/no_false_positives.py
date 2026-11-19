def bayes(prior, likelihood, false_positive_rate):
    """P(condition | positive result)."""
    evidence = likelihood * prior
    return likelihood * prior / evidence
