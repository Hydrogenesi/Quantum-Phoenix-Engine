"""Unit tests for the Phoenix engine core logic."""

import pytest
from quantum_phoenix.engine import Phoenix, State


class TestPhoenixInitialization:
    """Test Phoenix initialization."""

    def test_init_starts_in_merge(self):
        """Phoenix should initialize in MERGE state."""
        engine = Phoenix()
        assert engine.state == State.MERGE

    def test_init_empty_history(self):
        """Phoenix should start with initial state in history."""
        engine = Phoenix()
        assert len(engine.history) == 1
        assert engine.history[0] == State.MERGE

    def test_not_terminal_at_start(self):
        """Phoenix should not be terminal at initialization."""
        engine = Phoenix()
        assert not engine.is_terminal()


class TestMergeState:
    """Test MERGE state transitions."""

    def test_merge_stays_with_correct_operators(self):
        """MERGE should stay in MERGE with (stress_align, apex_stable)."""
        engine = Phoenix()
        engine.step("stress_align", "apex_stable")
        assert engine.state == State.MERGE

    def test_merge_transitions_with_wrong_operators(self):
        """MERGE should transition to REPLICATE with wrong operators."""
        engine = Phoenix()
        engine.step("dynamo", "plates")
        assert engine.state == State.REPLICATE

    def test_merge_multiple_stays(self):
        """MERGE should stay for consecutive correct operator pairs."""
        engine = Phoenix()
        engine.step("stress_align", "apex_stable")
        assert engine.state == State.MERGE
        engine.step("stress_align", "apex_stable")
        assert engine.state == State.MERGE


class TestReplicateState:
    """Test REPLICATE state transitions."""

    def test_merge_to_replicate(self):
        """Can transition from MERGE to REPLICATE."""
        engine = Phoenix()
        engine.step("wrong", "wrong")
        assert engine.state == State.REPLICATE

    def test_replicate_stays_with_correct_operators(self):
        """REPLICATE should stay with (dynamo, plates)."""
        engine = Phoenix()
        engine.step("wrong", "wrong")  # Enter REPLICATE
        engine.step("dynamo", "plates")
        assert engine.state == State.REPLICATE

    def test_replicate_transitions_with_wrong_operators(self):
        """REPLICATE should transition to DIVIDE with wrong operators."""
        engine = Phoenix()
        engine.step("wrong", "wrong")  # Enter REPLICATE
        engine.step("collapse", "hollow")  # Wrong for REPLICATE
        assert engine.state == State.DIVIDE

    def test_replicate_multiple_stays(self):
        """REPLICATE should stay for consecutive (dynamo, plates)."""
        engine = Phoenix()
        engine.step("x", "x")  # MERGE → REPLICATE
        engine.step("dynamo", "plates")  # Stay in REPLICATE
        assert engine.state == State.REPLICATE
        engine.step("dynamo", "plates")  # Stay in REPLICATE
        assert engine.state == State.REPLICATE
        engine.step("dynamo", "plates")  # Stay in REPLICATE
        assert engine.state == State.REPLICATE


class TestDivideState:
    """Test DIVIDE state transitions."""

    def test_replicate_to_divide(self):
        """Can transition from REPLICATE to DIVIDE."""
        engine = Phoenix()
        engine.step("x", "x")  # MERGE → REPLICATE
        engine.step("wrong", "wrong")  # REPLICATE → DIVIDE
        assert engine.state == State.DIVIDE

    def test_divide_stays_with_correct_operators(self):
        """DIVIDE should stay with (collapse, hollow)."""
        engine = Phoenix()
        engine.step("x", "x")  # MERGE → REPLICATE
        engine.step("y", "y")  # REPLICATE → DIVIDE
        engine.step("collapse", "hollow")
        assert engine.state == State.DIVIDE

    def test_divide_transitions_with_wrong_operators(self):
        """DIVIDE should transition to ABSOLUTE_ZERO with wrong operators."""
        engine = Phoenix()
        engine.step("x", "x")  # MERGE → REPLICATE
        engine.step("y", "y")  # REPLICATE → DIVIDE
        engine.step("wrong", "wrong")  # DIVIDE → ABSOLUTE_ZERO
        assert engine.state == State.ABSOLUTE_ZERO


class TestAbsoluteZeroState:
    """Test ABSOLUTE_ZERO state transitions."""

    def test_divide_to_zero(self):
        """Can transition from DIVIDE to ABSOLUTE_ZERO."""
        engine = Phoenix()
        engine.step("x", "x")  # MERGE → REPLICATE
        engine.step("y", "y")  # REPLICATE → DIVIDE
        engine.step("wrong", "wrong")  # DIVIDE → ABSOLUTE_ZERO
        assert engine.state == State.ABSOLUTE_ZERO

    def test_zero_to_apex(self):
        """ABSOLUTE_ZERO should always transition to APEX."""
        engine = Phoenix()
        engine.step("x", "x")  # MERGE → REPLICATE
        engine.step("y", "y")  # REPLICATE → DIVIDE
        engine.step("z", "z")  # DIVIDE → ABSOLUTE_ZERO
        engine.step("anything", "anything")  # ABSOLUTE_ZERO → APEX
        assert engine.state == State.APEX


class TestApexState:
    """Test APEX terminal state."""

    def test_apex_is_terminal(self):
        """APEX should be a terminal state."""
        engine = Phoenix()
        # Burn down to APEX
        engine.step("x", "x")
        engine.step("y", "y")
        engine.step("z", "z")
        engine.step("a", "a")
        assert engine.is_terminal()

    def test_apex_stays_terminal(self):
        """APEX should not transition to any other state."""
        engine = Phoenix()
        # Burn down to APEX
        engine.step("x", "x")
        engine.step("y", "y")
        engine.step("z", "z")
        engine.step("a", "a")
        assert engine.state == State.APEX
        # Try to step again
        engine.step("anything", "anything")
        assert engine.state == State.APEX


class TestEightBeatSequence:
    """Test the canonical eight-beat sequence."""

    def test_canonical_sequence(self):
        """Run the eight-beat sequence: MERGE (2x), REPLICATE (3x), DIVIDE, ZERO, APEX."""
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
        expected_states = [
            State.MERGE,
            State.MERGE,
            State.REPLICATE,
            State.REPLICATE,
            State.REPLICATE,
            State.DIVIDE,
            State.ABSOLUTE_ZERO,
            State.APEX,
        ]

        for i, ((opA, opB), expected_state) in enumerate(zip(ops, expected_states)):
            state = engine.step(opA, opB)
            assert state == expected_state, f"Beat {i + 1}: expected {expected_state}, got {state}"

    def test_history_tracks_all_states(self):
        """History should track all state transitions."""
        engine = Phoenix()
        ops = [
            ("stress_align", "apex_stable"),
            ("dynamo", "plates"),
            ("collapse", "hollow"),
        ]

        for opA, opB in ops:
            engine.step(opA, opB)

        assert len(engine.history) == 4  # Initial MERGE + 3 steps
        assert engine.history[0] == State.MERGE
        assert engine.history[1] == State.MERGE
        assert engine.history[2] == State.REPLICATE
        assert engine.history[3] == State.DIVIDE


class TestReset:
    """Test engine reset functionality."""

    def test_reset_to_merge(self):
        """Reset should return engine to MERGE state."""
        engine = Phoenix()
        engine.step("x", "x")
        engine.step("y", "y")
        assert engine.state != State.MERGE
        engine.reset()
        assert engine.state == State.MERGE

    def test_reset_clears_history(self):
        """Reset should reset history to only initial MERGE."""
        engine = Phoenix()
        engine.step("x", "x")
        engine.step("y", "y")
        engine.reset()
        assert len(engine.history) == 1
        assert engine.history[0] == State.MERGE


class TestStringRepresentation:
    """Test string representation of states."""

    def test_str_representation(self):
        """String representation should match state icons."""
        engine = Phoenix()
        assert str(engine) == "●  merge"
        engine.step("x", "x")
        assert str(engine) == "●● replicate"
        engine.step("y", "y")
        assert str(engine) == "✖  divide"
        engine.step("z", "z")
        assert str(engine) == "❄  absolute_zero"
        engine.step("a", "a")
        assert str(engine) == "★  apex"
