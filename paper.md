---
title: "Circuit Breaker Demo: A Lightweight Pattern for Service Resilience in High-Traffic Environments"
authors:
  - name: Rohan Rasane
    affiliation: ServiceNow, San Jose, CA
date: 2025-10-08
tags:
  - Python
  - Distributed Systems
  - Fault Tolerance
  - Resilience Patterns
license: MIT
---

# Summary

The **Circuit Breaker Demo** is a compact Python implementation of the *Circuit Breaker* design pattern. The pattern helps prevent cascading failures in distributed systems by short-circuiting calls to unhealthy downstream services for a configurable cooldown period. This repository provides an implementation, unit tests, and a small simulation that demonstrates behavior under high load (a "Black Friday" payment processing scenario).

# Statement of need

Modern microservice architectures depend on many networked services; failure or slowness in one service can quickly affect overall system availability. Developers, educators, and researchers need simple, well-documented implementations to experiment with resilience strategies before adopting them in production. This demo fills that need by offering:

- A minimal, clear `CircuitBreaker` class that is easy to read and extend.
- A simulation that shows how the breaker protects a payment service during traffic spikes.
- Unit tests and usage examples that make the code easy to run and validate.

# Implementation

The library provides a `CircuitBreaker` abstraction that can be used either as a decorator or by calling a `.call()` helper. Key features:

- **States:** `CLOSED`, `OPEN`, `HALF_OPEN`.
- **Configurable thresholds:** number of failures before opening, recovery timeout, and a success threshold while half-open.
- **Simple exception handling:** treat any exception raised by the wrapped function as a failure (configurable in your code).
- **Hooks:** easy places to plug in logging and metrics collection.

Example usage:

```python
from circuit_breaker import CircuitBreaker, CircuitBreakerError

breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10)

@breaker
def call_external_service():
    # Replace with actual call to external dependency
    raise Exception("Service unavailable")

try:
    call_external_service()
except CircuitBreakerError:
    print("Circuit is open; skipping call")
```

# Example scenario

The included `simulate_black_friday.py` demonstrates a payment-processing service receiving many simulated orders. As failures occur on the downstream payment API, the circuit breaker opens and subsequent calls are short-circuited, preventing further load on the failing service and allowing the system to recover.

# Testing

Unit tests are provided in `tests/test_circuit_breaker.py` and can be run with:

```bash
pytest -q
```

The tests cover state transitions and the basic decorator / call behavior.

# Acknowledgements

Thanks to the designers and authors who popularized resilience patterns in distributed systems, and to the open-source tooling that simplifies testing and packaging Python projects.

# References

- Michael T. Nygard. *Release It!: Design and Deploy Production-Ready Software*. Pragmatic Bookshelf, 2007.
- Martin Fowler. "Circuit Breaker" pattern. https://martinfowler.com/bliki/CircuitBreaker.html
- R. Rasane. "From Crisis to Resilience: How a Circuit Breaker Saved Our Platform Post-Thanksgiving." https://github.com/rohanrasane/devsculptcha/blob/main/docs/shortcircuit.md
