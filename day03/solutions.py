"""
Day 3 Solutions: Multi-Qubit Systems & Entanglement
====================================================

14-Day Quantum DevRel Bootcamp

Complete implementations with explanations and interview insights.
Only check these AFTER attempting the exercises yourself!
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace


# ============================================================
# Solution 1: Build the Four Bell State Circuits
# ============================================================
#
# Interview Insight: Bell states are the "hydrogen atoms" of
# entanglement — the simplest possible entangled states.
# Every quantum networking protocol (teleportation, superdense
# coding, QKD) starts from Bell pairs.
#
# The pattern:
#   1. Optionally flip qubits with X gates to choose which Bell state
#   2. Apply H to qubit 0 (creates superposition)
#   3. Apply CNOT from qubit 0 to qubit 1 (creates entanglement)
#
# Why CNOT creates entanglement:
#   H|0⟩ = (|0⟩ + |1⟩)/√2, so after H⊗I on |00⟩:
#   (|0⟩ + |1⟩)/√2 ⊗ |0⟩ = (|00⟩ + |10⟩)/√2
#
#   CNOT flips target when control is |1⟩:
#   → (|00⟩ + |11⟩)/√2 = |Φ+⟩
#
#   The key: CNOT correlates the second qubit with the first.
#   The result CANNOT be written as |a⟩⊗|b⟩ — it's entangled!

def bell_phi_plus() -> QuantumCircuit:
    """Build |Φ+⟩ = (|00⟩ + |11⟩) / √2."""
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def bell_phi_minus() -> QuantumCircuit:
    """Build |Φ-⟩ = (|00⟩ - |11⟩) / √2."""
    qc = QuantumCircuit(2)
    qc.x(0)       # |00⟩ → |10⟩
    qc.h(0)       # → (|0⟩ - |1⟩)/√2 ⊗ |0⟩
    qc.cx(0, 1)   # → (|00⟩ - |11⟩)/√2
    return qc


def bell_psi_plus() -> QuantumCircuit:
    """Build |Ψ+⟩ = (|01⟩ + |10⟩) / √2."""
    qc = QuantumCircuit(2)
    qc.x(1)       # |00⟩ → |01⟩
    qc.h(0)       # → (|0⟩ + |1⟩)/√2 ⊗ |1⟩
    qc.cx(0, 1)   # → (|01⟩ + |10⟩)/√2
    return qc


def bell_psi_minus() -> QuantumCircuit:
    """Build |Ψ-⟩ = (|01⟩ - |10⟩) / √2."""
    qc = QuantumCircuit(2)
    qc.x(0)       # flip qubit 0
    qc.x(1)       # flip qubit 1 → |11⟩
    qc.h(0)       # → (|0⟩ - |1⟩)/√2 ⊗ |1⟩
    qc.cx(0, 1)   # → (|01⟩ - |10⟩)/√2
    return qc


# ============================================================
# Solution 2: Entanglement Verification
# ============================================================
#
# Interview Insight: The partial trace is how you mathematically
# describe "ignoring" one subsystem. If the reduced state is
# mixed, the two systems are entangled — you can't describe
# one without the other.
#
# For a maximally entangled state like |Φ+⟩:
#   ρ_A = Tr_B(|Φ+⟩⟨Φ+|) = I/2 (maximally mixed!)
#   Purity = Tr(ρ_A²) = 1/2
#
# For a separable state like |+0⟩ = |+⟩⊗|0⟩:
#   ρ_A = Tr_B(|+0⟩⟨+0|) = |+⟩⟨+| (pure!)
#   Purity = Tr(ρ_A²) = 1
#
# This connects to von Neumann entropy:
#   S(ρ_A) = -Tr(ρ_A log ρ_A)
#   S = 0 → separable, S > 0 → entangled
#   S = log(d) → maximally entangled

def is_entangled(qc: QuantumCircuit) -> bool:
    """Determine if the output state of a circuit is entangled."""
    sv = Statevector.from_instruction(qc)
    dm = DensityMatrix(sv)
    # Partial trace over qubit 1 → reduced state of qubit 0
    reduced = partial_trace(dm, [1])
    # Compute purity: Tr(ρ²)
    purity = np.real(np.trace(reduced.data @ reduced.data))
    # Pure (purity ≈ 1) → separable, Mixed (purity < 1) → entangled
    return purity < 0.999


# ============================================================
# Solution 3: GHZ and W States
# ============================================================
#
# Interview Insight: GHZ and W represent two fundamentally
# different TYPES of multi-qubit entanglement (they are not
# equivalent under local operations + classical communication).
#
# GHZ |000⟩ + |111⟩)/√2:
#   - "All or nothing" entanglement
#   - Lose one qubit → remaining two are SEPARABLE (|00⟩⟨00| + |11⟩⟨11|)/2
#   - Used in: quantum secret sharing, quantum error correction
#   - Maximally violates Mermin inequality
#
# W state (|001⟩ + |010⟩ + |100⟩)/√3:
#   - "Robust" entanglement
#   - Lose one qubit → remaining two are STILL ENTANGLED
#   - More resilient to particle loss
#   - Used in: quantum memories, leader election protocols
#
# Key concept: SLOCC (Stochastic Local Operations and Classical
# Communication) — GHZ and W are in different SLOCC classes.
# You cannot convert one to the other, even probabilistically,
# using only local operations.

def ghz_state(n: int = 3) -> QuantumCircuit:
    """Build the n-qubit GHZ state."""
    qc = QuantumCircuit(n)
    qc.h(0)
    for i in range(1, n):
        qc.cx(0, i)
    return qc


def w_state() -> QuantumCircuit:
    """Build the 3-qubit W state."""
    qc = QuantumCircuit(3)
    # Use initialize for clarity — in practice you'd decompose
    # into native gates for hardware execution
    target = np.zeros(8, dtype=complex)
    target[1] = 1 / np.sqrt(3)  # |001⟩
    target[2] = 1 / np.sqrt(3)  # |010⟩
    target[4] = 1 / np.sqrt(3)  # |100⟩
    qc.initialize(target)
    return qc


def w_state_from_gates() -> QuantumCircuit:
    """
    Build the 3-qubit W state using only elementary gates.

    Strategy:
    1. Start with |000⟩
    2. Apply Ry(2·arccos(1/√3)) to qubit 0
       → √(1/3)|1⟩ + √(2/3)|0⟩ on qubit 0
    3. Controlled distribution of the |1⟩ amplitude
    """
    qc = QuantumCircuit(3)

    # Step 1: Create unequal superposition on qubit 0
    # We want: √(1/3)|1⟩₀ + √(2/3)|0⟩₀
    theta1 = 2 * np.arccos(np.sqrt(2 / 3))
    qc.ry(theta1, 0)

    # Step 2: If qubit 0 is |0⟩, distribute between qubits 1,2
    # Controlled-Ry on qubit 1, conditioned on qubit 0 being |0⟩
    # Use X gate to flip condition
    theta2 = 2 * np.arccos(np.sqrt(1 / 2))  # = π/2
    qc.x(0)
    qc.cry(theta2, 0, 1)
    qc.x(0)

    # Step 3: CNOT cascade to move the excitation
    qc.cx(0, 2)
    qc.cx(1, 2)

    return qc


# ============================================================
# Solution 4: No-Cloning Theorem
# ============================================================
#
# Interview Insight: No-cloning is not a bug — it's a FEATURE.
# It's the foundation of quantum cryptography (QKD):
#   - Eve cannot copy quantum states being transmitted
#   - Any eavesdropping attempt disturbs the state
#   - Alice and Bob can detect this disturbance
#
# Proof sketch (by contradiction):
#   Suppose U|ψ⟩|0⟩ = |ψ⟩|ψ⟩ for all |ψ⟩.
#   Then U|0⟩|0⟩ = |0⟩|0⟩ and U|1⟩|0⟩ = |1⟩|1⟩.
#   By linearity: U|+⟩|0⟩ = (U|0⟩|0⟩ + U|1⟩|0⟩)/√2
#                           = (|00⟩ + |11⟩)/√2 = |Φ+⟩
#   But we wanted: |+⟩|+⟩ = (|00⟩+|01⟩+|10⟩+|11⟩)/2
#   These are different states → contradiction!
#
# What CNOT actually does to |+⟩|0⟩:
#   Creates ENTANGLEMENT, not a clone.
#   The result |Φ+⟩ means: measuring one qubit instantly
#   determines the other, but neither is individually in state |+⟩.

def attempt_clone(state_name: str) -> tuple:
    """Attempt to 'clone' a quantum state using CNOT."""
    # Prepare the source state on qubit 0
    qc = QuantumCircuit(2)

    if state_name == '1':
        qc.x(0)
    elif state_name == '+':
        qc.h(0)
    elif state_name == '-':
        qc.x(0)
        qc.h(0)
    # '0' → nothing needed

    # Attempt to clone via CNOT
    qc.cx(0, 1)

    # Get what CNOT actually produced
    cloning_result = Statevector.from_instruction(qc)

    # Compute ideal clone |ψ⟩⊗|ψ⟩
    qc_single = QuantumCircuit(1)
    if state_name == '1':
        qc_single.x(0)
    elif state_name == '+':
        qc_single.h(0)
    elif state_name == '-':
        qc_single.x(0)
        qc_single.h(0)

    single_sv = np.array(Statevector.from_instruction(qc_single))
    ideal_clone = Statevector(np.kron(single_sv, single_sv))

    return cloning_result, ideal_clone


# ============================================================
# Solution 5: Bell State Measurement Correlations
# ============================================================
#
# Interview Insight: Bell state correlations are the basis of:
#   1. Bell's theorem — proves quantum mechanics is non-local
#   2. CHSH inequality — classical bound is 2, quantum can reach 2√2
#   3. Quantum teleportation — uses Bell measurement to transfer state
#   4. Superdense coding — send 2 classical bits per qubit
#
# The correlation structure:
#   |Φ+⟩: Correlated in ALL bases (Z, X, Y)
#   |Φ-⟩: Correlated in Z, anti-correlated in X, correlated in Y
#   |Ψ+⟩: Anti-correlated in Z, correlated in X, anti-correlated in Y
#   |Ψ-⟩: Anti-correlated in ALL bases (the singlet state)
#
# The singlet |Ψ-⟩ is special: it's rotationally invariant.
# No matter what axis you measure, qubits are anti-correlated.
# This is the state used in the EPR paradox and Bell tests.

def bell_correlation(bell_circuit: QuantumCircuit, shots: int = 10000) -> float:
    """Compute correlation coefficient between Bell state qubits."""
    sv = Statevector.from_instruction(bell_circuit)
    probs = sv.probabilities_dict()

    p_same = probs.get('00', 0) + probs.get('11', 0)
    p_diff = probs.get('01', 0) + probs.get('10', 0)

    return p_same - p_diff


# ============================================================
# Bonus: Schmidt Decomposition
# ============================================================
#
# Any bipartite state |ψ⟩ ∈ H_A ⊗ H_B can be written as:
#   |ψ⟩ = Σᵢ λᵢ |aᵢ⟩|bᵢ⟩
# where λᵢ ≥ 0 (Schmidt coefficients) and {|aᵢ⟩}, {|bᵢ⟩}
# are orthonormal bases for A and B.
#
# Key properties:
#   - Number of non-zero λᵢ = Schmidt rank
#   - Schmidt rank 1 → separable
#   - Schmidt rank > 1 → entangled
#   - Equal λᵢ → maximally entangled
#
# For Bell states: λ₁ = λ₂ = 1/√2 (Schmidt rank 2, maximally entangled)
# For |00⟩:       λ₁ = 1 (Schmidt rank 1, separable)

def schmidt_decomposition(sv: Statevector) -> tuple:
    """
    Compute Schmidt decomposition of a 2-qubit state.

    Returns:
        Tuple of (coefficients, rank)
    """
    # Reshape statevector as 2x2 matrix
    psi = np.array(sv).reshape(2, 2)
    # SVD gives Schmidt decomposition
    U, s, Vh = np.linalg.svd(psi)
    # Non-zero singular values = Schmidt coefficients
    rank = np.sum(s > 1e-10)
    return s, rank


# ============================================================
# Verification
# ============================================================

if __name__ == '__main__':
    print("Day 3 Solutions — Verification")
    print("=" * 55)

    # Verify Bell states
    for name, func in [('Φ+', bell_phi_plus), ('Φ-', bell_phi_minus),
                        ('Ψ+', bell_psi_plus), ('Ψ-', bell_psi_minus)]:
        sv = Statevector.from_instruction(func())
        corr = bell_correlation(func())
        print(f"|{name}⟩ = {np.array(sv).round(4)}  correlation={corr:+.1f}")

    # Verify entanglement detection
    print()
    qc_ent = QuantumCircuit(2); qc_ent.h(0); qc_ent.cx(0, 1)
    qc_sep = QuantumCircuit(2); qc_sep.h(0)
    print(f"Bell state entangled? {is_entangled(qc_ent)}")
    print(f"|+0⟩ entangled? {is_entangled(qc_sep)}")

    # GHZ
    print()
    sv_ghz = Statevector.from_instruction(ghz_state(3))
    print(f"GHZ = {np.array(sv_ghz).round(4)}")

    # Schmidt decomposition
    print()
    coeffs_bell, rank_bell = schmidt_decomposition(
        Statevector.from_instruction(bell_phi_plus()))
    coeffs_sep, rank_sep = schmidt_decomposition(
        Statevector.from_instruction(QuantumCircuit(2)))
    print(f"Bell |Φ+⟩: Schmidt coeffs={coeffs_bell.round(4)}, rank={rank_bell}")
    print(f"|00⟩:      Schmidt coeffs={coeffs_sep.round(4)}, rank={rank_sep}")

    # No-cloning
    print()
    for state in ['0', '1', '+', '-']:
        result, ideal = attempt_clone(state)
        match = result.equiv(ideal)
        symbol = "✅ cloned!" if match else "❌ entangled (not cloned)"
        print(f"Clone |{state}⟩: {symbol}")
    print()
    print("💡 CNOT copies basis states but ENTANGLES superpositions.")
    print("   This is the no-cloning theorem in action!")
