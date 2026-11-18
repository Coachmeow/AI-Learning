def batches(items, batch_size, drop_last=False):
    if batch_size < 1:
        raise ValueError(batch_size)
    data = list(items)
    out = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]
    if drop_last and out and len(out[-1]) < batch_size:
        out.pop()
    return iter(out)
