import statistics
import time


def benchmark(fn, repeats=5, warmup=1, sync=None, clock=time.perf_counter):
    if repeats < 1:
        raise ValueError(repeats)
    for _ in range(warmup):
        fn()
    times = []
    for _ in range(repeats):
        if sync:
            sync()
        t0 = clock()
        fn()
        t1 = clock()
        if sync:
            sync()
        times.append(t1 - t0)
    return float(statistics.median(times))
