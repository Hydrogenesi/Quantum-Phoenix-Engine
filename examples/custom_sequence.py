#!/usr/bin/env python3
"""Example of running a custom operator sequence."""

from quantum_phoenix.animation import run_custom


def main():
    # Define a custom sequence
    custom_operators = [
        ("stress_align", "apex_stable"),   # MERGE
        ("stress_align", "apex_stable"),   # MERGE (stay)
        ("dynamo", "plates"),              # REPLICATE
        ("dynamo", "plates"),              # REPLICATE (stay)
        ("collapse", "hollow"),            # DIVIDE
    ]

    print("🔥 Custom Sequence Example")
    print("═" * 50)
    print()

    run_custom(custom_operators, delay=0.5, verbose=True)


if __name__ == "__main__":
    main()
