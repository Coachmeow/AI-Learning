def run_order_report(nb):
    not_run, out_of_order = [], []
    prev = 0
    for i, cell in enumerate(nb["cells"]):
        if cell.get("cell_type") != "code":
            continue
        count = cell.get("execution_count")
        if count is None:
            not_run.append(i)
            continue
        if count <= prev:
            out_of_order.append(i)
        prev = count
    return {"not_run": not_run, "out_of_order": out_of_order}
