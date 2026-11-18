def extract_losses(log_text):
    """Like: grep "loss:" | awk '{print $NF}' -> list of floats."""
    losses = []
    for line in log_text.splitlines():
        # TODO: for lines containing "loss:", append the last word as a float
        pass
    return losses
