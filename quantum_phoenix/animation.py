"""Terminal animation loop for the Quantum Phoenix Engine."""

import time
from .engine import Phoenix
from .icons import ICONS


def run_sequence(delay=0.3, verbose=False):
    """Run the canonical eight-beat sequence.

    Args:
        delay (float): Delay between beats in seconds (default: 0.3)
        verbose (bool): Print transition info alongside beats
    """
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

    if verbose:
        print("🔥 Quantum Phoenix Engine — Eight-Beat Sequence")
        print("━" * 50)

    for beat, (opA, opB) in enumerate(ops, 1):
        state = engine.step(opA, opB)
        beat_output = str(engine)
        print(beat_output)

        if verbose:
            print(f"   Beat {beat}: ({opA}, {opB}) → {state.name}")

        if engine.is_terminal():
            if verbose:
                print("━" * 50)
                print("✨ Song complete. Phoenix has reached APEX.")
            break

        time.sleep(delay)


def run_custom(operators_list, delay=0.3, verbose=False):
    """Run a custom sequence of operator pairs.

    Args:
        operators_list (list): List of (opA, opB) tuples
        delay (float): Delay between beats in seconds
        verbose (bool): Print transition info
    """
    engine = Phoenix()

    if verbose:
        print("🔥 Custom Quantum Phoenix Engine Sequence")
        print("━" * 50)

    for beat, (opA, opB) in enumerate(operators_list, 1):
        state = engine.step(opA, opB)
        print(str(engine))

        if verbose:
            print(f"   Beat {beat}: ({opA}, {opB}) → {state.name}")

        if engine.is_terminal():
            if verbose:
                print("━" * 50)
                print("✨ Custom sequence complete.")
            break

        time.sleep(delay)


if __name__ == "__main__":
    run_sequence(delay=0.3, verbose=True)
