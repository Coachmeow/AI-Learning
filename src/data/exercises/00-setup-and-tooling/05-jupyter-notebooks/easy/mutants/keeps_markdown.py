def code_cells(nb):
    out = []
    for cell in nb["cells"]:
        source = cell["source"]
        out.append("".join(source) if isinstance(source, list) else source)
    return out
