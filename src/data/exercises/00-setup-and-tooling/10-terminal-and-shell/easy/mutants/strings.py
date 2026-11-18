def extract_losses(log_text):
    return [line.split()[-1] for line in log_text.splitlines() if "loss:" in line]
