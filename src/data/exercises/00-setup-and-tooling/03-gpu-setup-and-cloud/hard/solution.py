import statistics
import time


def benchmark(fn, repeats=5, warmup=1, sync=None, clock=time.perf_counter):
    """Median seconds per call of fn(), after `warmup` untimed calls."""
    if repeats < 1:
        raise ValueError(f"repeats must be at least 1, got {repeats}")
    wait = sync if sync is not None else (lambda: None)
    for _ in range(warmup):
        fn()
    times = []
    for _ in range(repeats):
        wait()
        t0 = clock()
        fn()
        wait()
        times.append(clock() - t0)
    return float(statistics.median(times))
