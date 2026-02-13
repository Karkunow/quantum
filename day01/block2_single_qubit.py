"""
Day 1 - Block 2: Single Qubit From Pure Math
=============================================

This module covers:
- Qubit as normalized vector in ℂ²
- Global phase irrelevance
- Bloch sphere parameterization
- Implementing quantum gates as matrices
- Computing measurement probabilities
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# =============================================================================
# FUNDAMENTAL CONCEPTS
# =============================================================================

"""
A QUBIT is the fundamental unit of quantum information.

Mathematically, a qubit is a unit vector in ℂ² (2D complex Hilbert space):

|ψ⟩ = α|0⟩ + β|1⟩

where:
- |0⟩ = [1, 0]ᵀ  (computational basis state "zero")
- |1⟩ = [0, 1]ᵀ  (computational basis state "one")
- α, β ∈ ℂ (complex amplitudes)
- |α|² + |β|² = 1 (normalization constraint)

KEY DIFFERENCES FROM CLASSICAL BITS:
1. A classical bit is either 0 OR 1
2. A qubit can be in SUPERPOSITION: both 0 AND 1 simultaneously
3. The amplitudes α, β are COMPLEX (have phase!)
4. Measurement COLLAPSES the state probabilistically
"""

# Computational basis states
KET_0 = np.array([1, 0], dtype=complex)
KET_1 = np.array([0, 1], dtype=complex)


# =============================================================================
# QUANTUM GATES AS MATRICES
# =============================================================================

# Pauli matrices
PAULI_X = np.array([[0, 1], 
                    [1, 0]], dtype=complex)

PAULI_Y = np.array([[0, -1j], 
                    [1j, 0]], dtype=complex)

PAULI_Z = np.array([[1, 0], 
                    [0, -1]], dtype=complex)

# Hadamard gate
HADAMARD = (1/np.sqrt(2)) * np.array([[1, 1], 
                                       [1, -1]], dtype=complex)

# Identity
IDENTITY = np.array([[1, 0], 
                     [0, 1]], dtype=complex)


def create_qubit(alpha: complex, beta: complex) -> np.ndarray:
    """
    Create a qubit state |ψ⟩ = α|0⟩ + β|1⟩.
    
    Automatically normalizes the state.
    """
    state = np.array([alpha, beta], dtype=complex)
    norm = np.linalg.norm(state)
    if norm == 0:
        raise ValueError("Cannot create zero-norm state")
    return state / norm


def apply_gate(gate: np.ndarray, state: np.ndarray) -> np.ndarray:
    """
    Apply a quantum gate (unitary matrix) to a qubit state.
    
    Quantum evolution: |ψ'⟩ = U|ψ⟩
    """
    return gate @ state


def measurement_probabilities(state: np.ndarray) -> dict:
    """
    Calculate probabilities of measuring |0⟩ and |1⟩.
    
    Born Rule: P(outcome) = |amplitude|²
    
    This is THE fundamental connection between quantum amplitudes
    and observable classical outcomes.
    """
    prob_0 = np.abs(state[0])**2
    prob_1 = np.abs(state[1])**2
    return {'P(0)': prob_0, 'P(1)': prob_1}


# =============================================================================
# BLOCH SPHERE REPRESENTATION
# =============================================================================

"""
BLOCH SPHERE: A beautiful geometric representation of single qubit states.

Any pure single-qubit state can be written as:
|ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩

Where:
- θ ∈ [0, π]  (polar angle from +Z axis)
- φ ∈ [0, 2π) (azimuthal angle in XY plane)

This maps to a point on the unit sphere:
- |0⟩ → North pole (0, 0, 1)
- |1⟩ → South pole (0, 0, -1)
- |+⟩ = (|0⟩+|1⟩)/√2 → +X axis (1, 0, 0)
- |-⟩ = (|0⟩-|1⟩)/√2 → -X axis (-1, 0, 0)
- |+i⟩ = (|0⟩+i|1⟩)/√2 → +Y axis (0, 1, 0)
- |-i⟩ = (|0⟩-i|1⟩)/√2 → -Y axis (0, -1, 0)

Why this works:
- Global phase doesn't matter: e^(iγ)|ψ⟩ is same state as |ψ⟩
- Normalization uses up one degree of freedom
- So 2 complex numbers (4 real) → 2 real parameters (θ, φ)
"""


def state_to_bloch(state: np.ndarray) -> tuple:
    """
    Convert qubit state to Bloch sphere coordinates (x, y, z).
    
    The Bloch vector components are expectation values of Pauli matrices:
    x = ⟨ψ|X|ψ⟩
    y = ⟨ψ|Y|ψ⟩  
    z = ⟨ψ|Z|ψ⟩
    """
    # Expectation values
    x = np.real(np.conj(state) @ PAULI_X @ state)
    y = np.real(np.conj(state) @ PAULI_Y @ state)
    z = np.real(np.conj(state) @ PAULI_Z @ state)
    return (x, y, z)


def bloch_to_state(theta: float, phi: float) -> np.ndarray:
    """
    Convert Bloch sphere angles to qubit state.
    
    |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩
    """
    alpha = np.cos(theta / 2)
    beta = np.exp(1j * phi) * np.sin(theta / 2)
    return np.array([alpha, beta], dtype=complex)


def plot_bloch_sphere(states: list, labels: list = None):
    """
    Visualize qubit states on the Bloch sphere.
    """
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Draw sphere wireframe
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_wireframe(x, y, z, alpha=0.1, color='gray')
    
    # Draw axes
    ax.quiver(0, 0, 0, 1.3, 0, 0, color='red', alpha=0.5, arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 1.3, 0, color='green', alpha=0.5, arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 0, 1.3, color='blue', alpha=0.5, arrow_length_ratio=0.1)
    ax.text(1.4, 0, 0, 'X', fontsize=12)
    ax.text(0, 1.4, 0, 'Y', fontsize=12)
    ax.text(0, 0, 1.4, 'Z', fontsize=12)
    
    # Mark basis states
    ax.scatter([0], [0], [1], color='blue', s=100, marker='^')
    ax.text(0.1, 0, 1.1, '|0⟩', fontsize=10)
    ax.scatter([0], [0], [-1], color='blue', s=100, marker='v')
    ax.text(0.1, 0, -1.1, '|1⟩', fontsize=10)
    
    # Plot input states
    colors = plt.cm.viridis(np.linspace(0, 1, len(states)))
    for i, state in enumerate(states):
        coords = state_to_bloch(state)
        ax.scatter(*coords, color=colors[i], s=200, marker='o')
        ax.quiver(0, 0, 0, *coords, color=colors[i], alpha=0.8, arrow_length_ratio=0.1)
        if labels:
            ax.text(coords[0]*1.1, coords[1]*1.1, coords[2]*1.1, labels[i], fontsize=10)
    
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([-1.5, 1.5])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Bloch Sphere Representation')
    
    plt.tight_layout()
    return fig


# =============================================================================
# GLOBAL PHASE IRRELEVANCE
# =============================================================================

"""
GLOBAL PHASE IRRELEVANCE

Two states that differ only by a global phase are physically identical:
e^(iγ)|ψ⟩ and |ψ⟩ give the same measurement outcomes.

Why? Measurement probabilities:
P = |⟨φ|ψ⟩|² = |⟨φ|e^(iγ)|ψ⟩|² = |e^(iγ)|²|⟨φ|ψ⟩|² = |⟨φ|ψ⟩|²

The phase e^(iγ) has magnitude 1, so it disappears!

RELATIVE phase between components DOES matter:
|ψ₁⟩ = (|0⟩ + |1⟩)/√2
|ψ₂⟩ = (|0⟩ - |1⟩)/√2

These are DIFFERENT states (opposite points on Bloch sphere X-axis).
"""


def demonstrate_global_phase():
    """Show that global phase doesn't affect measurements."""
    
    # Original state: |+⟩
    plus_state = (KET_0 + KET_1) / np.sqrt(2)
    
    # Same state with global phase e^(iπ/4)
    phase = np.exp(1j * np.pi / 4)
    plus_with_phase = phase * plus_state
    
    print("Global Phase Irrelevance Demo")
    print("=" * 40)
    print(f"|+⟩ = {plus_state}")
    print(f"e^(iπ/4)|+⟩ = {plus_with_phase}")
    print()
    print(f"Probabilities for |+⟩: {measurement_probabilities(plus_state)}")
    print(f"Probabilities for e^(iπ/4)|+⟩: {measurement_probabilities(plus_with_phase)}")
    print()
    print(f"Bloch coords for |+⟩: {state_to_bloch(plus_state)}")
    print(f"Bloch coords for e^(iπ/4)|+⟩: {state_to_bloch(plus_with_phase)}")
    print()
    print("→ Same measurement probabilities!")
    print("→ Same Bloch sphere position!")
    print("→ They represent the SAME physical state.")


# =============================================================================
# EXERCISES
# =============================================================================

def run_exercises():
    """Interactive exercises for Block 2."""
    
    print("=" * 60)
    print("BLOCK 2 EXERCISES: Single Qubit Operations")
    print("=" * 60)
    
    # Exercise 1: Apply X gate to |0⟩
    print("\n📝 Exercise 1: Pauli-X Gate")
    print("   X|0⟩ should give |1⟩")
    result_1 = apply_gate(PAULI_X, KET_0)
    print(f"   X|0⟩ = {result_1}")
    print(f"   Expected: {KET_1}")
    print(f"   ✅ Correct!" if np.allclose(result_1, KET_1) else "   ❌ Check again")
    
    # Exercise 2: Apply H gate to |0⟩
    print("\n📝 Exercise 2: Hadamard Gate")
    print("   H|0⟩ should give |+⟩ = (|0⟩ + |1⟩)/√2")
    result_2 = apply_gate(HADAMARD, KET_0)
    expected_plus = (KET_0 + KET_1) / np.sqrt(2)
    print(f"   H|0⟩ = {result_2}")
    print(f"   Probabilities: {measurement_probabilities(result_2)}")
    print(f"   ✅ Correct!" if np.allclose(result_2, expected_plus) else "   ❌ Check again")
    
    # Exercise 3: Apply H twice
    print("\n📝 Exercise 3: H² = I")
    print("   Applying H twice should return to original state")
    result_3 = apply_gate(HADAMARD, apply_gate(HADAMARD, KET_0))
    print(f"   HH|0⟩ = {result_3}")
    print(f"   ✅ Correct!" if np.allclose(result_3, KET_0) else "   ❌ Check again")
    
    # Exercise 4: Z gate on |+⟩
    print("\n📝 Exercise 4: Pauli-Z on superposition")
    print("   Z|+⟩ should give |-⟩ = (|0⟩ - |1⟩)/√2")
    plus = (KET_0 + KET_1) / np.sqrt(2)
    result_4 = apply_gate(PAULI_Z, plus)
    expected_minus = (KET_0 - KET_1) / np.sqrt(2)
    print(f"   Z|+⟩ = {result_4}")
    print(f"   ✅ Correct!" if np.allclose(result_4, expected_minus) else "   ❌ Check again")
    
    # Exercise 5: Bloch sphere positions
    print("\n📝 Exercise 5: Bloch Sphere Positions")
    states = [KET_0, KET_1, plus, expected_minus]
    labels = ['|0⟩', '|1⟩', '|+⟩', '|-⟩']
    for state, label in zip(states, labels):
        coords = state_to_bloch(state)
        print(f"   {label}: ({coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f})")
    
    print("\n" + "=" * 60)
    print("Exercises Complete!")
    print("=" * 60)
    
    return states, labels


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("DAY 1 - BLOCK 2: SINGLE QUBIT MECHANICS")
    print("=" * 60)
    
    # Run exercises
    states, labels = run_exercises()
    
    # Demonstrate global phase
    print("\n")
    demonstrate_global_phase()
    
    # Generate Bloch sphere visualization
    print("\n\n📊 Generating Bloch Sphere Visualization...")
    fig = plot_bloch_sphere(states, labels)
    plt.savefig('day01/bloch_sphere.png', dpi=150, bbox_inches='tight')
    print("   Saved to: day01/bloch_sphere.png")
    plt.close()
