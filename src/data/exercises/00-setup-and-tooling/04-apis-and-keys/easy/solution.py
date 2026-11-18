def mask_key(key):
    """Show only the start and end of an API key, e.g. 'sk-ant-...Rt4W'."""
    if len(key) <= 12:
        return "***"
    return key[:7] + "..." + key[-4:]
