def extract_losses(log_text):
    """Like: grep "loss:" | awk '{print $NF}' -> list of floats."""
    losses = []
    for line in log_text.splitlines():
        if "loss:" in line:
            losses.append(float(line.split()[-1]))
    return losses
