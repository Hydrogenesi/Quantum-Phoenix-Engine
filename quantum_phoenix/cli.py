"""Command-line interface for the Quantum Phoenix Engine."""

import argparse
import sys
from .engine import Phoenix
from .icons import ICONS


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Quantum Phoenix Engine — Two Operators, Two Laws",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Valid operator pairs:
  MERGE:         (stress_align, apex_stable)
  REPLICATE:     (dynamo, plates)
  DIVIDE:        (collapse, hollow)
  ABSOLUTE_ZERO: (freeze, lock) or any other pair

Examples:
  python -m quantum_phoenix.cli stress_align apex_stable
  python -m quantum_phoenix.cli dynamo plates
  python -m quantum_phoenix.cli collapse hollow
        """,
    )
    parser.add_argument(
        "opA",
        type=str,
        help="Operator A (e.g., stress_align, dynamo, collapse)",
    )
    parser.add_argument(
        "opB",
        type=str,
        help="Operator B (e.g., apex_stable, plates, hollow)",
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=1,
        help="Number of steps to run (default: 1)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed output including state transitions",
    )

    args = parser.parse_args()

    engine = Phoenix()

    if args.verbose:
        print(f"Starting state: {engine}")
        print(f"Operators: opA={args.opA}, opB={args.opB}\n")

    for i in range(args.count):
        state = engine.step(args.opA, args.opB)
        print(engine)
        if args.verbose and i < args.count - 1:
            print(f"  → Step {i + 1} complete")
        if engine.is_terminal():
            if args.verbose:
                print("  [Terminal state reached]")
            break


if __name__ == "__main__":
    main()
