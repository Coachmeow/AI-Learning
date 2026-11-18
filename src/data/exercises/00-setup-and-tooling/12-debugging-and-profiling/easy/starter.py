import time


class Timer:
    def __init__(self, name, times, clock=time.perf_counter):
        self.name, self.times, self.clock = name, times, clock

    def __enter__(self):
        self.start = self.clock()
        return self

    def __exit__(self, *exc):
        # TODO: store the elapsed time in self.elapsed and append it to self.times[self.name]
        pass
