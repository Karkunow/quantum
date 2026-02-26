"""
Day 7 Exercises: Quantum Fourier Transform
============================================

14-Day Quantum DevRel Bootcamp

Today's exercises cover:
1. Classical DFT → QFT correspondence
2. QFT circuit construction from scratch
3. Inverse QFT
4. Quantum Phase Estimation (QPE)
5. QPE on known eigenvalue problems

Run this file to test your implementations:
    python day07/exercises.py
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator
from qiskit_aer import AerSimulator


# ============================================================
# Exercise 1: Classical DFT and QFT Matrix
# ============================================================
# The Discrete Fourier Transform maps N complex numbers to N
# frequency components:
#
#   y_k = (1/√N) Σⱼ xⱼ · ω^(jk)    where ω = e^(2πi/N)
#
# The QFT does the same on quantum amplitudes:
#
#   QFT|j⟩ = (1/√N) Σ_k ω^(jk) |k⟩
#
# The QFT matrix has entries:
#   (QFT)_kj = ω^(jk) / √N

def classical_dft_matrix(N: int) -> np.ndarray:
    """Build the N×N DFT matrix.

    (DFT)_kj = ω^(jk) / √N  where ω = e^(2πi/N)

    Args:
        N: Dimension of the transform

    Returns:
        N×N complex unitary matrix
    """
    # TODO: Build the DFT matrix
    pass


def qft_matrix(n_qubits: int) -> np.ndarray:
    """Build the QFT matrix for n qubits.

    This is the DFT matrix of size N = 2ⁿ.

    Args:
        n_qubits: Number of qubits

    Returns:
        2ⁿ × 2ⁿ unitary matrix
    """
    # TODO: Return the DFT matrix with N = 2^n_qubits
    pass


def verify_qft_properties(n_qubits: int) -> dict:
    """Verify key properties of the QFT matrix.

    Check:
    1. Unitarity: QFT† · QFT = I
    2. Symmetry: QFT is symmetric (QFT = QFTᵀ)
    3. QFT⁴ = I (QFT has order 4... for the DFT at least)
    4. QFT|0⟩ = |+⟩⊗ⁿ (uniform superposition)

    Args:
        n_qubits: Number of qubits

    Returns:
        Dict with boolean results for each property
    """
    # TODO: Build QFT matrix and check each property
    pass


# ============================================================
# Exercise 2: QFT Circuit Construction
# ============================================================
# The QFT circuit for n qubits:
#
# For qubit j (from most significant to least):
#   1. Apply Hadamard to qubit j
#   2. Apply controlled-R_k rotation from qubit j+1, j+2, ...
#      where R_k = [[1, 0], [0, e^(2πi/2^k)]]
#   3. After all rotations, swap qubits to reverse bit order
#
# The controlled rotation R_k adds phase e^(2πi/2^k) when
# both control and target are |1⟩.

def qft_circuit(n_qubits: int, swap: bool = True) -> QuantumCircuit:
    """Build the QFT circuit for n qubits.

    Algorithm:
        For j = 0 to n-1:
            H on qubit j
            For k = 1 to n-1-j:
                Controlled-R_(k+1) with control=j+k, target=j
                where R_m adds phase 2π/2^m
        Swap qubits to reverse order (if swap=True)

    Args:
        n_qubits: Number of qubits
        swap: Whether to include the final SWAP gates
              for correct bit ordering

    Returns:
        QuantumCircuit implementing QFT

    Hint: Use qc.cp(angle, control, target) for controlled phase.
          The angle for R_k is 2π/2^k.
    """
    # TODO: Implement the QFT circuit
    pass


def inverse_qft_circuit(n_qubits: int, swap: bool = True) -> QuantumCircuit:
    """Build the inverse QFT circuit.

    The inverse QFT is simply the QFT circuit reversed with
    all rotation angles negated (i.e., the adjoint / dagger).

    Args:
        n_qubits: Number of qubits
        swap: Whether to include SWAP gates

    Returns:
        QuantumCircuit implementing QFT†

    Hint: Use qft_circuit(n_qubits, swap).inverse()
    """
    # TODO: Return the inverse of the QFT circuit
    pass


# ============================================================
# Exercise 3: QFT on Specific States
# ============================================================
# The QFT transforms computational basis states to phase states:
#
#   QFT|j⟩ = (1/√N) Σ_k e^(2πijk/N) |k⟩
#
# Special cases:
#   QFT|0⟩ = |+⟩⊗ⁿ (uniform superposition)
#   QFT maps periodic states to peaked states (and vice versa)

def qft_on_basis_state(n_qubits: int, j: int) -> Statevector:
    """Apply QFT to computational basis state |j⟩.

    Args:
        n_qubits: Number of qubits
        j: Basis state index (0 to 2ⁿ - 1)

    Returns:
        Statevector after QFT
    """
    # TODO: Create |j⟩, build QFT circuit, return statevector
    pass


def qft_on_periodic_state(n_qubits: int, period: int) -> Statevector:
    """Apply QFT to a state with period r in the computational basis.

    Create a state that is uniform over {0, r, 2r, ...} and apply QFT.
    This demonstrates how QFT converts periodicity in the computational
    basis to peaks in the frequency basis.

    Args:
        n_qubits: Number of qubits (N = 2ⁿ)
        period: Period r of the input state

    Returns:
        Statevector after QFT

    Example:
        n=3, period=2: input has support on {|000⟩, |010⟩, |100⟩, |110⟩}
        QFT output should peak at multiples of N/r = 8/2 = 4 → {|000⟩, |100⟩}
    """
    # TODO: Build periodic state, apply QFT, return result
    pass


# ============================================================
# Exercise 4: Quantum Phase Estimation (QPE)
# ============================================================
# QPE estimates the eigenvalue phase φ of a unitary U:
#   U|ψ⟩ = e^(2πiφ)|ψ⟩
#
# Algorithm:
#   1. n counting qubits in |0⟩, eigenstate |ψ⟩ in target register
#   2. H on all counting qubits
#   3. Controlled-U^(2^j) from counting qubit j to target
#   4. Inverse QFT on counting register
#   5. Measure counting register → binary estimate of φ
#
# For n counting qubits, precision is 2^(-n)

def qpe_circuit(unitary: QuantumCircuit | np.ndarray,
                n_counting: int,
                eigenstate: QuantumCircuit | None = None) -> QuantumCircuit:
    """Build a Quantum Phase Estimation circuit.

    Args:
        unitary: The unitary U as a QuantumCircuit or matrix
                 (must act on the same number of qubits as eigenstate)
        n_counting: Number of counting (precision) qubits
        eigenstate: Circuit to prepare the eigenstate |ψ⟩
                    (if None, assume target starts in |0⟩...target qubits prepared externally)

    Returns:
        QuantumCircuit with n_counting + n_target qubits
        and measurements on the counting register
    """
    # TODO: Build the QPE circuit
    # Steps:
    #   1. Create circuit with counting + target qubits
    #   2. H on counting qubits
    #   3. Prepare eigenstate (if provided)
    #   4. Controlled-U^(2^j) for each counting qubit j
    #   5. Inverse QFT on counting qubits
    #   6. Measure counting qubits
    pass


def estimate_phase(unitary: np.ndarray,
                   eigenstate: np.ndarray,
                   n_counting: int = 4,
                   shots: int = 1024) -> float:
    """Estimate the phase of an eigenvalue using QPE.

    Given U|ψ⟩ = e^(2πiφ)|ψ⟩, estimate φ.

    Args:
        unitary: 2×2 (or larger) unitary matrix
        eigenstate: Eigenvector of U (as state vector)
        n_counting: Number of precision qubits
        shots: Number of measurement shots

    Returns:
        Estimated phase φ ∈ [0, 1)
    """
    # TODO: Build and run QPE, extract most likely phase
    pass


# ============================================================
# Exercise 5: QPE Applications
# ============================================================
# QPE can estimate eigenvalues of:
#   - Rotation gates: Rz(θ)|1⟩ = e^(-iθ/2)|1⟩ → φ = -θ/(2π) mod 1
#   - T gate: T|1⟩ = e^(iπ/4)|1⟩ → φ = 1/8
#   - General unitaries: key subroutine in Shor's algorithm

def qpe_t_gate(n_counting: int = 3, shots: int = 1024) -> dict:
    """Use QPE to estimate the phase of the T gate on |1⟩.

    T|1⟩ = e^(iπ/4)|1⟩, so φ = 1/8 = 0.001 in binary.

    Args:
        n_counting: Number of counting qubits
        shots: Number of shots

    Returns:
        Dict with 'estimated_phase', 'exact_phase', 'counts', 'error'
    """
    # TODO: Build QPE for T gate, run, extract phase
    # Hint: T = [[1, 0], [0, e^(iπ/4)]], eigenstate = |1⟩
    pass


def qpe_rotation_gate(theta: float, n_counting: int = 4,
                      shots: int = 1024) -> dict:
    """Use QPE to estimate the phase of Rz(θ) on |1⟩.

    Rz(θ)|1⟩ = e^(-iθ/2)|1⟩, so φ = (-θ/2)/(2π) mod 1 = 1 - θ/(4π)

    Args:
        theta: Rotation angle
        n_counting: Number of counting qubits
        shots: Number of shots

    Returns:
        Dict with 'estimated_phase', 'exact_phase', 'error', 'theta'
    """
    # TODO: Build QPE for Rz(θ), run, extract phase
    pass


def shor_connection(N_to_factor: int = 15) -> str:
    """Explain how QPE connects to Shor's algorithm.

    Returns a formatted string explaining the connection.
    (No implementation needed — this is a conceptual exercise.)

    The key insight:
    1. Shor reduces factoring to ORDER FINDING
    2. Order finding asks: find smallest r such that a^r ≡ 1 (mod N)
    3. QPE can find r by estimating eigenvalues of the
       modular exponentiation operator U_a|x⟩ = |ax mod N⟩
    4. The eigenvalues of U_a are e^(2πis/r) for s = 0, ..., r-1
    5. QPE gives s/r, from which r can be extracted via
       continued fractions
    """
    # TODO: Return a clear explanation string
    pass


# =============================================================
# TESTS — Run these to verify your implementations
# =============================================================
def run_tests():
    """Test all implementations."""
    passed = 0
    failed = 0

    def check(description, condition):
        nonlocal passed, failed
        if condition:
            print(f"   ✅ {description}")
            passed += 1
        else:
            print(f"   ❌ {description}")
            failed += 1

    # ── Exercise 1: DFT / QFT Matrix ──
    print("\n📝 Exercise 1: DFT / QFT Matrix")

    dft4 = classical_dft_matrix(4)
    if dft4 is not None:
        check("DFT(4) is 4×4", dft4.shape == (4, 4))
        check("DFT(4) is unitary",
              np.allclose(dft4 @ dft4.conj().T, np.eye(4)))
        # DFT of |0⟩ should be uniform
        e0 = np.array([1, 0, 0, 0], dtype=complex)
        result = dft4 @ e0
        check("DFT|0⟩ = uniform",
              np.allclose(np.abs(result), 0.5 * np.ones(4)))
    else:
        check("classical_dft_matrix implemented", False)

    qft4 = qft_matrix(2)
    if qft4 is not None:
        check("QFT(2 qubits) shape correct", qft4.shape == (4, 4))
        check("QFT is unitary",
              np.allclose(qft4 @ qft4.conj().T, np.eye(4)))
    else:
        check("qft_matrix implemented", False)

    props = verify_qft_properties(2)
    if props is not None:
        check("QFT is unitary (verified)", props.get('unitary', False))
        check("QFT|0⟩ = uniform", props.get('zero_to_uniform', False))
    else:
        check("verify_qft_properties implemented", False)

    # ── Exercise 2: QFT Circuit ──
    print("\n📝 Exercise 2: QFT Circuit Construction")

    qft_circ = qft_circuit(3)
    if qft_circ is not None:
        check("QFT circuit is QuantumCircuit",
              isinstance(qft_circ, QuantumCircuit))
        check("QFT circuit has 3 qubits", qft_circ.num_qubits == 3)
        # Verify against matrix
        op = Operator(qft_circ)
        expected = qft_matrix(3) if qft_matrix(3) is not None else None
        if expected is not None:
            check("QFT circuit matches QFT matrix",
                  op.equiv(Operator(expected)))
    else:
        check("qft_circuit implemented", False)

    iqft_circ = inverse_qft_circuit(3)
    if iqft_circ is not None:
        check("Inverse QFT is QuantumCircuit",
              isinstance(iqft_circ, QuantumCircuit))
        # QFT · QFT† = I
        if qft_circ is not None:
            combined = QuantumCircuit(3)
            combined.compose(qft_circ, inplace=True)
            combined.compose(iqft_circ, inplace=True)
            op_combined = Operator(combined)
            check("QFT · QFT† ≈ I",
                  op_combined.equiv(Operator(np.eye(8))))
    else:
        check("inverse_qft_circuit implemented", False)

    # ── Exercise 3: QFT on States ──
    print("\n📝 Exercise 3: QFT on Specific States")

    sv_0 = qft_on_basis_state(3, 0)
    if sv_0 is not None:
        # QFT|000⟩ = uniform superposition
        probs = np.abs(sv_0.data) ** 2
        check("QFT|000⟩ = uniform",
              np.allclose(probs, np.ones(8) / 8, atol=1e-6))
    else:
        check("qft_on_basis_state implemented", False)

    sv_p = qft_on_periodic_state(3, 2)
    if sv_p is not None:
        probs = np.abs(sv_p.data) ** 2
        # Period 2 in input → peaks at multiples of N/2 = 4
        check("Periodic input: peaks at frequency multiples",
              probs[0] > 0.4 and probs[4] > 0.4)
    else:
        check("qft_on_periodic_state implemented", False)

    # ── Exercise 4: QPE ──
    print("\n📝 Exercise 4: Quantum Phase Estimation")

    # QPE on S gate: S|1⟩ = i|1⟩ → φ = 1/4
    S_gate = np.array([[1, 0], [0, 1j]], dtype=complex)
    eigenstate_1 = np.array([0, 1], dtype=complex)
    phase_s = estimate_phase(S_gate, eigenstate_1, n_counting=3, shots=1024)
    if phase_s is not None:
        check("QPE on S gate: φ ≈ 0.25",
              abs(phase_s - 0.25) < 0.05)
    else:
        check("estimate_phase implemented", False)

    # QPE on Z gate: Z|1⟩ = -|1⟩ → φ = 1/2
    Z_gate = np.array([[1, 0], [0, -1]], dtype=complex)
    phase_z = estimate_phase(Z_gate, eigenstate_1, n_counting=3, shots=1024)
    if phase_z is not None:
        check("QPE on Z gate: φ ≈ 0.5",
              abs(phase_z - 0.5) < 0.05)
    else:
        check("estimate_phase (Z) implemented", False)

    # ── Exercise 5: QPE Applications ──
    print("\n📝 Exercise 5: QPE Applications")

    t_result = qpe_t_gate(n_counting=3, shots=1024)
    if t_result is not None:
        check("T gate: estimated φ ≈ 1/8",
              abs(t_result['estimated_phase'] - 0.125) < 0.05)
        check("T gate: exact phase is 1/8",
              abs(t_result['exact_phase'] - 0.125) < 1e-10)
    else:
        check("qpe_t_gate implemented", False)

    rz_result = qpe_rotation_gate(np.pi / 3, n_counting=4, shots=1024)
    if rz_result is not None:
        exact = 1 - (np.pi / 3) / (4 * np.pi)
        check("Rz(π/3) QPE: reasonable estimate",
              abs(rz_result['estimated_phase'] - exact) < 0.1)
    else:
        check("qpe_rotation_gate implemented", False)

    explanation = shor_connection()
    if explanation is not None:
        check("Shor connection explained",
              len(explanation) > 50 and 'order' in explanation.lower())
    else:
        check("shor_connection implemented", False)

    # ── Summary ──
    print(f"\n{'=' * 60}")
    print(f"Results: {passed}/{passed + failed} tests passed")
    if failed == 0:
        print("🎉 All tests passed! Week 1 complete!")
    else:
        print(f"💪 {failed} test(s) remaining. Check the TODOs above.")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
