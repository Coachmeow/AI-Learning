from itertools import islice


def batches(items, batch_size, drop_last=False):
    if batch_size < 1:
        raise ValueError(batch_size)
    return _it(iter(items), batch_size)


def _it(iterator, batch_size):
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch:
            return
        yield batch
