def extract_losses(log_text):
    out = []
    for line in log_text.splitlines():
        if "loss:" in line:
            for w in line.split():
                try:
                    out.append(float(w))
                    break
                except ValueError:
                    pass
    return out
