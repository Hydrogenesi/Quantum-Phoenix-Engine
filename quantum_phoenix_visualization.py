"""
Quantum Phoenix Engine - Visualization & Analysis
Generates state diagrams and entropy curve plots for the Phoenix state machine.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from enum import Enum, auto
from dataclasses import dataclass

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
# VISUALIZATION FUNCTIONS
# ============================================================================

def plot_state_diagram():
    """
    Create a state diagram showing transitions between Phoenix states.
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 6)
    ax.axis('off')
    
    # State positions (x, y)
    states = {
        State.MERGE:        (2, 4),
        State.REPLICATE:    (5, 4),
        State.DIVIDE:       (8, 4),
        State.ABSOLUTE_ZERO: (5, 1),
        State.APEX:         (8, 1),
    }
    
    # State colors and icons
    state_colors = {
        State.MERGE:        '#3498db',      # Blue
        State.REPLICATE:    '#2ecc71',      # Green
        State.DIVIDE:       '#e74c3c',      # Red
        State.ABSOLUTE_ZERO: '#9b59b6',     # Purple
        State.APEX:         '#f39c12',      # Orange
    }
    
    state_icons = {
        State.MERGE:        '●',
        State.REPLICATE:    '●●',
        State.DIVIDE:       '✖',
        State.ABSOLUTE_ZERO: '❄',
        State.APEX:         '★',
    }
    
    state_labels = {
        State.MERGE:        'MERGE\n(Superposition)',
        State.REPLICATE:    'REPLICATE\n(Branching)',
        State.DIVIDE:       'DIVIDE\n(Decoherence)',
        State.ABSOLUTE_ZERO: 'ABSOLUTE_ZERO\n(Inversion)',
        State.APEX:         'APEX\n(Transcendence)',
    }
    
    # Draw state boxes
    for state, (x, y) in states.items():
        box = FancyBboxPatch((x - 0.7, y - 0.5), 1.4, 1.0,
                             boxstyle="round,pad=0.1", 
                             edgecolor=state_colors[state],
                             facecolor=state_colors[state],
                             alpha=0.3,
                             linewidth=2.5)
        ax.add_patch(box)
        
        # State label
        ax.text(x, y + 0.2, state_labels[state],
               ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Icon
        ax.text(x, y - 0.35, state_icons[state],
               ha='center', va='center', fontsize=16)
    
    # Define transitions with conditions
    transitions = [
        # (from_state, to_state, label, curve_direction)
        (State.MERGE, State.REPLICATE, 
         'stress_merge=False\nenergy > 0', 'normal'),
        
        (State.REPLICATE, State.DIVIDE,
         'energy ≤ 0', 'normal'),
        
        (State.DIVIDE, State.ABSOLUTE_ZERO,
         'entropy ≤ 0.1', 'down'),
        
        (State.ABSOLUTE_ZERO, State.APEX,
         'automatic', 'right'),
        
        (State.APEX, State.ABSOLUTE_ZERO,
         'escape enabled\nentropy > 0.2', 'up'),
    ]
    
    # Draw arrows
    for from_state, to_state, label, direction in transitions:
        x1, y1 = states[from_state]
        x2, y2 = states[to_state]
        
        if direction == 'normal':
            # Straight arrow
            arrow = FancyArrowPatch((x1 + 0.7, y1), (x2 - 0.7, y2),
                                  arrowstyle='->', mutation_scale=25,
                                  color='#2c3e50', linewidth=2.5,
                                  connectionstyle="arc3,rad=0")
        elif direction == 'down':
            # Curved arrow down
            arrow = FancyArrowPatch((x1, y1 - 0.5), (x2, y2 + 0.5),
                                  arrowstyle='->', mutation_scale=25,
                                  color='#2c3e50', linewidth=2.5,
                                  connectionstyle="arc3,rad=-0.4")
        elif direction == 'right':
            # Curved arrow to the right
            arrow = FancyArrowPatch((x1 + 0.7, y1), (x2, y2 + 0.5),
                                  arrowstyle='->', mutation_scale=25,
                                  color='#2c3e50', linewidth=2.5,
                                  connectionstyle="arc3,rad=0.5")
        elif direction == 'up':
            # Curved arrow up (escape)
            arrow = FancyArrowPatch((x2 - 0.7, y2), (x1, y1 + 0.5),
                                  arrowstyle='->', mutation_scale=25,
                                  color='#e74c3c', linewidth=2.0, linestyle='--',
                                  connectionstyle="arc3,rad=0.4")
        
        ax.add_patch(arrow)
        
        # Label position
        if direction == 'normal':
            label_x = (x1 + x2) / 2
            label_y = y1 + 0.7
        elif direction == 'down':
            label_x = (x1 + x2) / 2 - 0.5
            label_y = (y1 + y2) / 2
        elif direction == 'right':
            label_x = (x1 + x2) / 2 + 0.5
            label_y = (y1 + y2) / 2
        elif direction == 'up':
            label_x = (x1 + x2) / 2 + 0.5
            label_y = (y1 + y2) / 2 - 0.3
        
        ax.text(label_x, label_y, label,
               ha='center', va='center', fontsize=9,
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, pad=0.3))
    
    # Title and legend
    ax.text(5, 5.5, 'Quantum Phoenix Engine - State Transition Diagram',
           ha='center', fontsize=16, fontweight='bold')
    
    # Add legend for escape mode
    escape_line = mpatches.Patch(color='#e74c3c', linestyle='--', label='APEX Escape Route (Optional)')
    ax.legend(handles=[escape_line], loc='upper left', fontsize=10)
    
    plt.tight_layout()
    return fig


def plot_entropy_curves():
    """
    Simulate and plot entropy vs time for different scenarios.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Scenario 1: Standard evolution (no escape)
    ax = axes[0, 0]
    engine = Phoenix()
    times, energies, entropies, state_changes = [], [], [], []
    
    for t in range(20):
        stress_merge = (t < 2)
        energy = 1.0 - 0.2 * t
        entropy = max(0.0, 1.0 - 0.3 * t)
        
        times.append(t)
        energies.append(energy)
        entropies.append(entropy)
        state_changes.append(engine.state.value)
        
        engine.step(stress_merge, energy, entropy)
        
        if engine.state == State.APEX:
            break
    
    ax.plot(times, entropies, 'o-', linewidth=2.5, markersize=6, label='Entropy', color='#9b59b6')
    ax.axhline(y=0.1, color='#e74c3c', linestyle='--', linewidth=2, label='Transition Threshold (0.1)')
    ax.fill_between(times, 0, entropies, alpha=0.2, color='#9b59b6')
    ax.set_xlabel('Time Step', fontsize=11, fontweight='bold')
    ax.set_ylabel('Entropy', fontsize=11, fontweight='bold')
    ax.set_title('Scenario 1: Standard Evolution\n(No Escape Route)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    ax.set_ylim([0, 1.2])
    
    # Scenario 2: Energy depletion curve
    ax = axes[0, 1]
    times, energies = [], []
    
    for t in range(20):
        times.append(t)
        energies.append(1.0 - 0.2 * t)
    
    ax.plot(times, energies, 's-', linewidth=2.5, markersize=6, label='Energy', color='#e74c3c')
    ax.axhline(y=0, color='#2c3e50', linestyle='--', linewidth=2, label='Depletion Point (E=0)')
    ax.fill_between(times, energies, 0, alpha=0.2, color='#e74c3c')
    ax.set_xlabel('Time Step', fontsize=11, fontweight='bold')
    ax.set_ylabel('Energy', fontsize=11, fontweight='bold')
    ax.set_title('Energy Depletion Dynamics', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Scenario 3: With apex escape enabled
    ax = axes[1, 0]
    config_escape = PhoenixConfig(allow_apex_escape=True)
    engine_escape = Phoenix(config=config_escape)
    times_e, entropies_e, state_vals = [], [], []
    
    for t in range(20):
        stress_merge = False
        energy = 0.5 - 0.1 * t
        # Entropy oscillates: drops, then rises to trigger escape
        entropy = abs(1.0 - 0.3 * t) if t < 5 else 0.5 + 0.2 * (t - 5)
        entropy = min(entropy, 2.0)  # Cap at max
        
        times_e.append(t)
        entropies_e.append(entropy)
        state_vals.append(engine_escape.state.value)
        
        engine_escape.step(stress_merge, energy, entropy)
    
    ax.plot(times_e, entropies_e, 'D-', linewidth=2.5, markersize=6, label='Entropy (Escape Enabled)', color='#f39c12')
    ax.axhline(y=0.1, color='#e74c3c', linestyle='--', linewidth=2, label='Low Threshold (0.1)')
    ax.axhline(y=0.2, color='#3498db', linestyle='--', linewidth=2, label='Escape Threshold (0.2)')
    ax.fill_between(times_e, 0, entropies_e, alpha=0.2, color='#f39c12')
    ax.set_xlabel('Time Step', fontsize=11, fontweight='bold')
    ax.set_ylabel('Entropy', fontsize=11, fontweight='bold')
    ax.set_title('Scenario 3: With APEX Escape Route\n(entropy oscillation triggers return)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Scenario 4: Phase space (Energy vs Entropy)
    ax = axes[1, 1]
    times, energies_ps, entropies_ps = [], [], []
    
    for t in range(20):
        times.append(t)
        energy = 1.0 - 0.2 * t
        entropy = max(0.0, 1.0 - 0.3 * t)
        energies_ps.append(energy)
        entropies_ps.append(entropy)
    
    scatter = ax.scatter(energies_ps, entropies_ps, c=times, s=100, cmap='viridis', 
                        edgecolors='black', linewidth=1.5, alpha=0.8, zorder=3)
    ax.plot(energies_ps, entropies_ps, 'k--', alpha=0.3, linewidth=1, zorder=1)
    
    # Mark transition points
    ax.axvline(x=0, color='#e74c3c', linestyle=':', linewidth=2, label='Energy Depletion (E=0)', alpha=0.7)
    ax.axhline(y=0.1, color='#9b59b6', linestyle=':', linewidth=2, label='Entropy Collapse (S=0.1)', alpha=0.7)
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Time Step', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Energy', fontsize=11, fontweight='bold')
    ax.set_ylabel('Entropy', fontsize=11, fontweight='bold')
    ax.set_title('Phase Space: Energy vs Entropy Evolution', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9, loc='upper right')
    
    plt.suptitle('Quantum Phoenix Engine - Entropy & Energy Dynamics', 
                fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    return fig


def plot_state_timeline():
    """
    Plot the state transitions over time for multiple scenarios.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    state_colors_map = {
        1: '#3498db',      # MERGE
        2: '#2ecc71',      # REPLICATE
        3: '#e74c3c',      # DIVIDE
        4: '#9b59b6',      # ABSOLUTE_ZERO
        5: '#f39c12',      # APEX
    }
    
    state_names = {
        1: 'MERGE',
        2: 'REPLICATE',
        3: 'DIVIDE',
        4: 'ABSOLUTE_ZERO',
        5: 'APEX',
    }
    
    # Scenario A: Standard evolution
    ax = axes[0]
    engine = Phoenix()
    steps, state_vals = [], []
    
    for t in range(20):
        stress_merge = (t < 2)
        energy = 1.0 - 0.2 * t
        entropy = max(0.0, 1.0 - 0.3 * t)
        
        steps.append(t)
        state_vals.append(engine.state.value)
        
        engine.step(stress_merge, energy, entropy)
        
        if engine.state == State.APEX:
            break
    
    # Plot state changes
    for i, state_val in enumerate(state_vals):
        color = state_colors_map[state_val]
        ax.scatter(i, state_val, s=150, color=color, edgecolors='black', linewidth=1.5, zorder=3)
    
    ax.plot(steps, state_vals, 'k--', alpha=0.2, linewidth=1, zorder=1)
    
    ax.set_xlabel('Time Step', fontsize=11, fontweight='bold')
    ax.set_ylabel('State', fontsize=11, fontweight='bold')
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['MERGE', 'REPLICATE', 'DIVIDE', 'ABSOLUTE_ZERO', 'APEX'])
    ax.set_title('Standard Evolution: State Progression', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim([0.5, 5.5])
    
    # Scenario B: With escape route
    ax = axes[1]
    config_escape = PhoenixConfig(allow_apex_escape=True)
    engine_escape = Phoenix(config=config_escape)
    steps_e, state_vals_e = [], []
    
    for t in range(20):
        stress_merge = False
        energy = 0.5 - 0.1 * t
        entropy = abs(1.0 - 0.3 * t) if t < 5 else 0.5 + 0.2 * (t - 5)
        entropy = min(entropy, 2.0)
        
        steps_e.append(t)
        state_vals_e.append(engine_escape.state.value)
        
        engine_escape.step(stress_merge, energy, entropy)
    
    # Plot state changes with different colors for escapes
    for i, state_val in enumerate(state_vals_e):
        color = state_colors_map[state_val]
        marker = 'o' if i < len(state_vals_e) - 1 else 's'  # Square for final state
        ax.scatter(i, state_val, s=150, color=color, marker=marker, 
                  edgecolors='black', linewidth=1.5, zorder=3)
    
    ax.plot(steps_e, state_vals_e, 'k--', alpha=0.2, linewidth=1, zorder=1)
    
    ax.set_xlabel('Time Step', fontsize=11, fontweight='bold')
    ax.set_ylabel('State', fontsize=11, fontweight='bold')
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['MERGE', 'REPLICATE', 'DIVIDE', 'ABSOLUTE_ZERO', 'APEX'])
    ax.set_title('With Escape Route: Oscillating Behavior', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim([0.5, 5.5])
    
    plt.suptitle('Quantum Phoenix Engine - State Timeline Comparison', 
                fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    return fig


def plot_system_dynamics():
    """
    Advanced plot showing stress, energy, entropy, and state together.
    """
    fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)
    
    engine = Phoenix()
    times, stresses, energies, entropies, states = [], [], [], [], []
    
    for t in range(20):
        stress_merge = (t < 2)
        energy = 1.0 - 0.2 * t
        entropy = max(0.0, 1.0 - 0.3 * t)
        
        times.append(t)
        stresses.append(1 if stress_merge else 0)
        energies.append(energy)
        entropies.append(entropy)
        states.append(engine.state.value)
        
        engine.step(stress_merge, energy, entropy)
        
        if engine.state == State.APEX:
            break
    
    # Plot 1: Stress
    ax = axes[0]
    ax.fill_between(times, stresses, alpha=0.3, color='#e74c3c', step='mid')
    ax.plot(times, stresses, 'o-', color='#e74c3c', linewidth=2, markersize=5, label='Stress')
    ax.set_ylabel('Stress Merge', fontsize=11, fontweight='bold')
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Low', 'High'])
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(loc='upper right', fontsize=10)
    
    # Plot 2: Energy
    ax = axes[1]
    ax.plot(times, energies, 's-', color='#3498db', linewidth=2.5, markersize=6, label='Energy')
    ax.axhline(y=0, color='#2c3e50', linestyle='--', linewidth=1.5, alpha=0.6)
    ax.fill_between(times, energies, 0, alpha=0.2, color='#3498db')
    ax.set_ylabel('Energy Level', fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=10)
    
    # Plot 3: Entropy
    ax = axes[2]
    ax.plot(times, entropies, '^-', color='#9b59b6', linewidth=2.5, markersize=6, label='Entropy')
    ax.axhline(y=0.1, color='#e74c3c', linestyle='--', linewidth=1.5, alpha=0.6, label='Transition Threshold')
    ax.fill_between(times, entropies, 0, alpha=0.2, color='#9b59b6')
    ax.set_ylabel('Entropy Level', fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=10)
    
    # Plot 4: State
    state_names = {1: 'MERGE', 2: 'REPLICATE', 3: 'DIVIDE', 4: 'ABSOLUTE_ZERO', 5: 'APEX'}
    state_colors = {1: '#3498db', 2: '#2ecc71', 3: '#e74c3c', 4: '#9b59b6', 5: '#f39c12'}
    
    ax = axes[3]
    for i, (t, state) in enumerate(zip(times, states)):
        color = state_colors[state]
        ax.scatter(t, state, s=200, color=color, edgecolors='black', linewidth=1.5, zorder=3)
    
    ax.set_ylabel('State', fontsize=11, fontweight='bold')
    ax.set_xlabel('Time Step', fontsize=11, fontweight='bold')
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['MERGE', 'REPLICATE', 'DIVIDE', 'ABSOLUTE_ZERO', 'APEX'])
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim([0.5, 5.5])
    
    plt.suptitle('Quantum Phoenix Engine - Complete System Dynamics', 
                fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    return fig


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("Generating Quantum Phoenix Engine Visualizations...\n")
    
    # Generate all plots
    print("1. Creating State Transition Diagram...")
    fig1 = plot_state_diagram()
    fig1.savefig('phoenix_state_diagram.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved: phoenix_state_diagram.png")
    
    print("2. Creating Entropy & Energy Curves...")
    fig2 = plot_entropy_curves()
    fig2.savefig('phoenix_entropy_curves.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved: phoenix_entropy_curves.png")
    
    print("3. Creating State Timeline Comparison...")
    fig3 = plot_state_timeline()
    fig3.savefig('phoenix_state_timeline.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved: phoenix_state_timeline.png")
    
    print("4. Creating System Dynamics Plot...")
    fig4 = plot_system_dynamics()
    fig4.savefig('phoenix_system_dynamics.png', dpi=300, bbox_inches='tight')
    print("   ✓ Saved: phoenix_system_dynamics.png")
    
    print("\n" + "="*60)
    print("All visualizations generated successfully!")
    print("="*60)
    print("\nGenerated files:")
    print("  • phoenix_state_diagram.png - State transition diagram")
    print("  • phoenix_entropy_curves.png - Entropy dynamics (4 scenarios)")
    print("  • phoenix_state_timeline.png - State progression comparison")
    print("  • phoenix_system_dynamics.png - Complete system behavior")
    
    plt.show()
