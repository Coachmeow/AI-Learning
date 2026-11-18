def batches(items, batch_size, drop_last=False):
    if batch_size < 1:
        raise ValueError(batch_size)
    return (list(items[i:i + batch_size]) for i in range(0, len(items), batch_size)
            if not (drop_last and len(items[i:i + batch_size]) < batch_size))
