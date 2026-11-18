def code_cells(nb):
    """Return the source of every code cell in notebook `nb`, as strings, in order."""
    out = []
    for cell in nb["cells"]:
        # TODO: skip cells that are not code, and join a list source into one string
        out.append(cell["source"])
    return out
