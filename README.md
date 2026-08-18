# ⚡ Quantum Phoenix Engine

**Two Operators. Two Laws Per Step.**

A minimalist four-state finite state machine driven by operator pairs and transition laws, burning down eight beats from **MERGE** to **APEX**.

```
●  merge
●  merge
●● replicate
●● replicate
●● replicate
✖  divide
❄  absolute_zero
★  apex
```

## Installation

### From PyPI

```bash
pip install quantum-phoenix-engine
```

### From source

```bash
git clone https://github.com/Hydrogenesi/Quantum-Phoenix-Engine.git
cd Quantum-Phoenix-Engine
pip install -e .
```

## Quick Start

### Run the canonical eight-beat sequence

```bash
python -m quantum_phoenix.animation
```

### Use the CLI

```bash
# Single step
phoenix stress_align apex_stable

# Multiple steps
phoenix dynamo plates -c 3 -v
```

### Python API

```python
from quantum_phoenix import Phoenix

engine = Phoenix()

# Step 1: MERGE
state = engine.step("stress_align", "apex_stable")
print(engine)  # ●  merge

# Step 2: MERGE (stable)
state = engine.step("stress_align", "apex_stable")
print(engine)  # ●  merge

# Step 3: REPLICATE (transition)
state = engine.step("dynamo", "plates")
print(engine)  # ●● replicate

# Continue the sequence...
while not engine.is_terminal():
    state = engine.step("dynamo", "plates")
    print(engine)
```

## Architecture

### Five States

| State | Icon | Meaning |
|-------|------|----------|
| **MERGE** | `●` | Stress alignment, apex stability |
| **REPLICATE** | `●●` | Dynamo amplification, plate counter-motion |
| **DIVIDE** | `✖` | Convection collapse, apex hollowing |
| **ABSOLUTE_ZERO** | `❄` | Entropy lock, motion extinction |
| **APEX** | `★` | Terminal state — no encore |

### Transition Laws

Each state is governed by two operators and two laws:

#### MERGE (●)

**Operators:**
- Operator A: Stress alignment
- Operator B: Apex stability

**Laws:**
- Law 1: If stress aligns → stay in MERGE
- Law 2: If stress fails → jump to REPLICATE

```python
if (opA, opB) == ("stress_align", "apex_stable"):
    next_state = MERGE
else:
    next_state = REPLICATE
```

#### REPLICATE (●●)

**Operators:**
- Operator A: Dynamo amplification
- Operator B: Plate counter-motion

**Laws:**
- Law 1: If energy > threshold → stay in REPLICATE
- Law 2: If energy ≤ threshold → fall to DIVIDE

```python
if (opA, opB) == ("dynamo", "plates"):
    next_state = REPLICATE
else:
    next_state = DIVIDE
```

#### DIVIDE (✖)

**Operators:**
- Operator A: Convection collapse
- Operator B: Apex hollowing

**Laws:**
- Law 1: If entropy > 0 → stay in DIVIDE
- Law 2: If entropy = 0 → freeze into ABSOLUTE_ZERO

```python
if (opA, opB) == ("collapse", "hollow"):
    next_state = DIVIDE
else:
    next_state = ABSOLUTE_ZERO
```

#### ABSOLUTE_ZERO (❄)

**Operators:**
- Operator A: Entropy lock
- Operator B: Motion extinction

**Laws:**
- Law 1: If entropy = 0 → remain frozen
- Law 2: If frozen → transition to APEX (terminal)

```python
next_state = APEX
```

#### APEX (★)

**Terminal State** — No transitions, no operators, no laws.

## Package Structure

```
quantum-phoenix-engine/
├── quantum_phoenix/
│   ├── __init__.py          # Package exports
│   ├── engine.py            # Core Phoenix class + State enum
│   ├── icons.py             # Visual representations
│   ├── cli.py               # Command-line interface
│   └── animation.py         # Terminal animation sequences
├── tests/
│   ├── test_engine.py       # Unit tests
│   └── test_transitions.py  # Transition verification
├── examples/
│   ├── basic_usage.py       # Simple API example
│   ├── custom_sequence.py   # Custom operator sequences
│   └── full_journey.py      # Complete eight-beat run
├── setup.py                 # PyPI configuration
├── README.md                # This file
└── LICENSE                  # MIT License
```

## Examples

### Example 1: Basic Usage

```python
from quantum_phoenix import Phoenix, State

engine = Phoenix()
print(f"Initial state: {engine}")  # ●  merge

state = engine.step("stress_align", "apex_stable")
print(f"After step: {engine}")  # ●  merge

print(f"Is terminal? {engine.is_terminal()}")  # False
```

### Example 2: Full Eight-Beat Sequence

```python
from quantum_phoenix import Phoenix

engine = Phoenix()
ops = [
    ("stress_align", "apex_stable"),   # merge
    ("stress_align", "apex_stable"),   # merge
    ("dynamo", "plates"),              # replicate
    ("dynamo", "plates"),              # replicate
    ("dynamo", "plates"),              # replicate
    ("collapse", "hollow"),            # divide
    ("freeze", "lock"),                # absolute_zero
    ("none", "none"),                  # apex
]

for i, (opA, opB) in enumerate(ops, 1):
    state = engine.step(opA, opB)
    print(f"Beat {i}: {engine}")
    if engine.is_terminal():
        print("✨ Phoenix has reached APEX")
        break
```

### Example 3: Animation Loop

```python
from quantum_phoenix.animation import run_sequence

# Run with default timing (0.3 second delay)
run_sequence(delay=0.3, verbose=True)
```

### Example 4: Custom Sequence

```python
from quantum_phoenix.animation import run_custom

custom_ops = [
    ("stress_align", "apex_stable"),
    ("dynamo", "plates"),
    ("collapse", "hollow"),
]

run_custom(custom_ops, delay=0.5, verbose=True)
```

## Command-Line Usage

### Basic Step

```bash
$ phoenix stress_align apex_stable
●  merge
```

### Multiple Steps

```bash
$ phoenix dynamo plates -c 3
●● replicate
●● replicate
●● replicate
```

### Verbose Output

```bash
$ phoenix stress_align apex_stable -v
Starting state: ●  merge
Operators: opA=stress_align, opB=apex_stable

●  merge
  → Step 1 complete
```

### Full Eight-Beat Run

```bash
$ python -m quantum_phoenix.animation
●  merge
●  merge
●● replicate
●● replicate
●● replicate
✖  divide
❄  absolute_zero
★  apex
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=quantum_phoenix tests/

# Run a specific test file
python -m pytest tests/test_engine.py -v
```

## Design Philosophy

> **Two operators. Two laws per step. If they fail, you drop. If they freeze, you end.**

The Quantum Phoenix Engine encodes a complete deterministic state machine in minimal code:

1. **Each state is a checkpoint** — MERGE, REPLICATE, DIVIDE, ABSOLUTE_ZERO, APEX
2. **Each transition is gated by two operators** — pairs like (stress_align, apex_stable)
3. **Each gate is enforced by two laws** — success conditions and failure paths
4. **The output is a song** — eight beats that burn from ignition (MERGE) to terminal (APEX)

No randomness. No cycles (except within MERGE and REPLICATE). No implicit state. Pure state machine.

## License

MIT License — See LICENSE file for details.

## Author

James Stanley  
[GitHub Profile](https://github.com/Hydrogenesi)

---

**Burn it down to APEX. ★**
