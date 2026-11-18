def run_order_report(nb):
    not_run, out_of_order = [], []
    highest = 0
    code = [c for c in nb["cells"] if c.get("cell_type") == "code"]
    for i, cell in enumerate(code):
        count = cell.get("execution_count")
        if count is None:
            not_run.append(i)
        elif count <= highest:
            out_of_order.append(i)
        else:
            highest = count
    return {"not_run": not_run, "out_of_order": out_of_order}
