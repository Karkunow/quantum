"""
Day 4 Exercises: Quantum Circuits as Matrix Operations
======================================================

14-Day Quantum DevRel Bootcamp

Today's exercises cover:
1. Multi-qubit gate matrices (CNOT, SWAP, Toffoli)
2. Building SWAP from CNOTs
3. Controlled gates (CZ, CP, arbitrary controlled-U)
4. Toffoli (CCX) gate decomposition
5. Circuit simulation with Qiskit Aer

Run this file to test your implementations:
    python day04/exercises.py
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector
from qiskit_aer import AerSimulator


# ============================================================
# Exercise 1: Multi-Qubit Gate Matrices
# ============================================================
# Build gate matrices manually using np.kron (tensor products)
# and verify them against Qiskit's Operator class.
#
# Recall: For a 2-qubit gate that applies U on qubit i and
# identity on qubit j, we use tensor products:
#   - Gate on qubit 1 (left): U ⊗ I
#   - Gate on qubit 0 (right): I ⊗ U
#
# The CNOT matrix (control=1, target=0) is:
#   |00⟩→|00⟩, |01⟩→|01⟩, |10⟩→|11⟩, |11⟩→|10⟩
#
#   CNOT = |0⟩⟨0| ⊗ I + |1⟩⟨1| ⊗ X

def cnot_matrix() -> np.ndarray:
    """Build the 4×4 CNOT matrix manually (control=1, target=0).

    Use the projector formula:
        CNOT = |0⟩⟨0| ⊗ I + |1⟩⟨1| ⊗ X

    Returns:
        4×4 complex numpy array
    """
    # TODO: Define |0⟩⟨0| and |1⟩⟨1| projectors
    # TODO: Define I (2×2 identity) and X (Pauli-X)
    # TODO: Return |0⟩⟨0| ⊗ I + |1⟩⟨1| ⊗ X
    pass


def swap_matrix() -> np.ndarray:
    """Build the 4×4 SWAP matrix manually.

    SWAP exchanges two qubits:
        |00⟩→|00⟩, |01⟩→|10⟩, |10⟩→|01⟩, |11⟩→|11⟩

    SWAP = [[1,0,0,0],
            [0,0,1,0],
            [0,1,0,0],
            [0,0,0,1]]

    Returns:
        4×4 complex numpy array
    """
    # TODO: Build the SWAP matrix
    pass


def toffoli_matrix() -> np.ndarray:
    """Build the 8×8 Toffoli (CCX) matrix manually.

    Toffoli flips the target qubit only when BOTH controls are |1⟩:
        |110⟩ → |111⟩,  |111⟩ → |110⟩
        All other basis states unchanged.

    Hint: Toffoli = I⊗I⊗I everywhere except the |11x⟩ subspace,
          where it applies X to the target.

    Returns:
        8×8 complex numpy array
    """
    # TODO: Start with 8×8 identity
    # TODO: Swap rows/columns 6 and 7 (|110⟩ ↔ |111⟩)
    pass


# ============================================================
# Exercise 2: SWAP from Three CNOTs
# ============================================================
# The SWAP gate can be decomposed into exactly 3 CNOT gates:
#
#   SWAP = CNOT(0,1) · CNOT(1,0) · CNOT(0,1)
#
# This is important because SWAP isn't a native gate on most
# hardware — it must be compiled into CNOTs.

def swap_from_cnots() -> QuantumCircuit:
    """Build a SWAP gate using exactly 3 CNOT gates.

    The decomposition is:
        CNOT(0→1), then CNOT(1→0), then CNOT(0→1)

    Returns:
        QuantumCircuit implementing SWAP on 2 qubits
    """
    # TODO: Create a 2-qubit circuit
    # TODO: Apply 3 CNOTs in the correct order
    pass


# ============================================================
# Exercise 3: Controlled Gates
# ============================================================
# A controlled-U gate applies U to the target only when the
# control qubit is |1⟩:
#
#   CU = |0⟩⟨0| ⊗ I + |1⟩⟨1| ⊗ U
#
# Build controlled versions of common gates.

def cz_matrix() -> np.ndarray:
    """Build the 4×4 Controlled-Z (CZ) matrix manually.

    CZ applies Z to the target when control is |1⟩:
        CZ = |0⟩⟨0| ⊗ I + |1⟩⟨1| ⊗ Z

    Note: CZ is symmetric — it doesn't matter which qubit
    is the control! (Both qubits get a phase flip on |11⟩.)

    Returns:
        4×4 complex numpy array
    """
    # TODO: Use the projector formula with Z gate
    pass


def controlled_u_matrix(u: np.ndarray) -> np.ndarray:
    """Build a controlled-U matrix for an arbitrary 2×2 unitary U.

    CU = |0⟩⟨0| ⊗ I + |1⟩⟨1| ⊗ U

    Args:
        u: 2×2 unitary matrix

    Returns:
        4×4 complex numpy array
    """
    # TODO: Implement the general controlled-U formula
    pass


def cz_from_cnot() -> QuantumCircuit:
    """Build a CZ gate using only H gates and one CNOT.

    Identity: CZ = (I ⊗ H) · CNOT · (I ⊗ H)
    (Apply H before and after the CNOT on the target qubit.)

    Returns:
        QuantumCircuit implementing CZ on 2 qubits
    """
    # TODO: Create 2-qubit circuit
    # TODO: H on target, CNOT, H on target
    pass


# ============================================================
# Exercise 4: Toffoli Gate Decomposition
# ============================================================
# The Toffoli (CCX) gate can be decomposed into single-qubit
# gates and CNOTs. This is critical because hardware doesn't
# have native 3-qubit gates.
#
# One standard decomposition uses 6 CNOTs and several T/T†/H gates.
# For this exercise, use Qiskit's built-in decomposition to verify.

def toffoli_circuit() -> QuantumCircuit:
    """Build a Toffoli gate and verify it matches the matrix.

    Create a 3-qubit circuit with controls on qubits 2,1
    and target on qubit 0:
        qc.ccx(2, 1, 0)

    Returns:
        QuantumCircuit implementing Toffoli on 3 qubits
    """
    # TODO: Create a 3-qubit circuit
    # TODO: Apply ccx(2, 1, 0)
    pass


def toffoli_from_cnots() -> QuantumCircuit:
    """Decompose Toffoli into 1- and 2-qubit gates.

    Use Qiskit's decompose() method to break down the Toffoli gate.
    The standard decomposition uses 6 CNOTs + single-qubit gates.

    Returns:
        QuantumCircuit with only 1- and 2-qubit gates
    """
    # TODO: Build the Toffoli circuit
    # TODO: Call .decompose() on it
    pass


# ============================================================
# Exercise 5: Circuit Simulation with Qiskit Aer
# ============================================================
# Use AerSimulator to run circuits with measurement and collect
# shot-based statistics (like a real quantum computer).

def simulate_bell_measurements(shots: int = 1024) -> dict:
    """Create a Bell state |Φ+⟩, measure both qubits, and return counts.

    Steps:
    1. Create a 2-qubit circuit with 2 classical bits
    2. Apply H on qubit 0, CNOT(0, 1)
    3. Measure both qubits
    4. Run with AerSimulator for the given number of shots
    5. Return the measurement counts dictionary

    Expected: roughly 50% |00⟩ and 50% |11⟩ (no |01⟩ or |10⟩)

    Args:
        shots: Number of measurement repetitions

    Returns:
        dict like {'00': ~512, '11': ~512}
    """
    # TODO: Build Bell state circuit with measurements
    # TODO: Create AerSimulator and run
    # TODO: Return counts
    pass


def simulate_ghz_measurements(n: int = 3, shots: int = 1024) -> dict:
    """Create an n-qubit GHZ state, measure all qubits, return counts.

    GHZ = (|00...0⟩ + |11...1⟩) / √2

    Steps:
    1. Create n-qubit circuit with n classical bits
    2. H on qubit 0, then CNOT chain: cx(0,1), cx(1,2), ...
    3. Measure all qubits
    4. Run with AerSimulator

    Expected: roughly 50% |00...0⟩ and 50% |11...1⟩

    Args:
        n: Number of qubits (default 3)
        shots: Number of measurement repetitions

    Returns:
        dict like {'000': ~512, '111': ~512}
    """
    # TODO: Build GHZ circuit with measurements
    # TODO: Simulate and return counts
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
    print("Day 4 Tests: Quantum Circuits as Matrix Operations")
    print("=" * 60)

    # ── Exercise 1: Gate Matrices ──
    print("\n📝 Exercise 1: Multi-Qubit Gate Matrices")

    cnot = cnot_matrix()
    if cnot is not None:
        # Compare with Qiskit
        qc = QuantumCircuit(2); qc.cx(1, 0)
        qiskit_cnot = Operator(qc).data
        check("CNOT matrix matches Qiskit", np.allclose(cnot, qiskit_cnot))
        check("CNOT is unitary", np.allclose(cnot @ cnot.conj().T, np.eye(4)))
    else:
        check("CNOT matrix implemented", False)

    sw = swap_matrix()
    if sw is not None:
        qc = QuantumCircuit(2); qc.swap(0, 1)
        qiskit_swap = Operator(qc).data
        check("SWAP matrix matches Qiskit", np.allclose(sw, qiskit_swap))
        check("SWAP is its own inverse", np.allclose(sw @ sw, np.eye(4)))
    else:
        check("SWAP matrix implemented", False)

    tof = toffoli_matrix()
    if tof is not None:
        qc = QuantumCircuit(3); qc.ccx(2, 1, 0)
        qiskit_tof = Operator(qc).data
        check("Toffoli matrix matches Qiskit", np.allclose(tof, qiskit_tof))
        check("Toffoli is unitary", np.allclose(tof @ tof.conj().T, np.eye(8)))
    else:
        check("Toffoli matrix implemented", False)

    # ── Exercise 2: SWAP from CNOTs ──
    print("\n📝 Exercise 2: SWAP from Three CNOTs")

    swap_qc = swap_from_cnots()
    if swap_qc is not None:
        swap_op = Operator(swap_qc).data
        qc_ref = QuantumCircuit(2); qc_ref.swap(0, 1)
        ref_op = Operator(qc_ref).data
        check("SWAP circuit matches SWAP matrix", np.allclose(swap_op, ref_op))

        # Count CNOT gates
        cnot_count = sum(1 for inst in swap_qc.data if inst.operation.name == 'cx')
        check("Uses exactly 3 CNOTs", cnot_count == 3)
    else:
        check("SWAP from CNOTs implemented", False)

    # ── Exercise 3: Controlled Gates ──
    print("\n📝 Exercise 3: Controlled Gates")

    cz = cz_matrix()
    if cz is not None:
        qc = QuantumCircuit(2); qc.cz(1, 0)
        qiskit_cz = Operator(qc).data
        check("CZ matrix matches Qiskit", np.allclose(cz, qiskit_cz))
        check("CZ is symmetric (control/target interchangeable)",
              np.allclose(cz, cz.T))
    else:
        check("CZ matrix implemented", False)

    # Test controlled-U with T gate
    T_gate = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])
    cu = controlled_u_matrix(T_gate)
    if cu is not None:
        check("Controlled-T is unitary", np.allclose(cu @ cu.conj().T, np.eye(4)))
        # Top-left 2×2 should be identity (control=|0⟩ → do nothing)
        check("Controlled-U: control=0 → identity",
              np.allclose(cu[:2, :2], np.eye(2)))
        # Bottom-right 2×2 should be U (control=|1⟩ → apply U)
        check("Controlled-U: control=1 → apply U",
              np.allclose(cu[2:, 2:], T_gate))
    else:
        check("Controlled-U matrix implemented", False)

    cz_qc = cz_from_cnot()
    if cz_qc is not None:
        cz_op = Operator(cz_qc).data
        qc_ref = QuantumCircuit(2); qc_ref.cz(1, 0)
        ref_op = Operator(qc_ref).data
        check("CZ from H+CNOT+H matches CZ",
              np.allclose(cz_op, ref_op))
    else:
        check("CZ from CNOT implemented", False)

    # ── Exercise 4: Toffoli Decomposition ──
    print("\n📝 Exercise 4: Toffoli Gate Decomposition")

    tof_qc = toffoli_circuit()
    if tof_qc is not None:
        tof_op = Operator(tof_qc).data
        ref = toffoli_matrix()
        if ref is not None:
            check("Toffoli circuit matches matrix", np.allclose(tof_op, ref))
        else:
            qc_ref = QuantumCircuit(3); qc_ref.ccx(2, 1, 0)
            check("Toffoli circuit matches Qiskit",
                  np.allclose(tof_op, Operator(qc_ref).data))
    else:
        check("Toffoli circuit implemented", False)

    tof_decomp = toffoli_from_cnots()
    if tof_decomp is not None:
        # Verify no 3-qubit gates remain
        gate_names = [inst.operation.name for inst in tof_decomp.data]
        has_3q = any(inst.operation.num_qubits > 2 for inst in tof_decomp.data)
        check("Decomposition has no 3-qubit gates", not has_3q)
        check("Decomposition matches Toffoli matrix",
              np.allclose(Operator(tof_decomp).data, Operator(tof_qc).data))
    else:
        check("Toffoli decomposition implemented", False)

    # ── Exercise 5: Circuit Simulation ──
    print("\n📝 Exercise 5: Circuit Simulation with Aer")

    bell_counts = simulate_bell_measurements(shots=2048)
    if bell_counts is not None:
        total = sum(bell_counts.values())
        check("Bell simulation returns correct shot count", total == 2048)
        # Should only have '00' and '11'
        only_correlated = all(k in ['00', '11'] for k in bell_counts.keys())
        check("Bell: only |00⟩ and |11⟩ outcomes", only_correlated)
        # Each should be roughly 50%
        if '00' in bell_counts and '11' in bell_counts:
            ratio = bell_counts['00'] / total
            check("Bell: roughly 50/50 split", 0.35 < ratio < 0.65)
        else:
            check("Bell: roughly 50/50 split", False)
    else:
        check("Bell simulation implemented", False)

    ghz_counts = simulate_ghz_measurements(n=4, shots=2048)
    if ghz_counts is not None:
        total = sum(ghz_counts.values())
        check("GHZ simulation returns correct shot count", total == 2048)
        only_ghz = all(k in ['0000', '1111'] for k in ghz_counts.keys())
        check("GHZ-4: only |0000⟩ and |1111⟩ outcomes", only_ghz)
    else:
        check("GHZ simulation implemented", False)

    # ── Summary ──
    print(f"\n{'=' * 60}")
    print(f"Results: {passed}/{passed + failed} tests passed")
    if failed == 0:
        print("🎉 All tests passed! Ready for Day 5!")
    else:
        print(f"💪 {failed} test(s) remaining. Check the TODOs above.")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
