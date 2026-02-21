"""
Day 5 Solutions: Noise & Reality (NISQ Era)
============================================

14-Day Quantum DevRel Bootcamp

Complete implementations with interview insights.
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import (
    Statevector, DensityMatrix, Operator,
    partial_trace, state_fidelity
)
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error


# Standard matrices
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


# ============================================================
# Exercise 1: Density Matrices — Pure vs Mixed States
# ============================================================
# 💬 Interview insight: "Density matrices are the language of
# open quantum systems. Pure states (ρ = |ψ⟩⟨ψ|) are an idealisation —
# real qubits are always in mixed states due to noise. The purity
# Tr(ρ²) tells you how close to ideal your qubit is."

STATE_VECTORS = {
    '0': np.array([1, 0], dtype=complex),
    '1': np.array([0, 1], dtype=complex),
    '+': np.array([1, 1], dtype=complex) / np.sqrt(2),
    '-': np.array([1, -1], dtype=complex) / np.sqrt(2),
    '+i': np.array([1, 1j], dtype=complex) / np.sqrt(2),
    '-i': np.array([1, -1j], dtype=complex) / np.sqrt(2),
}


def pure_state_dm(state_label: str) -> np.ndarray:
    """ρ = |ψ⟩⟨ψ| — outer product of state vector with itself."""
    psi = STATE_VECTORS[state_label]
    return np.outer(psi, psi.conj())


def mixed_state_dm(states: list[str], probs: list[float]) -> np.ndarray:
    """ρ = Σ pᵢ |ψᵢ⟩⟨ψᵢ| — classical probabilistic mixture.

    💬 "A mixed state is NOT a superposition. It's classical
    ignorance — we don't know which pure state was prepared.
    The density matrix encodes this uncertainty. A 50/50 mixture
    of |0⟩ and |1⟩ gives I/2, which is identical to a 50/50
    mixture of |+⟩ and |−⟩. You can't tell which mixture
    produced a given density matrix — that's a key difference
    from the classical world."
    """
    rho = np.zeros((2, 2), dtype=complex)
    for state, p in zip(states, probs):
        rho += p * pure_state_dm(state)
    return rho


def purity(rho: np.ndarray) -> float:
    """Tr(ρ²) — measures how pure/mixed a state is.

    💬 "Purity is the simplest entanglement witness for bipartite
    states. If Tr(ρ_A²) < 1, the system is entangled. For noise
    analysis, purity tells you how much information has leaked
    to the environment."
    """
    return float(np.real(np.trace(rho @ rho)))


# ============================================================
# Exercise 2: Kraus Operator Noise Channels
# ============================================================
# 💬 Interview insight: "Kraus operators are the 'matrix mechanics'
# of noise. Every physical noise process — decoherence, gate errors,
# measurement errors — can be written as ε(ρ) = Σ Kᵢ ρ Kᵢ†.
# The completeness relation Σ Kᵢ†Kᵢ = I ensures trace preservation
# (probabilities still sum to 1 after noise)."

def apply_channel(rho: np.ndarray, kraus_ops: list[np.ndarray]) -> np.ndarray:
    """ε(ρ) = Σ Kᵢ ρ Kᵢ† — the general quantum channel formula."""
    result = np.zeros_like(rho)
    for K in kraus_ops:
        result += K @ rho @ K.conj().T
    return result


def bit_flip_channel(p: float) -> list[np.ndarray]:
    """Bit-flip: with probability p, apply X.

    Models classical bit errors. On a Bloch sphere, this
    contracts the Z axis (coherence in computational basis).
    """
    K0 = np.sqrt(1 - p) * I2
    K1 = np.sqrt(p) * X
    return [K0, K1]


def phase_flip_channel(p: float) -> list[np.ndarray]:
    """Phase-flip: with probability p, apply Z.

    Models dephasing (T2 decay without energy loss).
    On a Bloch sphere, this contracts the X-Y plane.
    """
    K0 = np.sqrt(1 - p) * I2
    K1 = np.sqrt(p) * Z
    return [K0, K1]


def depolarizing_channel(p: float) -> list[np.ndarray]:
    """Depolarizing: with probability p, replace with I/2.

    The 'worst-case' noise — equally likely to apply any Pauli error.
    On a Bloch sphere, this shrinks the Bloch vector uniformly
    toward the origin: r → (1-p) r.

    💬 "Depolarizing noise is the standard benchmark model because
    it's the most symmetric. Real noise is usually biased (more
    Z errors than X errors), but depolarizing gives you the
    worst-case analysis."
    """
    K0 = np.sqrt(1 - 3 * p / 4) * I2
    K1 = np.sqrt(p / 4) * X
    K2 = np.sqrt(p / 4) * Y
    K3 = np.sqrt(p / 4) * Z
    return [K0, K1, K2, K3]


def amplitude_damping_channel(gamma: float) -> list[np.ndarray]:
    """Amplitude damping: |1⟩ → |0⟩ with probability γ.

    Models T1 relaxation — spontaneous emission of energy.
    This is the dominant decoherence mechanism on superconducting
    qubits.

    💬 "T1 decay is like a light bulb slowly losing energy. The
    qubit in |1⟩ (excited state) spontaneously drops to |0⟩
    (ground state) by emitting a photon. The decay rate is
    γ = 1 - e^(-t/T1) where T1 is the energy relaxation time.
    IBM Eagle processors have T1 ≈ 100-300μs."
    """
    K0 = np.array([[1, 0], [0, np.sqrt(1 - gamma)]], dtype=complex)
    K1 = np.array([[0, np.sqrt(gamma)], [0, 0]], dtype=complex)
    return [K0, K1]


# ============================================================
# Bonus: Phase Damping Channel
# ============================================================

def phase_damping_channel(lam: float) -> list[np.ndarray]:
    """Phase damping: models T2 dephasing (pure dephasing).

    Unlike phase flip, this is a continuous process.
    Off-diagonal elements of ρ decay: ρ₀₁ → √(1-λ) ρ₀₁

    💬 "Phase damping (T2 decay) is loss of quantum coherence
    without energy loss. Physically, it's caused by fluctuating
    magnetic fields that randomly shift the qubit's frequency.
    T2 ≤ 2·T1 always. When T2 < 2·T1, there's 'pure dephasing'
    on top of T1 relaxation."
    """
    K0 = np.array([[1, 0], [0, np.sqrt(1 - lam)]], dtype=complex)
    K1 = np.array([[0, 0], [0, np.sqrt(lam)]], dtype=complex)
    return [K0, K1]


# ============================================================
# Exercise 3: Noise Effects on Quantum States
# ============================================================

def noisy_superposition(p: float) -> np.ndarray:
    """Apply depolarizing noise to |+⟩."""
    rho = pure_state_dm('+')
    kraus = depolarizing_channel(p)
    return apply_channel(rho, kraus)


def t1_decay(gamma: float) -> np.ndarray:
    """Apply amplitude damping to |1⟩."""
    rho = pure_state_dm('1')
    kraus = amplitude_damping_channel(gamma)
    return apply_channel(rho, kraus)


# ============================================================
# Exercise 4: Qiskit Aer Noise Models
# ============================================================
# 💬 Interview insight: "Qiskit Aer noise models let you simulate
# realistic hardware. IBM publishes calibration data for all their
# processors — you can build device-specific noise models to predict
# how your circuit will perform before running on real hardware.
# This is essential for error mitigation development."

def build_simple_noise_model(
    single_gate_error: float = 0.001,
    two_gate_error: float = 0.01,
) -> NoiseModel:
    """Build a depolarizing noise model."""
    noise_model = NoiseModel()

    # Single-qubit depolarizing error
    error_1q = depolarizing_error(single_gate_error, 1)
    noise_model.add_all_qubit_quantum_error(error_1q, ['u', 'sx', 'x', 'h', 'rz', 'ry', 's', 't'])

    # Two-qubit depolarizing error
    error_2q = depolarizing_error(two_gate_error, 2)
    noise_model.add_all_qubit_quantum_error(error_2q, ['cx', 'cz'])

    return noise_model


def simulate_with_noise(
    qc: QuantumCircuit,
    noise_model: NoiseModel,
    shots: int = 4096
) -> dict:
    """Simulate with noise."""
    sim = AerSimulator(noise_model=noise_model)
    result = sim.run(qc, shots=shots).result()
    return result.get_counts()


# ============================================================
# Exercise 5: Ideal vs Noisy Comparison
# ============================================================
# 💬 Interview insight: "The gap between ideal and noisy results
# is the central challenge of NISQ computing. For a circuit with
# depth d and 2-qubit error rate ε, the fidelity scales roughly
# as (1-ε)^d — exponential decay! This limits useful circuit
# depth to about 1/ε gates before noise dominates."

def compare_bell_state(
    single_error: float = 0.001,
    two_error: float = 0.01,
    shots: int = 4096
) -> tuple[dict, dict]:
    """Compare ideal vs noisy Bell state."""
    # Build circuit
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    # Ideal
    sim_ideal = AerSimulator()
    ideal_counts = sim_ideal.run(qc, shots=shots).result().get_counts()

    # Noisy
    noise_model = build_simple_noise_model(single_error, two_error)
    sim_noisy = AerSimulator(noise_model=noise_model)
    noisy_counts = sim_noisy.run(qc, shots=shots).result().get_counts()

    return ideal_counts, noisy_counts


def calculate_fidelity_vs_noise(
    noise_levels: list[float],
    shots: int = 8192
) -> list[float]:
    """Fidelity proxy (correct outcome probability) vs noise level."""
    fidelities = []
    for p in noise_levels:
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        noise_model = build_simple_noise_model(0.001, p)
        sim = AerSimulator(noise_model=noise_model)
        counts = sim.run(qc, shots=shots).result().get_counts()

        # Correct outcomes for Bell state: |00⟩ and |11⟩
        correct = counts.get('00', 0) + counts.get('11', 0)
        fidelities.append(correct / shots)

    return fidelities


# ============================================================
# Bonus: Bloch Sphere Noise Visualisation Data
# ============================================================

def bloch_under_noise(channel_fn, param_values, initial_state='+'
                      ) -> list[tuple[float, float, float]]:
    """Track a state's Bloch vector as noise strength increases.

    Returns list of (x, y, z) Bloch coordinates.

    💬 "Different noise channels shrink the Bloch sphere in
    different ways:
    - Depolarizing: uniform shrinkage (sphere → point)
    - Amplitude damping: shrinkage + drift toward |0⟩
    - Phase damping: X-Y plane shrinkage (disk → line)
    - Bit flip: Z axis shrinkage"
    """
    PAULI = [X, Y, Z]
    coords = []
    for p in param_values:
        rho = pure_state_dm(initial_state)
        kraus = channel_fn(p)
        rho_noisy = apply_channel(rho, kraus)
        xyz = tuple(float(np.real(np.trace(rho_noisy @ P))) for P in PAULI)
        coords.append(xyz)
    return coords


if __name__ == "__main__":
    print("Day 5 Solutions: Noise & Reality")
    print("=" * 55)

    # Demo: noise effects
    print("\nNoise Effects on |+⟩:")
    for p in [0.0, 0.1, 0.5, 1.0]:
        rho = noisy_superposition(p)
        pur = purity(rho)
        print(f"  p={p:.1f}: purity = {pur:.4f}")

    print("\nT1 Decay of |1⟩:")
    for g in [0.0, 0.1, 0.5, 1.0]:
        rho = t1_decay(g)
        p0 = rho[0, 0].real
        p1 = rho[1, 1].real
        print(f"  γ={g:.1f}: P(|0⟩)={p0:.3f}, P(|1⟩)={p1:.3f}")

    print("\nIdeal vs Noisy Bell State:")
    ideal, noisy = compare_bell_state(0.001, 0.05)
    print(f"  Ideal: {ideal}")
    print(f"  Noisy: {noisy}")

    print("\nFidelity vs Noise Level:")
    levels = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5]
    fids = calculate_fidelity_vs_noise(levels)
    for p, f in zip(levels, fids):
        print(f"  2Q error = {p:.2f}: fidelity = {f:.4f}")
