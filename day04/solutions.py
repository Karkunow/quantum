"""
Day 4 Solutions: Quantum Circuits as Matrix Operations
======================================================

14-Day Quantum DevRel Bootcamp

Complete implementations with interview insights.
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector
from qiskit_aer import AerSimulator


# ============================================================
# Exercise 1: Multi-Qubit Gate Matrices
# ============================================================
# 💬 Interview insight: "Every quantum circuit IS a matrix.
# An n-qubit circuit is a 2ⁿ × 2ⁿ unitary matrix. This is why
# quantum simulation is exponentially hard — the matrices grow
# exponentially. Understanding the circuit-matrix correspondence
# is essential for verifying circuit correctness."

# Helper: standard matrices
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)
T_dag = T.conj().T

# Projectors
P0 = np.array([[1, 0], [0, 0]], dtype=complex)  # |0⟩⟨0|
P1 = np.array([[0, 0], [0, 1]], dtype=complex)  # |1⟩⟨1|


def cnot_matrix() -> np.ndarray:
    """Build CNOT using the projector formula.

    CNOT = |0⟩⟨0| ⊗ I + |1⟩⟨1| ⊗ X

    When control=|0⟩: do nothing (I) to target
    When control=|1⟩: flip (X) the target
    """
    return np.kron(P0, I2) + np.kron(P1, X)


def swap_matrix() -> np.ndarray:
    """Build SWAP matrix.

    SWAP can be derived as three CNOTs, but the matrix form is:
        SWAP = |0⟩⟨0| ⊗ I · (I ⊗ |0⟩⟨0| + X ⊗ |1⟩⟨1|)

    Or simply construct directly — SWAP permutes |01⟩ ↔ |10⟩:
    """
    sw = np.array([
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ], dtype=complex)
    return sw


def toffoli_matrix() -> np.ndarray:
    """Build the 8×8 Toffoli matrix.

    Toffoli = identity everywhere except the |11x⟩ subspace,
    where it applies X. In matrix terms, swap rows 6 and 7.

    💬 Interview insight: "Toffoli is a universal CLASSICAL gate —
    it can implement any classical Boolean function reversibly.
    Combined with H, it gives quantum universality. In practice,
    Toffoli decomposes into 6 CNOTs, which is expensive on NISQ hardware."
    """
    tof = np.eye(8, dtype=complex)
    # Swap |110⟩ (index 6) and |111⟩ (index 7)
    tof[6, 6] = 0
    tof[7, 7] = 0
    tof[6, 7] = 1
    tof[7, 6] = 1
    return tof


# ============================================================
# Exercise 2: SWAP from Three CNOTs
# ============================================================
# 💬 Interview insight: "SWAP costs 3 CNOTs, and since CNOT is
# the most expensive gate on hardware, optimizing SWAP count is
# critical. Transpilers spend enormous effort routing qubits to
# minimize the SWAPs needed for a given connectivity graph."

def swap_from_cnots() -> QuantumCircuit:
    """SWAP = CNOT(0,1) · CNOT(1,0) · CNOT(0,1)

    Proof by walking through basis states:
      |01⟩ → CNOT(0,1) → |11⟩ → CNOT(1,0) → |10⟩ → CNOT(0,1) → |10⟩ ✓
      |10⟩ → CNOT(0,1) → |10⟩ → CNOT(1,0) → |11⟩ → CNOT(0,1) → |01⟩ ✓
    """
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    qc.cx(1, 0)
    qc.cx(0, 1)
    return qc


# ============================================================
# Exercise 3: Controlled Gates
# ============================================================
# 💬 Interview insight: "The controlled-U construction
# CU = |0⟩⟨0|⊗I + |1⟩⟨1|⊗U is the general recipe for making
# any gate conditional. CZ is special because it's symmetric —
# you can't tell which qubit is the 'control'. This symmetry
# is why CZ is the native entangling gate on many platforms
# (superconducting, trapped ion)."

def cz_matrix() -> np.ndarray:
    """CZ = |0⟩⟨0| ⊗ I + |1⟩⟨1| ⊗ Z = diag(1, 1, 1, -1)"""
    return np.kron(P0, I2) + np.kron(P1, Z)


def controlled_u_matrix(u: np.ndarray) -> np.ndarray:
    """General controlled-U: CU = |0⟩⟨0| ⊗ I + |1⟩⟨1| ⊗ U"""
    return np.kron(P0, I2) + np.kron(P1, u)


def cz_from_cnot() -> QuantumCircuit:
    """CZ = (I ⊗ H) · CNOT · (I ⊗ H)

    Why this works: H transforms X basis ↔ Z basis.
    CNOT applies X conditionally; sandwiching the target with H
    converts that conditional-X into conditional-Z = CZ.

    This is a general identity:
        Controlled-U = (I ⊗ B) · CNOT · (I ⊗ B†)
        when U = B · X · B†
    """
    qc = QuantumCircuit(2)
    qc.h(0)       # H on target (qubit 0)
    qc.cx(1, 0)   # CNOT: control=1, target=0
    qc.h(0)       # H on target again
    return qc


# ============================================================
# Exercise 4: Toffoli Gate Decomposition
# ============================================================
# 💬 Interview insight: "Toffoli decomposes into 6 CNOTs and
# several T/T†/H gates. This 6-CNOT cost is a fundamental lower
# bound. The T gates make Toffoli non-Clifford, which is what
# gives it computational power beyond classical simulation.
# In fault-tolerant QC, each T gate requires magic state
# distillation — making Toffoli one of the most expensive gates."

def toffoli_circuit() -> QuantumCircuit:
    """Build Toffoli using Qiskit's built-in ccx."""
    qc = QuantumCircuit(3)
    qc.ccx(2, 1, 0)
    return qc


def toffoli_from_cnots() -> QuantumCircuit:
    """Decompose Toffoli into 1- and 2-qubit gates.

    Standard decomposition (Barenco et al.):
    Uses H, T, T†, and CNOT gates.
    """
    qc = QuantumCircuit(3)
    qc.ccx(2, 1, 0)
    return qc.decompose()


# ============================================================
# Exercise 5: Circuit Simulation with Qiskit Aer
# ============================================================
# 💬 Interview insight: "Real quantum computers give you SAMPLES,
# not statevectors. The AerSimulator mimics this: you get measurement
# counts from many shots. Understanding the difference between
# exact statevector simulation (exponential classical cost) and
# sampling simulation (polynomial per shot) is key to understanding
# why quantum computers are hard to simulate."

def simulate_bell_measurements(shots: int = 1024) -> dict:
    """Create |Φ+⟩, measure, return counts.

    Key: we add classical bits and measurement operations.
    Unlike Statevector simulation, this gives probabilistic results.
    """
    qc = QuantumCircuit(2, 2)  # 2 qubits, 2 classical bits
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    sim = AerSimulator()
    result = sim.run(qc, shots=shots).result()
    return result.get_counts()


def simulate_ghz_measurements(n: int = 3, shots: int = 1024) -> dict:
    """Create n-qubit GHZ, measure all, return counts."""
    qc = QuantumCircuit(n, n)
    qc.h(0)
    for i in range(n - 1):
        qc.cx(i, i + 1)
    qc.measure(range(n), range(n))

    sim = AerSimulator()
    result = sim.run(qc, shots=shots).result()
    return result.get_counts()


# ============================================================
# Bonus: Circuit Identity Proofs
# ============================================================

def verify_circuit_identities():
    """Verify important circuit identities that come up in interviews.

    💬 "Circuit identities are the algebraic toolkit of quantum
    computing. Knowing these lets you optimize circuits by hand
    and understand what transpilers do automatically."
    """
    print("Circuit Identities")
    print("=" * 55)

    # 1. HXH = Z
    hxh = H @ X @ H
    print(f"1. HXH = Z: {np.allclose(hxh, Z)} ✅")

    # 2. HZH = X
    hzh = H @ Z @ H
    print(f"2. HZH = X: {np.allclose(hzh, X)} ✅")

    # 3. HYH = -Y
    hyh = H @ Y @ H
    print(f"3. HYH = -Y: {np.allclose(hyh, -Y)} ✅")

    # 4. SXS† = Y (up to phase)
    sxs = S @ X @ S.conj().T
    print(f"4. SXS† = Y: {np.allclose(sxs, Y)} ✅")

    # 5. X = HZH (another way to see identity 2)
    print(f"5. X = HZH: {np.allclose(X, H @ Z @ H)} ✅")

    # 6. CNOT(a,b) · CNOT(a,b) = I (CNOT is its own inverse)
    cnot = cnot_matrix()
    print(f"6. CNOT² = I: {np.allclose(cnot @ cnot, np.eye(4))} ✅")

    # 7. Three CNOTs = SWAP (verified by matrix)
    swap_from_3cnot = Operator(swap_from_cnots()).data
    print(f"7. 3 CNOTs = SWAP: {np.allclose(swap_from_3cnot, swap_matrix())} ✅")

    # 8. CZ is symmetric
    cz = cz_matrix()
    # Swap control and target: should give same matrix
    qc_cz_01 = QuantumCircuit(2); qc_cz_01.cz(0, 1)
    qc_cz_10 = QuantumCircuit(2); qc_cz_10.cz(1, 0)
    print(f"8. CZ(0,1) = CZ(1,0): "
          f"{np.allclose(Operator(qc_cz_01).data, Operator(qc_cz_10).data)} ✅")

    # 9. T² = S
    print(f"9. T² = S: {np.allclose(T @ T, S)} ✅")

    # 10. S² = Z
    print(f"10. S² = Z: {np.allclose(S @ S, Z)} ✅")


def universality_demo():
    """Demonstrate that {H, T, CNOT} can approximate any gate.

    💬 Interview insight: "A gate set is universal if it can
    approximate any unitary to arbitrary precision. {H, T, CNOT}
    is universal because:
    - H and T generate a dense subset of SU(2) (single-qubit unitaries)
    - CNOT provides entanglement between qubits
    - Together they can approximate any unitary on n qubits

    The Solovay-Kitaev theorem guarantees efficient approximation:
    any single-qubit gate can be approximated to precision ε using
    O(log^c(1/ε)) gates from {H, T}."
    """
    print("\nUniversality of {H, T, CNOT}")
    print("=" * 55)

    # Show how H and T generate other common gates
    print("Generating gates from H and T:")
    print(f"  T² = S: {np.allclose(T @ T, S)} ✅")
    print(f"  S² = Z: {np.allclose(S @ S, Z)} ✅")
    print(f"  HZH = X: {np.allclose(H @ Z @ H, X)} ✅")
    print(f"  SXS† = Y: {np.allclose(S @ X @ S.conj().T, Y)} ✅")
    print()
    print("  So from {H, T} alone we can build {X, Y, Z, S, T, H}")
    print("  These generate a DENSE subset of all single-qubit gates.")
    print()
    print("  Add CNOT for entanglement → universal gate set!")
    print()

    # Show T gate count matters
    print("Why T count matters in fault-tolerant QC:")
    print("  - Clifford gates ({H, S, CNOT}) are 'free' with error correction")
    print("  - Each T gate needs magic state distillation (~1000 physical qubits)")
    print("  - Optimizing T count is THE key metric for fault-tolerant circuits")


if __name__ == "__main__":
    verify_circuit_identities()
    universality_demo()
