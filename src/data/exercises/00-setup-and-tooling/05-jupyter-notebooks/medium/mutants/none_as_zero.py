def run_order_report(nb):
    not_run, out_of_order = [], []
    highest = 0
    for i, cell in enumerate(nb["cells"]):
        if cell.get("cell_type") != "code":
            continue
        count = cell.get("execution_count") or 0
        if count == 0:
            not_run.append(i)
        if count <= highest:
            out_of_order.append(i)
        else:
            highest = count
    return {"not_run": not_run, "out_of_order": out_of_order}
