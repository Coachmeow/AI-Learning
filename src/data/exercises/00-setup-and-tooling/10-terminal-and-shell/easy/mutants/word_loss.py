def extract_losses(log_text):
    return [float(line.split()[-1]) for line in log_text.splitlines() if "loss" in line and line.split()[-1][0].isdigit()]
