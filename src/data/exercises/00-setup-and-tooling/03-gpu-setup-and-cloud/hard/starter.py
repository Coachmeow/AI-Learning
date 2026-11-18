import statistics
import time


def benchmark(fn, repeats=5, warmup=1, sync=None, clock=time.perf_counter):
    """Median seconds per call of fn(), after `warmup` untimed calls.

    Each timed call runs: sync() -> t0 = clock() -> fn() -> sync() -> t1 = clock()
    (sync is skipped when it is None).
    """
    raise NotImplementedError
