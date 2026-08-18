#!/usr/bin/env python3
"""Run the full eight-beat journey to APEX."""

from quantum_phoenix import Phoenix


def main():
    engine = Phoenix()
    ops = [
        ("stress_align", "apex_stable"),   # Beat 1: merge
        ("stress_align", "apex_stable"),   # Beat 2: merge
        ("dynamo", "plates"),              # Beat 3: replicate
        ("dynamo", "plates"),              # Beat 4: replicate
        ("dynamo", "plates"),              # Beat 5: replicate
        ("collapse", "hollow"),            # Beat 6: divide
        ("freeze", "lock"),                # Beat 7: absolute_zero
        ("none", "none"),                  # Beat 8: apex
    ]

    print("🔥 Quantum Phoenix Engine — Eight-Beat Journey")
    print("═" * 50)

    for beat, (opA, opB) in enumerate(ops, 1):
        state = engine.step(opA, opB)
        print(f"Beat {beat}: {engine}")
        if engine.is_terminal():
            print("═" * 50)
            print("✨ Phoenix has reached APEX")
            break

    print()
    print("Journey summary:")
    print(f"Total beats: {len(engine.history)}")
    print(f"State progression: {' → '.join(s.name for s in engine.history)}")


if __name__ == "__main__":
    main()
