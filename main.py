# main.py
from simulate_black_friday import simulate_orders

def run_black_friday_simulation():
    print("Starting Black Friday simulation...")
    simulate_orders(30)
    print("Simulation complete!")

if __name__ == "__main__":
    run_black_friday_simulation()
