# payments.py
import random
import time
from circuit_breaker import CircuitBreaker

# Initialize a circuit breaker for payments
payment_cb = CircuitBreaker(
    failure_threshold=0.5,
    window_seconds=5,
    timeout_seconds=2,
    cooldown_seconds=3,
    half_open_requests=2
)

# A mock payment function for testing
def process_payment(order_id):
    # Randomly succeed or fail to simulate downstream issues
    if random.random() < 0.5:
        raise RuntimeError(f"Payment failed for order {order_id}")
    return f"Payment processed for order {order_id}"

# Flapper helper (fail N times before succeeding)
def flapper(failures_before_success=3):
    state = {"count": 0}

    def fn(order_id):
        if state["count"] < failures_before_success:
            state["count"] += 1
            raise RuntimeError(f"Downstream error for order {order_id}")
        return f"Payment processed for order {order_id}"
    
    return fn
