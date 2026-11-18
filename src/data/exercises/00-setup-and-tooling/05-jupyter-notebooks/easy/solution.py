def code_cells(nb):
    """Return the source of every code cell in notebook `nb`, as strings, in order."""
    out = []
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        source = cell["source"]
        out.append("".join(source) if isinstance(source, list) else source)
    return out
