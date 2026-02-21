"""
Day 5 Exercises: Noise & Reality (NISQ Era)
============================================

14-Day Quantum DevRel Bootcamp

Today's exercises cover:
1. Density matrices and mixed states
2. Kraus operator noise channels
3. Depolarizing, amplitude damping, phase damping
4. Qiskit Aer noise models
5. Ideal vs noisy circuit comparison

Run this file to test your implementations:
    python day05/exercises.py
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import (
    Statevector, DensityMatrix, Operator,
    partial_trace, state_fidelity
)
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error


# ============================================================
# Exercise 1: Density Matrices — Pure vs Mixed States
# ============================================================
# A density matrix ρ generalises the state vector:
#   Pure state |ψ⟩  →  ρ = |ψ⟩⟨ψ|        (rank 1, Tr(ρ²) = 1)
#   Mixed state      →  ρ = Σ pᵢ|ψᵢ⟩⟨ψᵢ| (rank > 1, Tr(ρ²) < 1)
#
# Mixed states arise from:
#   1. Classical ignorance (we don't know which state was prepared)
#   2. Entanglement (partial trace of entangled state)
#   3. Noise (interaction with environment)

def pure_state_dm(state_label: str) -> np.ndarray:
    """Build the density matrix for a pure state.

    Args:
        state_label: One of '0', '1', '+', '-', '+i', '-i'

    Returns:
        2×2 density matrix as numpy array

    Example:
        |0⟩ → |0⟩⟨0| = [[1, 0], [0, 0]]
        |+⟩ → |+⟩⟨+| = [[0.5, 0.5], [0.5, 0.5]]
    """
    # TODO: Build the state vector for the given label
    # TODO: Return the outer product |ψ⟩⟨ψ|
    pass


def mixed_state_dm(states: list[str], probs: list[float]) -> np.ndarray:
    """Build a density matrix for a classical mixture of pure states.

    ρ = Σ pᵢ |ψᵢ⟩⟨ψᵢ|

    Args:
        states: List of state labels (e.g. ['0', '1'])
        probs: List of probabilities (must sum to 1)

    Returns:
        2×2 density matrix as numpy array

    Example:
        50/50 mixture of |0⟩ and |1⟩ → [[0.5, 0], [0, 0.5]] = I/2
    """
    # TODO: Sum pᵢ * pure_state_dm(sᵢ) for each state
    pass


def purity(rho: np.ndarray) -> float:
    """Calculate the purity Tr(ρ²) of a density matrix.

    Purity = 1   → pure state
    Purity = 1/d → maximally mixed (d = dimension)

    Args:
        rho: Density matrix

    Returns:
        Purity value between 1/d and 1
    """
    # TODO: Return Tr(ρ²)
    pass


# ============================================================
# Exercise 2: Kraus Operator Noise Channels
# ============================================================
# A quantum channel ε maps density matrices to density matrices:
#   ε(ρ) = Σ Kᵢ ρ Kᵢ†
#
# where {Kᵢ} are Kraus operators satisfying Σ Kᵢ†Kᵢ = I
#
# This is the most general form of quantum noise.

def apply_channel(rho: np.ndarray, kraus_ops: list[np.ndarray]) -> np.ndarray:
    """Apply a quantum channel defined by Kraus operators.

    ε(ρ) = Σ Kᵢ ρ Kᵢ†

    Args:
        rho: Input density matrix
        kraus_ops: List of Kraus operator matrices

    Returns:
        Output density matrix after the channel
    """
    # TODO: Sum Kᵢ @ ρ @ Kᵢ† for each Kraus operator
    pass


def bit_flip_channel(p: float) -> list[np.ndarray]:
    """Return Kraus operators for the bit-flip channel.

    With probability p, apply X (bit flip).
    With probability 1-p, do nothing.

    K₀ = √(1-p) · I
    K₁ = √p · X

    Args:
        p: Probability of bit flip (0 to 1)

    Returns:
        List of two 2×2 Kraus operator matrices
    """
    # TODO: Build and return [K₀, K₁]
    pass


def phase_flip_channel(p: float) -> list[np.ndarray]:
    """Return Kraus operators for the phase-flip channel.

    With probability p, apply Z (phase flip).
    With probability 1-p, do nothing.

    K₀ = √(1-p) · I
    K₁ = √p · Z

    Args:
        p: Probability of phase flip (0 to 1)

    Returns:
        List of two 2×2 Kraus operator matrices
    """
    # TODO: Build and return [K₀, K₁]
    pass


def depolarizing_channel(p: float) -> list[np.ndarray]:
    """Return Kraus operators for the depolarizing channel.

    With probability p, replace state with I/2 (maximally mixed).
    With probability 1-p, do nothing.

    Equivalent to: apply I, X, Y, Z each with specific probabilities.

    K₀ = √(1 - 3p/4) · I
    K₁ = √(p/4) · X
    K₂ = √(p/4) · Y
    K₃ = √(p/4) · Z

    Args:
        p: Depolarizing probability (0 to 1)

    Returns:
        List of four 2×2 Kraus operator matrices
    """
    # TODO: Build and return [K₀, K₁, K₂, K₃]
    pass


def amplitude_damping_channel(gamma: float) -> list[np.ndarray]:
    """Return Kraus operators for the amplitude damping channel.

    Models energy relaxation (T1 decay): |1⟩ → |0⟩ with probability γ.
    This is the dominant noise on superconducting qubits.

    K₀ = [[1, 0], [0, √(1-γ)]]     (no decay)
    K₁ = [[0, √γ], [0, 0]]          (decay |1⟩ → |0⟩)

    Args:
        gamma: Decay probability (0 to 1)

    Returns:
        List of two 2×2 Kraus operator matrices
    """
    # TODO: Build and return [K₀, K₁]
    pass


# ============================================================
# Exercise 3: Noise Effects on Quantum States
# ============================================================
# Apply noise channels to specific states and observe the effects.

def noisy_superposition(p: float) -> np.ndarray:
    """Apply depolarizing noise to |+⟩ and return the result.

    Steps:
    1. Build the density matrix for |+⟩
    2. Apply depolarizing channel with parameter p
    3. Return the resulting density matrix

    Args:
        p: Depolarizing probability

    Returns:
        2×2 density matrix after noise
    """
    # TODO: Implement
    pass


def t1_decay(gamma: float) -> np.ndarray:
    """Apply amplitude damping to |1⟩ and return the result.

    This models T1 relaxation: excited state |1⟩ decays toward |0⟩.

    Args:
        gamma: Decay probability (related to time as γ = 1 - e^(-t/T1))

    Returns:
        2×2 density matrix after decay
    """
    # TODO: Implement
    pass


# ============================================================
# Exercise 4: Qiskit Aer Noise Models
# ============================================================
# Build noise models and simulate circuits with realistic noise.

def build_simple_noise_model(
    single_gate_error: float = 0.001,
    two_gate_error: float = 0.01,
) -> NoiseModel:
    """Build a simple noise model with depolarizing errors.

    Add depolarizing errors:
    - single_gate_error on all 1-qubit gates
    - two_gate_error on all 2-qubit gates

    Args:
        single_gate_error: Error rate for single-qubit gates
        two_gate_error: Error rate for two-qubit gates

    Returns:
        Qiskit NoiseModel
    """
    # TODO: Create NoiseModel
    # TODO: Add depolarizing_error for 1-qubit gates (applied to ['u', 'sx', 'x', 'h', 'rz'])
    # TODO: Add depolarizing_error for 2-qubit gates (applied to ['cx'])
    # TODO: Return the noise model
    pass


def simulate_with_noise(
    qc: QuantumCircuit,
    noise_model: NoiseModel,
    shots: int = 4096
) -> dict:
    """Simulate a circuit with a noise model and return counts.

    Args:
        qc: Quantum circuit with measurements
        noise_model: Qiskit NoiseModel to apply
        shots: Number of measurement repetitions

    Returns:
        Measurement counts dictionary
    """
    # TODO: Create AerSimulator with noise_model
    # TODO: Run the circuit and return counts
    pass


# ============================================================
# Exercise 5: Ideal vs Noisy Comparison
# ============================================================
# Compare ideal and noisy results for a Bell state circuit.

def compare_bell_state(
    single_error: float = 0.001,
    two_error: float = 0.01,
    shots: int = 4096
) -> tuple[dict, dict]:
    """Compare ideal vs noisy Bell state measurements.

    Steps:
    1. Build a Bell state circuit (H + CNOT + measure)
    2. Run ideal simulation (no noise)
    3. Run noisy simulation with given error rates
    4. Return both count dictionaries

    Args:
        single_error: Single-qubit gate error rate
        two_error: Two-qubit gate error rate
        shots: Number of shots

    Returns:
        Tuple of (ideal_counts, noisy_counts)
    """
    # TODO: Build Bell circuit with measurements
    # TODO: Run ideal simulation
    # TODO: Build noise model and run noisy simulation
    # TODO: Return (ideal_counts, noisy_counts)
    pass


def calculate_fidelity_vs_noise(
    noise_levels: list[float],
    shots: int = 8192
) -> list[float]:
    """Calculate output fidelity at different noise levels.

    For each noise level p:
    1. Build a Bell state circuit with measurements
    2. Run noisy simulation (p as 2-qubit error rate)
    3. Calculate the probability of correct outcomes (|00⟩ + |11⟩)
    4. This "correct probability" is a proxy for fidelity

    Args:
        noise_levels: List of 2-qubit error rates to test
        shots: Number of shots per simulation

    Returns:
        List of fidelity values (correct outcome probability)
    """
    # TODO: For each noise level, simulate and compute fidelity
    pass


# ============================================================
# Test Suite
# ============================================================

def run_tests():
    """Run all exercise tests."""
    passed = 0
    failed = 0

    def check(name, condition):
        nonlocal passed, failed
        if condition:
            print(f"  ✅ {name}")
            passed += 1
        else:
            print(f"  ❌ {name}")
            failed += 1

    print("=" * 60)
    print("Day 5 Tests: Noise & Reality (NISQ Era)")
    print("=" * 60)

    # ── Exercise 1: Density Matrices ──
    print("\n📝 Exercise 1: Density Matrices")

    dm0 = pure_state_dm('0')
    if dm0 is not None:
        check("|0⟩ density matrix correct",
              np.allclose(dm0, np.array([[1, 0], [0, 0]])))
        check("|0⟩ is pure (Tr(ρ²) = 1)", np.isclose(purity(dm0), 1.0))
    else:
        check("pure_state_dm implemented", False)

    dm_plus = pure_state_dm('+')
    if dm_plus is not None:
        expected = np.array([[0.5, 0.5], [0.5, 0.5]])
        check("|+⟩ density matrix correct", np.allclose(dm_plus, expected))
    else:
        check("|+⟩ density matrix implemented", False)

    mixed = mixed_state_dm(['0', '1'], [0.5, 0.5])
    if mixed is not None:
        check("50/50 mixture = I/2", np.allclose(mixed, np.eye(2) / 2))
        p = purity(mixed)
        if p is not None:
            check("Mixed state purity = 0.5", np.isclose(p, 0.5))
        else:
            check("purity implemented", False)
    else:
        check("mixed_state_dm implemented", False)

    # ── Exercise 2: Kraus Operators ──
    print("\n📝 Exercise 2: Kraus Operator Channels")

    bf = bit_flip_channel(0.1)
    if bf is not None:
        # Check completeness: Σ Kᵢ†Kᵢ = I
        completeness = sum(k.conj().T @ k for k in bf)
        check("Bit-flip: completeness (Σ K†K = I)", np.allclose(completeness, np.eye(2)))
    else:
        check("bit_flip_channel implemented", False)

    pf = phase_flip_channel(0.1)
    if pf is not None:
        completeness = sum(k.conj().T @ k for k in pf)
        check("Phase-flip: completeness", np.allclose(completeness, np.eye(2)))
    else:
        check("phase_flip_channel implemented", False)

    dep = depolarizing_channel(0.1)
    if dep is not None:
        completeness = sum(k.conj().T @ k for k in dep)
        check("Depolarizing: completeness", np.allclose(completeness, np.eye(2)))
        # Depolarizing on pure state should reduce purity
        if dm_plus is not None:
            result = apply_channel(dm_plus, dep)
            if result is not None:
                check("Depolarizing reduces purity",
                      purity(result) < purity(dm_plus))
            else:
                check("apply_channel implemented", False)
    else:
        check("depolarizing_channel implemented", False)

    ad = amplitude_damping_channel(0.3)
    if ad is not None:
        completeness = sum(k.conj().T @ k for k in ad)
        check("Amplitude damping: completeness", np.allclose(completeness, np.eye(2)))
        # |1⟩ should partially decay toward |0⟩
        dm1 = pure_state_dm('1')
        if dm1 is not None:
            result = apply_channel(dm1, ad)
            if result is not None:
                check("Amp damping: |1⟩ probability decreases",
                      result[1, 1] < 1.0)
                check("Amp damping: |0⟩ probability increases",
                      result[0, 0] > 0.0)
            else:
                check("apply_channel implemented", False)
    else:
        check("amplitude_damping_channel implemented", False)

    # ── Exercise 3: Noise Effects ──
    print("\n📝 Exercise 3: Noise Effects")

    noisy_plus = noisy_superposition(0.5)
    if noisy_plus is not None:
        check("Noisy |+⟩ is valid density matrix",
              np.isclose(np.trace(noisy_plus), 1.0) and
              np.allclose(noisy_plus, noisy_plus.conj().T))
        check("Noisy |+⟩ purity < 1",
              purity(noisy_plus) < 0.999)
    else:
        check("noisy_superposition implemented", False)

    decayed = t1_decay(0.5)
    if decayed is not None:
        check("T1 decay: population shifted toward |0⟩",
              decayed[0, 0] > 0.4)
        check("T1 decay: valid density matrix",
              np.isclose(np.trace(decayed), 1.0))
    else:
        check("t1_decay implemented", False)

    # ── Exercise 4: Aer Noise Models ──
    print("\n📝 Exercise 4: Qiskit Aer Noise Models")

    noise = build_simple_noise_model(0.01, 0.05)
    if noise is not None:
        check("Noise model created", isinstance(noise, NoiseModel))
    else:
        check("build_simple_noise_model implemented", False)

    if noise is not None:
        qc = QuantumCircuit(1, 1)
        qc.x(0)
        qc.measure(0, 0)
        counts = simulate_with_noise(qc, noise, shots=2048)
        if counts is not None:
            total = sum(counts.values())
            check("Noisy simulation returns correct shots", total == 2048)
            # With noise, we should sometimes get wrong answer
            has_errors = '0' in counts
            check("Noisy X gate: some errors present", has_errors)
        else:
            check("simulate_with_noise implemented", False)

    # ── Exercise 5: Ideal vs Noisy ──
    print("\n📝 Exercise 5: Ideal vs Noisy Comparison")

    result = compare_bell_state(0.001, 0.05, 4096)
    if result is not None:
        ideal, noisy = result
        check("Ideal Bell: only |00⟩ and |11⟩",
              all(k in ['00', '11'] for k in ideal.keys()))
        # Noisy should have some |01⟩ or |10⟩
        noisy_has_errors = any(k in noisy for k in ['01', '10'])
        check("Noisy Bell: some error outcomes present", noisy_has_errors)
    else:
        check("compare_bell_state implemented", False)

    fids = calculate_fidelity_vs_noise([0.0, 0.05, 0.2, 0.5])
    if fids is not None:
        check("Fidelity decreases with noise",
              fids[0] >= fids[-1])
        check("Zero noise → ~100% fidelity",
              fids[0] > 0.95)
    else:
        check("calculate_fidelity_vs_noise implemented", False)

    # ── Summary ──
    print(f"\n{'=' * 60}")
    print(f"Results: {passed}/{passed + failed} tests passed")
    if failed == 0:
        print("🎉 All tests passed! Ready for Day 6!")
    else:
        print(f"💪 {failed} test(s) remaining. Check the TODOs above.")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
