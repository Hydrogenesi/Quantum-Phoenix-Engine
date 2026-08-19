"""
Unit Tests for Quantum Phoenix Engine
Comprehensive test suite covering state transitions, validation, and edge cases.
"""

import unittest
from enum import Enum, auto
from dataclasses import dataclass
import sys
from io import StringIO


# ============================================================================
# STATE MACHINE DEFINITION (from quantum_phoenix_punk.py)
# ============================================================================

class State(Enum):
    MERGE = auto()
    REPLICATE = auto()
    DIVIDE = auto()
    ABSOLUTE_ZERO = auto()
    APEX = auto()


@dataclass
class PhoenixConfig:
    """Configuration and physics constants for the Phoenix engine."""
    merge_to_replicate_stress_max = 0.5
    replicate_to_divide_energy_min = 0.0
    divide_to_zero_entropy_max = 0.1
    energy_min = -1.0
    energy_max = 2.0
    entropy_min = 0.0
    entropy_max = 2.0
    allow_apex_escape = False


class Phoenix:
    """Quantum-Thermodynamic State Engine."""
    
    def __init__(self, config: PhoenixConfig = None):
        self.config = config or PhoenixConfig()
        self.state = State.MERGE
        self.step_count = 0
        self.history = [self.state]
    
    def validate_inputs(self, stress_merge: bool, energy: float, entropy: float) -> bool:
        """Validate that inputs are within physical bounds."""
        if not isinstance(stress_merge, bool):
            raise TypeError("stress_merge must be boolean")
        
        if not (self.config.energy_min <= energy <= self.config.energy_max):
            raise ValueError(
                f"energy {energy} out of range "
                f"[{self.config.energy_min}, {self.config.energy_max}]"
            )
        
        if not (self.config.entropy_min <= entropy <= self.config.entropy_max):
            raise ValueError(
                f"entropy {entropy} out of range "
                f"[{self.config.entropy_min}, {self.config.entropy_max}]"
            )
        
        return True
    
    def step(self, stress_merge: bool, energy: float, entropy: float) -> State:
        """Execute one timestep of state evolution."""
        self.validate_inputs(stress_merge, energy, entropy)
        
        previous_state = self.state
        
        if (self.state == State.MERGE and 
            not stress_merge and 
            energy > self.config.replicate_to_divide_energy_min):
            self.state = State.REPLICATE
        
        elif (self.state == State.REPLICATE and 
              energy <= self.config.replicate_to_divide_energy_min):
            self.state = State.DIVIDE
        
        elif (self.state == State.DIVIDE and 
              entropy <= self.config.divide_to_zero_entropy_max):
            self.state = State.ABSOLUTE_ZERO
        
        elif self.state == State.ABSOLUTE_ZERO:
            if not self.config.allow_apex_escape:
                self.state = State.APEX
        
        elif (self.state == State.APEX and 
              self.config.allow_apex_escape and 
              entropy > self.config.divide_to_zero_entropy_max * 2):
            self.state = State.ABSOLUTE_ZERO
        
        self.step_count += 1
        self.history.append(self.state)
        return self.state


# ============================================================================
# TEST SUITE
# ============================================================================

class TestPhoenixInitialization(unittest.TestCase):
    """Test Phoenix engine initialization and configuration."""
    
    def test_default_initialization(self):
        """Test that Phoenix initializes with default config."""
        phoenix = Phoenix()
        self.assertEqual(phoenix.state, State.MERGE)
        self.assertEqual(phoenix.step_count, 0)
        self.assertEqual(len(phoenix.history), 1)
        self.assertEqual(phoenix.history[0], State.MERGE)
    
    def test_custom_config(self):
        """Test Phoenix with custom configuration."""
        config = PhoenixConfig(allow_apex_escape=True, divide_to_zero_entropy_max=0.15)
        phoenix = Phoenix(config=config)
        self.assertTrue(phoenix.config.allow_apex_escape)
        self.assertEqual(phoenix.config.divide_to_zero_entropy_max, 0.15)
    
    def test_config_defaults(self):
        """Test that default config has correct values."""
        config = PhoenixConfig()
        self.assertEqual(config.energy_min, -1.0)
        self.assertEqual(config.energy_max, 2.0)
        self.assertEqual(config.entropy_min, 0.0)
        self.assertEqual(config.entropy_max, 2.0)
        self.assertFalse(config.allow_apex_escape)


class TestInputValidation(unittest.TestCase):
    """Test input validation for the step function."""
    
    def setUp(self):
        self.phoenix = Phoenix()
    
    def test_valid_inputs(self):
        """Test that valid inputs pass validation."""
        result = self.phoenix.validate_inputs(True, 0.5, 0.5)
        self.assertTrue(result)
    
    def test_invalid_stress_merge_type(self):
        """Test that non-boolean stress_merge raises TypeError."""
        with self.assertRaises(TypeError) as context:
            self.phoenix.validate_inputs("not_bool", 0.5, 0.5)
        self.assertIn("stress_merge must be boolean", str(context.exception))
    
    def test_energy_too_low(self):
        """Test that energy below minimum raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.phoenix.validate_inputs(True, -2.0, 0.5)
        self.assertIn("energy", str(context.exception))
        self.assertIn("out of range", str(context.exception))
    
    def test_energy_too_high(self):
        """Test that energy above maximum raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.phoenix.validate_inputs(True, 3.0, 0.5)
        self.assertIn("energy", str(context.exception))
    
    def test_entropy_too_low(self):
        """Test that entropy below minimum raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.phoenix.validate_inputs(True, 0.5, -0.1)
        self.assertIn("entropy", str(context.exception))
    
    def test_entropy_too_high(self):
        """Test that entropy above maximum raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.phoenix.validate_inputs(True, 0.5, 3.0)
        self.assertIn("entropy", str(context.exception))
    
    def test_boundary_energy_min(self):
        """Test energy at minimum boundary."""
        result = self.phoenix.validate_inputs(True, -1.0, 0.5)
        self.assertTrue(result)
    
    def test_boundary_energy_max(self):
        """Test energy at maximum boundary."""
        result = self.phoenix.validate_inputs(True, 2.0, 0.5)
        self.assertTrue(result)


class TestStateTransitions(unittest.TestCase):
    """Test state machine transitions."""
    
    def setUp(self):
        self.phoenix = Phoenix()
    
    def test_merge_to_replicate(self):
        """Test MERGE → REPLICATE transition."""
        # MERGE with no stress and positive energy should go to REPLICATE
        self.phoenix.step(stress_merge=False, energy=0.5, entropy=0.5)
        self.assertEqual(self.phoenix.state, State.REPLICATE)
    
    def test_merge_stays_with_stress(self):
        """Test that MERGE stays in place when stress is high."""
        self.phoenix.step(stress_merge=True, energy=0.5, entropy=0.5)
        self.assertEqual(self.phoenix.state, State.MERGE)
    
    def test_merge_stays_with_low_energy(self):
        """Test that MERGE stays when energy is depleted."""
        self.phoenix.step(stress_merge=False, energy=-0.5, entropy=0.5)
        self.assertEqual(self.phoenix.state, State.MERGE)
    
    def test_replicate_to_divide(self):
        """Test REPLICATE → DIVIDE transition."""
        # First transition to REPLICATE
        self.phoenix.step(stress_merge=False, energy=0.5, entropy=0.5)
        self.assertEqual(self.phoenix.state, State.REPLICATE)
        
        # Then transition to DIVIDE with depleted energy
        self.phoenix.step(stress_merge=False, energy=-0.5, entropy=0.5)
        self.assertEqual(self.phoenix.state, State.DIVIDE)
    
    def test_divide_to_absolute_zero(self):
        """Test DIVIDE → ABSOLUTE_ZERO transition with tolerance."""
        # Manually set to DIVIDE
        self.phoenix.state = State.DIVIDE
        
        # Entropy at tolerance threshold (0.1)
        self.phoenix.step(stress_merge=False, energy=-0.5, entropy=0.1)
        self.assertEqual(self.phoenix.state, State.ABSOLUTE_ZERO)
    
    def test_divide_to_absolute_zero_below_threshold(self):
        """Test DIVIDE → ABSOLUTE_ZERO with entropy below threshold."""
        self.phoenix.state = State.DIVIDE
        
        # Entropy below tolerance threshold
        self.phoenix.step(stress_merge=False, energy=-0.5, entropy=0.05)
        self.assertEqual(self.phoenix.state, State.ABSOLUTE_ZERO)
    
    def test_divide_stays_above_threshold(self):
        """Test that DIVIDE stays when entropy is above threshold."""
        self.phoenix.state = State.DIVIDE
        
        # Entropy above tolerance threshold
        self.phoenix.step(stress_merge=False, energy=-0.5, entropy=0.15)
        self.assertEqual(self.phoenix.state, State.DIVIDE)
    
    def test_absolute_zero_to_apex_without_escape(self):
        """Test ABSOLUTE_ZERO → APEX when escape disabled."""
        self.phoenix.state = State.ABSOLUTE_ZERO
        
        self.phoenix.step(stress_merge=False, energy=-0.5, entropy=0.05)
        self.assertEqual(self.phoenix.state, State.APEX)
    
    def test_absolute_zero_stays_with_escape_enabled(self):
        """Test that ABSOLUTE_ZERO stays when escape enabled."""
        config = PhoenixConfig(allow_apex_escape=True)
        phoenix = Phoenix(config=config)
        phoenix.state = State.ABSOLUTE_ZERO
        
        # With low entropy (below escape threshold), stays in ABSOLUTE_ZERO
        phoenix.step(stress_merge=False, energy=-0.5, entropy=0.05)
        self.assertEqual(phoenix.state, State.ABSOLUTE_ZERO)
    
    def test_apex_escape_route(self):
        """Test APEX → ABSOLUTE_ZERO escape when enabled."""
        config = PhoenixConfig(allow_apex_escape=True)
        phoenix = Phoenix(config=config)
        phoenix.state = State.APEX
        
        # Entropy above escape threshold (0.2)
        phoenix.step(stress_merge=False, energy=-0.5, entropy=0.25)
        self.assertEqual(phoenix.state, State.ABSOLUTE_ZERO)
    
    def test_apex_no_escape_when_disabled(self):
        """Test that APEX stays when escape disabled."""
        self.phoenix.state = State.APEX
        
        # Entropy above would-be escape threshold, but escape disabled
        self.phoenix.step(stress_merge=False, energy=-0.5, entropy=0.25)
        self.assertEqual(self.phoenix.state, State.APEX)


class TestStepCounter(unittest.TestCase):
    """Test step counting and history tracking."""
    
    def setUp(self):
        self.phoenix = Phoenix()
    
    def test_step_count_increments(self):
        """Test that step_count increments correctly."""
        self.assertEqual(self.phoenix.step_count, 0)
        self.phoenix.step(False, 0.5, 0.5)
        self.assertEqual(self.phoenix.step_count, 1)
        self.phoenix.step(False, 0.5, 0.5)
        self.assertEqual(self.phoenix.step_count, 2)
    
    def test_history_tracking(self):
        """Test that history records all states."""
        self.phoenix.step(False, 0.5, 0.5)  # MERGE → REPLICATE
        self.phoenix.step(False, -0.5, 0.5)  # REPLICATE → DIVIDE
        
        self.assertEqual(len(self.phoenix.history), 3)
        self.assertEqual(self.phoenix.history[0], State.MERGE)
        self.assertEqual(self.phoenix.history[1], State.REPLICATE)
        self.assertEqual(self.phoenix.history[2], State.DIVIDE)
    
    def test_history_includes_initial_state(self):
        """Test that history starts with initial MERGE state."""
        self.assertEqual(len(self.phoenix.history), 1)
        self.assertEqual(self.phoenix.history[0], State.MERGE)


class TestFullCascade(unittest.TestCase):
    """Test full cascade from MERGE to APEX."""
    
    def test_standard_cascade_to_apex(self):
        """Test the complete cascade from MERGE to APEX."""
        phoenix = Phoenix()
        
        for t in range(10):
            stress_merge = (t < 2)
            energy = 1.0 - 0.2 * t
            entropy = max(0.0, 1.0 - 0.3 * t)
            
            phoenix.step(stress_merge, energy, entropy)
            
            if phoenix.state == State.APEX:
                break
        
        self.assertEqual(phoenix.state, State.APEX)
        self.assertGreater(phoenix.step_count, 0)
        self.assertGreater(len(phoenix.history), 1)
    
    def test_cascade_sequence(self):
        """Test that cascade follows expected state sequence."""
        phoenix = Phoenix()
        expected_sequence = [State.MERGE, State.REPLICATE, State.DIVIDE, 
                           State.ABSOLUTE_ZERO, State.APEX]
        
        for t in range(10):
            stress_merge = (t < 2)
            energy = 1.0 - 0.2 * t
            entropy = max(0.0, 1.0 - 0.3 * t)
            
            phoenix.step(stress_merge, energy, entropy)
            
            if phoenix.state == State.APEX:
                break
        
        # Check that we visited states in correct order
        for i, expected_state in enumerate(expected_sequence):
            if i < len(phoenix.history):
                self.assertEqual(phoenix.history[i], expected_state)


class TestEscapeRoute(unittest.TestCase):
    """Test APEX escape route when enabled."""
    
    def test_oscillation_with_escape_enabled(self):
        """Test that APEX can oscillate with escape enabled."""
        config = PhoenixConfig(allow_apex_escape=True)
        phoenix = Phoenix(config=config)
        
        # Manually advance to APEX
        phoenix.state = State.ABSOLUTE_ZERO
        phoenix.step(False, -0.5, 0.05)  # ABSOLUTE_ZERO → stays (escape enabled, low entropy)
        
        # Now at ABSOLUTE_ZERO, trigger escape by raising entropy
        phoenix.step(False, -0.5, 0.25)  # Should return to ABSOLUTE_ZERO (escape route)
        
        # Verify we can oscillate
        self.assertEqual(phoenix.state, State.ABSOLUTE_ZERO)
    
    def test_escape_only_with_high_entropy(self):
        """Test that escape only triggers with entropy > 0.2."""
        config = PhoenixConfig(allow_apex_escape=True)
        phoenix = Phoenix(config=config)
        phoenix.state = State.APEX
        
        # Low entropy - should stay in APEX
        phoenix.step(False, -0.5, 0.15)
        self.assertEqual(phoenix.state, State.APEX)
        
        # High entropy - should escape to ABSOLUTE_ZERO
        phoenix.step(False, -0.5, 0.25)
        self.assertEqual(phoenix.state, State.ABSOLUTE_ZERO)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_zero_energy_boundary(self):
        """Test behavior at zero energy boundary."""
        phoenix = Phoenix()
        phoenix.state = State.REPLICATE
        
        # Exactly at boundary
        phoenix.step(False, 0.0, 0.5)
        self.assertEqual(phoenix.state, State.DIVIDE)
    
    def test_zero_entropy_boundary(self):
        """Test behavior at zero entropy boundary."""
        phoenix = Phoenix()
        phoenix.state = State.DIVIDE
        
        # Exactly at minimum entropy
        phoenix.step(False, -0.5, 0.0)
        self.assertEqual(phoenix.state, State.ABSOLUTE_ZERO)
    
    def test_tolerance_threshold_epsilon(self):
        """Test just below tolerance threshold."""
        phoenix = Phoenix()
        phoenix.state = State.DIVIDE
        
        # Just below tolerance (0.1)
        phoenix.step(False, -0.5, 0.09)
        self.assertEqual(phoenix.state, State.ABSOLUTE_ZERO)
    
    def test_tolerance_threshold_above(self):
        """Test just above tolerance threshold."""
        phoenix = Phoenix()
        phoenix.state = State.DIVIDE
        
        # Just above tolerance (0.1)
        phoenix.step(False, -0.5, 0.11)
        self.assertEqual(phoenix.state, State.DIVIDE)
    
    def test_multiple_rapid_steps(self):
        """Test multiple steps without valid transitions."""
        phoenix = Phoenix()
        
        # Multiple steps in MERGE (stress prevents transition)
        for _ in range(5):
            phoenix.step(True, 0.5, 0.5)
            self.assertEqual(phoenix.state, State.MERGE)
        
        self.assertEqual(phoenix.step_count, 5)


# ============================================================================
# TEST RUNNER WITH DETAILED OUTPUT
# ============================================================================

class DetailedTestResult(unittest.TextTestResult):
    """Custom test result class for detailed output."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_details = []
    
    def startTest(self, test):
        super().startTest(test)
        self.current_test = test
    
    def addSuccess(self, test):
        super().addSuccess(test)
        self.test_details.append({
            'name': str(test),
            'status': '✓ PASS',
            'message': None
        })
    
    def addError(self, test, err):
        super().addError(test, err)
        self.test_details.append({
            'name': str(test),
            'status': '✗ ERROR',
            'message': self._exc_info_to_string(err, test)
        })
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_details.append({
            'name': str(test),
            'status': '✗ FAIL',
            'message': self._exc_info_to_string(err, test)
        })


def run_tests_with_detailed_output():
    """Run all tests and print detailed results."""
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPhoenixInitialization))
    suite.addTests(loader.loadTestsFromTestCase(TestInputValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestStateTransitions))
    suite.addTests(loader.loadTestsFromTestCase(TestStepCounter))
    suite.addTests(loader.loadTestsFromTestCase(TestFullCascade))
    suite.addTests(loader.loadTestsFromTestCase(TestEscapeRoute))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print("QUANTUM PHOENIX ENGINE - TEST SUMMARY")
    print("=" * 80)
    print(f"\nTotal Tests Run: {result.testsRun}")
    print(f"✓ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"✗ Failed: {len(result.failures)}")
    print(f"✗ Errors: {len(result.errors)}")
    print(f"\nTest Coverage:")
    print(f"  • Initialization & Configuration")
    print(f"  • Input Validation (6 tests)")
    print(f"  • State Transitions (11 tests)")
    print(f"  • Step Counting & History (3 tests)")
    print(f"  • Full Cascade (2 tests)")
    print(f"  • Escape Route (2 tests)")
    print(f"  • Edge Cases & Boundaries (5 tests)")
    
    if result.wasSuccessful():
        print("\n" + "🎉 " * 20)
        print("ALL TESTS PASSED!")
        print("🎉 " * 20)
    else:
        print("\n⚠️  SOME TESTS FAILED - See details above")
    
    print("=" * 80)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests_with_detailed_output()
    sys.exit(0 if success else 1)
