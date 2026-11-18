from itertools import islice


def batches(items, batch_size, drop_last=False):
    """Yield lists of up to `batch_size` items, lazily. Raise ValueError at once if batch_size < 1."""
    if batch_size < 1:
        raise ValueError(f"batch_size must be at least 1, got {batch_size}")
    return _batch_iter(iter(items), batch_size, drop_last)


def _batch_iter(iterator, batch_size, drop_last):
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch or (drop_last and len(batch) < batch_size):
            return
        yield batch
