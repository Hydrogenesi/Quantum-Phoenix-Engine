"""Core Quantum Phoenix Engine — Two Operators, Two Laws.

Four states driven by operator pairs:
  - MERGE: stress alignment + apex stability
  - REPLICATE: dynamo amplification + plate counter-motion
  - DIVIDE: convection collapse + apex hollowing
  - ABSOLUTE_ZERO: entropy lock + motion extinction
  - APEX: terminal state
"""

from enum import Enum, auto


class State(Enum):
    """Five states of the Phoenix engine."""
    MERGE = auto()
    REPLICATE = auto()
    DIVIDE = auto()
    ABSOLUTE_ZERO = auto()
    APEX = auto()


class Phoenix:
    """Quantum Phoenix Engine — Two Operators, Two Laws Per Step.

    Each state transition is governed by two operators (opA, opB) and two laws
    that determine whether to stay in the current state or transition to the next.

    States:
      MERGE (●) → REPLICATE (●●) → DIVIDE (✖) → ABSOLUTE_ZERO (❄) → APEX (★)
    """

    def __init__(self):
        """Initialize the engine in MERGE state."""
        self.state = State.MERGE
        self.history = [self.state]

    def step(self, opA, opB):
        """Advance the engine by one beat.

        Args:
            opA (str): First operator (e.g., 'stress_align', 'dynamo', 'collapse')
            opB (str): Second operator (e.g., 'apex_stable', 'plates', 'hollow')

        Returns:
            State: The new state after the transition.
        """
        if self.state == State.MERGE:
            # Law 1: If stress aligns → stay in MERGE
            # Law 2: If stress fails → jump to REPLICATE
            if (opA, opB) == ("stress_align", "apex_stable"):
                self.state = State.MERGE
            else:
                self.state = State.REPLICATE

        elif self.state == State.REPLICATE:
            # Law 1: If energy > threshold → stay in REPLICATE
            # Law 2: If energy ≤ threshold → fall to DIVIDE
            if (opA, opB) == ("dynamo", "plates"):
                self.state = State.REPLICATE
            else:
                self.state = State.DIVIDE

        elif self.state == State.DIVIDE:
            # Law 1: If entropy > 0 → stay in DIVIDE
            # Law 2: If entropy = 0 → freeze into ABSOLUTE_ZERO
            if (opA, opB) == ("collapse", "hollow"):
                self.state = State.DIVIDE
            else:
                self.state = State.ABSOLUTE_ZERO

        elif self.state == State.ABSOLUTE_ZERO:
            # Law 1: If entropy = 0 → remain frozen
            # Law 2: If frozen → transition to APEX (terminal)
            self.state = State.APEX

        elif self.state == State.APEX:
            # Terminal state — no transitions
            pass

        self.history.append(self.state)
        return self.state

    def reset(self):
        """Reset the engine to MERGE state."""
        self.state = State.MERGE
        self.history = [self.state]

    def is_terminal(self):
        """Check if the engine has reached APEX."""
        return self.state == State.APEX

    def __str__(self):
        """Return a string representation of the current state."""
        from .icons import ICONS
        return ICONS.get(self.state, "unknown")
