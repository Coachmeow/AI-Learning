def update_after_tests(prior, results, sensitivity, specificity):
    """P(sick) after the test results (True = positive), updating one result at a time."""
    for name, value in (("prior", prior), ("sensitivity", sensitivity), ("specificity", specificity)):
        if not 0 <= value <= 1:
            raise ValueError(f"{name} must be between 0 and 1")
    p = prior
    for positive in results:
        if positive:
            if_sick, if_healthy = sensitivity, 1 - specificity
        else:
            if_sick, if_healthy = sensitivity, 1 - specificity
        p = if_sick * p / (if_sick * p + if_healthy * (1 - p))
    return p
