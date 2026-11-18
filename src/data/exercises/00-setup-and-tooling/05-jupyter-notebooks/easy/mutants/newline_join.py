def code_cells(nb):
    out = []
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        source = cell["source"]
        out.append("\n".join(source) if isinstance(source, list) else source)
    return out
