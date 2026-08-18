#!/usr/bin/env python3
"""Basic usage example of the Quantum Phoenix Engine."""

from quantum_phoenix import Phoenix


def main():
    # Initialize the engine
    engine = Phoenix()
    print(f"Initial state: {engine}")
    print()

    # Step 1: Stay in MERGE
    print("Step 1: Applying (stress_align, apex_stable)")
    state = engine.step("stress_align", "apex_stable")
    print(f"State after step: {engine}")
    print(f"Is terminal? {engine.is_terminal()}")
    print()

    # Step 2: Transition to REPLICATE
    print("Step 2: Applying (dynamo, plates)")
    state = engine.step("dynamo", "plates")
    print(f"State after step: {engine}")
    print(f"Is terminal? {engine.is_terminal()}")
    print()

    # Show history
    print(f"History: {[s.name for s in engine.history]}")


if __name__ == "__main__":
    main()
