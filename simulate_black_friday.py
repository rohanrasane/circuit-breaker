# simulate_black_friday.py
import time
import random
from payments import payment_cb, process_payment  # <- updated import

NUM_ORDERS = 30
FAILURE_PROBABILITY = 0.4  # 40% chance a payment fails

def simulate_order(order_id):
    """Simulate a single order payment."""
    def payment():
        # Randomly fail some payments
        if random.random() < FAILURE_PROBABILITY:
            raise RuntimeError("Payment failed due to downstream error")
        return f"Payment processed for order {order_id}"

    # Attempt payment through the circuit breaker
    try:
        result = payment_cb.call(payment)
        print(f"Order {order_id}: {result} | Circuit State: {payment_cb.state.value}")
        return True
    except RuntimeError:
        # Circuit is open or payment failed
        print(f"Order {order_id}: Payment queued for retry | Circuit State: {payment_cb.state.value}")
        return False

def main():
    print("Starting Black Friday order simulation...\n")
    successes = 0
    failures = 0

    for order_id in range(1, NUM_ORDERS + 1):
        if simulate_order(order_id):
            successes += 1
        else:
            failures += 1
        # Short delay to see HALF_OPEN transitions in action
        time.sleep(0.2)
    
    print("\nSimulation complete!")
    print(f"Total orders: {NUM_ORDERS}")
    print(f"Successful payments: {successes}")
    print(f"Failed / queued payments: {failures}")
    print(f"Final circuit state: {payment_cb.state.value}")

if __name__ == "__main__":
    main()
