import time

class RateLimiter:
    def __init__(self, calls: int = 1, period: float = 1.0):
        self.calls = calls
        self.period = period
        self.last_reset = time.time()
        self.num_calls = 0

    def __enter__(self):
        current = time.time()
        if current - self.last_reset >= self.period:
            self.num_calls = 0
            self.last_reset = current

        if self.num_calls >= self.calls:
            wait_time = self.period - (current - self.last_reset)
            time.sleep(max(0, wait_time))
            self.num_calls = 0
            self.last_reset = time.time()

        self.num_calls += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass