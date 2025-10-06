import pytest
import time
from circuit_breaker import CircuitBreaker, State

# Flapper simulates downstream failures and success
def flapper(failures_before_success=0, delay=0):
    state = {"count": 0}
    def fn():
        if delay:
            time.sleep(delay)
        if state["count"] < failures_before_success:
            state["count"] += 1
            raise RuntimeError("downstream error")
        return "ok"
    return fn

def test_circuit_trips_and_recovers():
    cb = CircuitBreaker(failure_threshold=0.5, window_seconds=2, timeout_seconds=1,
                        cooldown_seconds=1, half_open_requests=2)
    f = flapper(2)

    # Cause failures → OPEN
    for _ in range(2):
        with pytest.raises(RuntimeError):
            cb.call(f)

    assert cb.state == State.OPEN

    # Wait for cooldown → HALF_OPEN
    time.sleep(1.1)
    cb._maybe_transition()
    assert cb.state == State.HALF_OPEN

    # Allow success in HALF_OPEN
    f_success = flapper(0)
    result = cb.call(f_success)
    assert result == "ok"

    # Make the second successful call (required by half_open_requests=2)
    result = cb.call(f_success)
    assert result == "ok"

    # Circuit should close after successful HALF_OPEN calls
    cb._maybe_transition()
    assert cb.state == State.CLOSED

def test_call_timeout():
    cb = CircuitBreaker(timeout_seconds=0.1, half_open_requests=1)
    f = flapper(delay=0.2)

    with pytest.raises(RuntimeError, match="Timeout"):
        cb.call(f)

def test_decorator_with_fallback():
    cb = CircuitBreaker(half_open_requests=2)
    f = flapper(failures_before_success=10)

    def fallback():
        return "fallback"

    decorated = cb.decorator(fallback=fallback)(f)

    # Trigger failures → fallback
    for _ in range(3):
        result = decorated()
        if result == "fallback":
            break

    assert result == "fallback"

def test_half_open_allows_one_request():
    cb = CircuitBreaker(cooldown_seconds=1, half_open_requests=1)
    f = flapper(failures_before_success=1)

    # Cause initial failure → OPEN
    with pytest.raises(RuntimeError):
        cb.call(f)

    assert cb.state == State.OPEN

    # Wait → HALF_OPEN
    time.sleep(1.1)
    cb._maybe_transition()
    assert cb.state == State.HALF_OPEN

    # Allow one success
    f_success = flapper(0)
    result = cb.call(f_success)
    assert result == "ok"

    # Circuit should close
    cb._maybe_transition()
    assert cb.state == State.CLOSED
