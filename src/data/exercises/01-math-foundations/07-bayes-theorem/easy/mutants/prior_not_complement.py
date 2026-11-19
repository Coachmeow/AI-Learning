def bayes(prior, likelihood, false_positive_rate):
    """P(condition | positive result)."""
    evidence = likelihood * prior + false_positive_rate * prior
    return likelihood * prior / evidence
