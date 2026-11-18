import time


class Timer:
    def __init__(self, name, times, clock=time.perf_counter):
        self.name, self.times, self.clock = name, times, clock

    def __enter__(self):
        self.start = self.clock()
        return self

    def __exit__(self, *exc):
        self.elapsed = self.clock() - self.start
        self.times[self.name] = [self.elapsed]
