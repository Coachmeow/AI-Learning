def update_after_tests(prior, results, sensitivity, specificity):
    """P(sick) after the test results (True = positive), updating one result at a time."""
    p = prior
    for positive in results:
        if positive:
            if_sick, if_healthy = sensitivity, 1 - specificity
        else:
            if_sick, if_healthy = 1 - sensitivity, specificity
        p = if_sick * p / (if_sick * p + if_healthy * (1 - p))
    return p
