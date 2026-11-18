def mask_key(key):
    """Show only the start and end of an API key, e.g. 'sk-ant-...Rt4W'."""
    if len(key) <= 12:
        return "***"
    # TODO: return the first 7 characters, then "...", then the last 4
    raise NotImplementedError
