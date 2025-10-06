import threading
import time
from enum import Enum

class State(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=0.5, window_seconds=10, timeout_seconds=2,
                 cooldown_seconds=30, half_open_requests=2):
        self.failure_threshold = failure_threshold
        self.window_seconds = window_seconds
        self.timeout_seconds = timeout_seconds
        self.cooldown_seconds = cooldown_seconds
        self.half_open_requests = half_open_requests

        self.state = State.CLOSED
        self.failures = []
        self.successes_in_half_open = 0
        self._lock = threading.Lock()
        self.opened_at = None

    def _maybe_transition(self):
        now = time.time()
        if self.state == State.OPEN:
            if now - self.opened_at >= self.cooldown_seconds:
                self.state = State.HALF_OPEN
                self.successes_in_half_open = 0
        elif self.state == State.HALF_OPEN:
            if self.successes_in_half_open >= self.half_open_requests:
                self.state = State.CLOSED
                self.failures = []

    def call(self, func, *args, **kwargs):
        with self._lock:
            self._maybe_transition()

            if self.state == State.OPEN:
                raise RuntimeError("Circuit is open")

            try:
                start = time.time()
                result = func(*args, **kwargs)
                duration = time.time() - start
                if duration > self.timeout_seconds:
                    raise RuntimeError("Timeout")
            except Exception as e:
                self.failures.append(time.time())
                if self.state == State.HALF_OPEN:
                    self.state = State.OPEN
                    self.opened_at = time.time()
                elif self.state == State.CLOSED:
                    self._evaluate_failures()
                raise
            else:
                if self.state == State.HALF_OPEN:
                    self.successes_in_half_open += 1
                return result

    def _evaluate_failures(self):
        now = time.time()
        window_start = now - self.window_seconds
        recent_failures = [f for f in self.failures if f >= window_start]
        total = max(len(recent_failures) + 1, 1)
        if len(recent_failures) / total >= self.failure_threshold:
            self.state = State.OPEN
            self.opened_at = now

    def decorator(self, fallback=None):
        def wrapper(func):
            def inner(*args, **kwargs):
                try:
                    return self.call(func, *args, **kwargs)
                except RuntimeError:
                    if fallback:
                        return fallback(*args, **kwargs)
                    raise
            return inner
        return wrapper
