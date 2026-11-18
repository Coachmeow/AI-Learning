def code_cells(nb):
    return [cell["source"] for cell in nb["cells"] if cell["cell_type"] == "code"]
