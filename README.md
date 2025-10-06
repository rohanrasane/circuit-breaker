# Circuit Breaker Simulation

## Overview
This repository implements a **Circuit Breaker pattern simulation** inspired by real-world platform incidents. It demonstrates how a circuit breaker can protect a backend system from cascading failures when a critical external service becomes slow or unresponsive.

Features:

- Circuit Breaker states: **CLOSED → OPEN → HALF_OPEN → CLOSED**
- Failure threshold with rolling time window
- Configurable timeouts and cooldown periods
- Fallback mechanism for failed calls
- Simulation of high-load scenarios (e.g., multiple orders)
- Thread-safe and modular design for testing and reuse

## Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/rohanrasane/circuit-breaker.git
cd circuit-breaker
python -m venv venv
source venv/bin/activate  # macOS/Linux
# For Windows: venv\Scripts\activate
