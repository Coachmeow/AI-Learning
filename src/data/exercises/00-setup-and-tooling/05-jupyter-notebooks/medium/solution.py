def run_order_report(nb):
    """Return {"not_run": [...], "out_of_order": [...]} as indexes into nb["cells"]."""
    not_run, out_of_order = [], []
    highest = 0
    for i, cell in enumerate(nb["cells"]):
        if cell.get("cell_type") != "code":
            continue
        count = cell.get("execution_count")
        if count is None:
            not_run.append(i)
        elif count <= highest:
            out_of_order.append(i)
        else:
            highest = count
    return {"not_run": not_run, "out_of_order": out_of_order}
