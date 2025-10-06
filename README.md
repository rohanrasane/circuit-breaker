# Circuit Breaker Demo

**Authors:** Rohan Rasane
**License:** MIT

---

## Summary

This repository provides a simple Python implementation of the Circuit Breaker pattern, along with a demonstration simulating payment processing during a high-traffic event (Black Friday). The circuit breaker protects downstream services from cascading failures by transitioning between `CLOSED`, `OPEN`, and `HALF_OPEN` states.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/rohanrasane/circuit-breaker.git
cd circuit-breaker
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Project Structure

```
circuit-breaker/
│
├── README.md
├── requirements.txt       # Python dependencies
├── .gitignore
├── main.py                # Optional entry point for testing circuit breaker
├── simulate_black_friday.py # Demo simulating high load payments
├── payments.py            # Payment processing wrapper with circuit breaker
├── circuit_breaker.py     # Circuit breaker implementation
└── tests/
    └── test_circuit_breaker.py # Pytest unit tests
```

---

## Usage

Run the Black Friday simulation:

```bash
python simulate_black_friday.py
```

Run an example manually using the circuit breaker:

```python
from payments import payment_cb, process_payment

payment_cb.call(process_payment, order_id=1)
```

---

## Example Output

```
Starting Black Friday order simulation...
Order 1: Payment processed for order 1 | Circuit State: closed
Order 2: Payment queued for retry for order 2 | Circuit State: open
...
Order 10: Payment queued for retry for order 10 | Circuit State: open
Simulation complete!
```

---

## Testing

Run all unit tests with pytest:

```bash
pytest tests/test_circuit_breaker.py -v
```

---

## References

* JOSS Submission: [https://joss.theoj.org/](https://joss.theoj.org/)
* Circuit Breaker Pattern: [https://martinfowler.com/bliki/CircuitBreaker.html](https://martinfowler.com/bliki/CircuitBreaker.html)
* My Story - From Crisis to Resilience: How a Circuit Breaker Saved Our Platform Post-Thanksgiving: [https://github.com/rohanrasane/devsculptcha/blob/main/docs/shortcircuit.md]