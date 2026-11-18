def mask_key(key):
    if len(key) <= 12:
        return "***"
    return key[:7] + "..." + key[4:]
