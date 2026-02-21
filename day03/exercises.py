"""
Day 3 Exercises: Multi-Qubit Systems & Entanglement
====================================================

14-Day Quantum DevRel Bootcamp

Today's exercises cover:
1. Building Bell state circuits
2. Entanglement verification via partial trace
3. Partial measurement and post-measurement states
4. GHZ and W state construction
5. No-cloning theorem demonstration

Run this file to test your implementations:
    python day03/exercises.py
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace


# ============================================================
# Exercise 1: Build the Four Bell State Circuits
# ============================================================
# The Bell states are the four maximally entangled two-qubit states:
#
#   |Φ+⟩ = (|00⟩ + |11⟩) / √2
#   |Φ-⟩ = (|00⟩ - |11⟩) / √2
#   |Ψ+⟩ = (|01⟩ + |10⟩) / √2
#   |Ψ-⟩ = (|01⟩ - |10⟩) / √2
#
# All four can be constructed from |00⟩ using H, X, Z, and CNOT.
#
# Pattern:
#   |Φ+⟩ = CNOT · (H ⊗ I) |00⟩
#   |Φ-⟩ = CNOT · (H ⊗ I) |10⟩   (apply X to qubit 0 first)
#   |Ψ+⟩ = CNOT · (H ⊗ I) |01⟩   (apply X to qubit 1 first)
#   |Ψ-⟩ = CNOT · (H ⊗ I) |11⟩   (apply X to both first)

def bell_phi_plus() -> QuantumCircuit:
    """Build a circuit that creates |Φ+⟩ = (|00⟩ + |11⟩) / √2."""
    # TODO: Create a 2-qubit circuit
    # TODO: Apply H to qubit 0
    # TODO: Apply CNOT with control=0, target=1
    pass


def bell_phi_minus() -> QuantumCircuit:
    """Build a circuit that creates |Φ-⟩ = (|00⟩ - |11⟩) / √2."""
    # TODO: Start from |10⟩ (apply X to qubit 0)
    # TODO: Apply H to qubit 0
    # TODO: Apply CNOT with control=0, target=1
    pass


def bell_psi_plus() -> QuantumCircuit:
    """Build a circuit that creates |Ψ+⟩ = (|01⟩ + |10⟩) / √2."""
    # TODO: Start from |01⟩ (apply X to qubit 1)
    # TODO: Apply H to qubit 0
    # TODO: Apply CNOT with control=0, target=1
    pass


def bell_psi_minus() -> QuantumCircuit:
    """Build a circuit that creates |Ψ-⟩ = (|01⟩ - |10⟩) / √2."""
    # TODO: Start from |11⟩ (apply X to both qubits)
    # TODO: Apply H to qubit 0
    # TODO: Apply CNOT with control=0, target=1
    pass


# ============================================================
# Exercise 2: Entanglement Verification
# ============================================================
# A state is entangled if and only if the partial trace over either
# subsystem gives a MIXED state (not pure).
#
# For a pure state ρ = |ψ⟩⟨ψ|:
#   - ρ_A = Tr_B(ρ)  — reduced density matrix of qubit A
#   - If ρ_A is pure (Tr(ρ_A²) = 1) → separable
#   - If ρ_A is mixed (Tr(ρ_A²) < 1) → entangled
#
# The purity Tr(ρ²) ranges from 1/d (maximally mixed) to 1 (pure).

def is_entangled(qc: QuantumCircuit) -> bool:
    """
    Determine if the output state of a circuit is entangled.

    Use the partial trace to compute the reduced density matrix
    of qubit 0, then check its purity.

    Args:
        qc: A 2-qubit QuantumCircuit.

    Returns:
        True if the state is entangled, False if separable.

    Hint:
        - Get the full statevector: Statevector.from_instruction(qc)
        - Convert to density matrix: DensityMatrix(sv)
        - Partial trace over qubit 1: partial_trace(dm, [1])
        - Check purity: np.real(np.trace(reduced.data @ reduced.data))
        - Entangled if purity < 1 (use tolerance: purity < 0.999)
    """
    # TODO: Implement entanglement detection
    pass


# ============================================================
# Exercise 3: Build GHZ and W States
# ============================================================
# GHZ state (3 qubits): |GHZ⟩ = (|000⟩ + |111⟩) / √2
#   - Maximally entangled, but fragile: losing one qubit destroys
#     ALL entanglement between the remaining two.
#
# W state (3 qubits): |W⟩ = (|001⟩ + |010⟩ + |100⟩) / √3
#   - Entangled, but robust: losing one qubit leaves the other
#     two STILL entangled.

def ghz_state(n: int = 3) -> QuantumCircuit:
    """
    Build a circuit that creates the n-qubit GHZ state:
    |GHZ_n⟩ = (|00...0⟩ + |11...1⟩) / √2

    Args:
        n: Number of qubits (default 3).

    Hint:
        - Apply H to qubit 0
        - Apply CNOT from qubit 0 to qubit 1, 2, ..., n-1
    """
    # TODO: Implement n-qubit GHZ state
    pass


def w_state() -> QuantumCircuit:
    """
    Build a circuit that creates the 3-qubit W state:
    |W⟩ = (|001⟩ + |010⟩ + |100⟩) / √3

    This is harder than GHZ! One approach:
        1. Start from |100⟩ (apply X to qubit 0)
        2. Apply Ry(2·arccos(1/√3)) to qubit 0
           This creates: √(1/3)|0⟩ + √(2/3)|1⟩ on qubit 0
        3. Apply controlled-Ry(π/2) from qubit 0 to qubit 1
           (or use CNOT + Ry combinations)
        4. Apply CNOT from qubit 1 to qubit 2

    Alternative: Use Qiskit's initialize method if stuck:
        qc.initialize([0,1,1,0,1,0,0,0] / np.sqrt(3))
    """
    # TODO: Implement W state (use initialize if needed)
    pass


# ============================================================
# Exercise 4: Demonstrate the No-Cloning Theorem
# ============================================================
# The no-cloning theorem states: there is no unitary operation U
# that can copy an ARBITRARY unknown quantum state:
#   U|ψ⟩|0⟩ = |ψ⟩|ψ⟩  ← impossible for all |ψ⟩
#
# However, CNOT CAN "copy" computational basis states:
#   CNOT|0⟩|0⟩ = |0⟩|0⟩  ✓
#   CNOT|1⟩|0⟩ = |1⟩|1⟩  ✓
#
# But it FAILS for superpositions:
#   CNOT|+⟩|0⟩ = (|00⟩ + |11⟩)/√2 ≠ |+⟩|+⟩

def attempt_clone(state_name: str) -> tuple:
    """
    Attempt to "clone" a quantum state using CNOT.

    Args:
        state_name: One of '0', '1', '+', '-'

    Returns:
        Tuple of (cloning_result: Statevector, ideal_clone: Statevector)
        - cloning_result: What CNOT actually produces
        - ideal_clone: What a perfect clone |ψ⟩|ψ⟩ would be

    Steps:
        1. Create a 2-qubit circuit
        2. Prepare qubit 0 in the desired state
        3. Apply CNOT(0, 1) — attempting to copy
        4. Get the result statevector
        5. Compute the ideal |ψ⟩⊗|ψ⟩ using np.kron

    Hint for preparing states:
        '0' → nothing, '1' → X, '+' → H, '-' → X then H
    """
    # TODO: Implement cloning attempt
    pass


# ============================================================
# Exercise 5: Bell State Measurement Correlations
# ============================================================
# When measuring a Bell state, the two qubits are perfectly
# correlated (or anti-correlated).
#
# |Φ+⟩ = (|00⟩ + |11⟩)/√2:
#   - Measuring qubit 0 gives 0 → qubit 1 MUST be 0
#   - Measuring qubit 0 gives 1 → qubit 1 MUST be 1
#   - Perfect positive correlation
#
# |Ψ-⟩ = (|01⟩ - |10⟩)/√2:
#   - Measuring qubit 0 gives 0 → qubit 1 MUST be 1
#   - Measuring qubit 0 gives 1 → qubit 1 MUST be 0
#   - Perfect anti-correlation

def bell_correlation(bell_circuit: QuantumCircuit, shots: int = 10000) -> float:
    """
    Compute the correlation coefficient between measurement outcomes
    of the two qubits in a Bell state.

    Correlation = P(same) - P(different)
    - For |Φ+⟩ and |Φ-⟩: correlation = +1 (always same)
    - For |Ψ+⟩ and |Ψ-⟩: correlation = -1 (always different)

    Args:
        bell_circuit: A 2-qubit circuit producing a Bell state.
        shots: Number of measurement samples.

    Returns:
        Correlation coefficient between -1 and +1.

    Hint:
        1. Copy the circuit and add measurements: qc.measure_all()
        2. Use Statevector for exact probabilities:
           sv = Statevector.from_instruction(bell_circuit)
           probs = sv.probabilities_dict()
        3. Count P(same) = P('00') + P('11')
           Count P(diff) = P('01') + P('10')
        4. Return P(same) - P(diff)
    """
    # TODO: Implement correlation measurement
    pass


# ============================================================
# Tests
# ============================================================

def run_tests():
    """Run all exercise tests."""
    print("🧪 Day 3 Exercise Tests")
    print("=" * 60)

    passed = 0
    total = 0

    # ── Test 1: Bell states ──
    print("\n📋 Test 1: Bell State Circuits")
    bell_targets = {
        'Φ+': (bell_phi_plus, np.array([1, 0, 0, 1]) / np.sqrt(2)),
        'Φ-': (bell_phi_minus, np.array([1, 0, 0, -1]) / np.sqrt(2)),
        'Ψ+': (bell_psi_plus, np.array([0, 1, 1, 0]) / np.sqrt(2)),
        'Ψ-': (bell_psi_minus, np.array([0, 1, -1, 0]) / np.sqrt(2)),
    }

    for name, (func, target) in bell_targets.items():
        total += 1
        try:
            qc = func()
            assert qc is not None, "Function returned None"
            sv = Statevector.from_instruction(qc)
            assert sv.equiv(Statevector(target)), \
                f"Expected {target}, got {np.array(sv)}"
            print(f"   |{name}⟩: ✅")
            passed += 1
        except Exception as e:
            print(f"   |{name}⟩: ❌ {e}")

    # ── Test 2: Entanglement detection ──
    print("\n📋 Test 2: Entanglement Verification")

    # Entangled state: Bell |Φ+⟩
    total += 1
    try:
        qc_ent = QuantumCircuit(2)
        qc_ent.h(0)
        qc_ent.cx(0, 1)
        result = is_entangled(qc_ent)
        assert result is not None, "Function returned None"
        assert result is True, f"Bell state should be entangled, got {result}"
        print("   Bell state (entangled): ✅")
        passed += 1
    except Exception as e:
        print(f"   Bell state (entangled): ❌ {e}")

    # Separable state: |+0⟩
    total += 1
    try:
        qc_sep = QuantumCircuit(2)
        qc_sep.h(0)
        result = is_entangled(qc_sep)
        assert result is not None, "Function returned None"
        assert result is False, f"|+0⟩ should be separable, got {result}"
        print("   |+0⟩ state (separable): ✅")
        passed += 1
    except Exception as e:
        print(f"   |+0⟩ state (separable): ❌ {e}")

    # ── Test 3: GHZ state ──
    print("\n📋 Test 3: GHZ State")
    total += 1
    try:
        qc = ghz_state(3)
        assert qc is not None, "Function returned None"
        sv = Statevector.from_instruction(qc)
        target = np.zeros(8)
        target[0] = 1 / np.sqrt(2)  # |000⟩
        target[7] = 1 / np.sqrt(2)  # |111⟩
        assert sv.equiv(Statevector(target)), \
            f"Expected (|000⟩+|111⟩)/√2, got {np.array(sv)}"
        print("   3-qubit GHZ: ✅")
        passed += 1
    except Exception as e:
        print(f"   3-qubit GHZ: ❌ {e}")

    # 4-qubit GHZ
    total += 1
    try:
        qc = ghz_state(4)
        sv = Statevector.from_instruction(qc)
        target = np.zeros(16)
        target[0] = 1 / np.sqrt(2)
        target[15] = 1 / np.sqrt(2)
        assert sv.equiv(Statevector(target)), "4-qubit GHZ incorrect"
        print("   4-qubit GHZ: ✅")
        passed += 1
    except Exception as e:
        print(f"   4-qubit GHZ: ❌ {e}")

    # ── Test 4: W state ──
    print("\n📋 Test 4: W State")
    total += 1
    try:
        qc = w_state()
        assert qc is not None, "Function returned None"
        sv = Statevector.from_instruction(qc)
        target = np.zeros(8, dtype=complex)
        target[1] = 1 / np.sqrt(3)  # |001⟩
        target[2] = 1 / np.sqrt(3)  # |010⟩
        target[4] = 1 / np.sqrt(3)  # |100⟩
        assert sv.equiv(Statevector(target)), \
            f"Expected (|001⟩+|010⟩+|100⟩)/√3"
        print("   W state: ✅")
        passed += 1
    except Exception as e:
        print(f"   W state: ❌ {e}")

    # ── Test 5: No-cloning ──
    print("\n📋 Test 5: No-Cloning Theorem")

    # Cloning |0⟩ should work (CNOT copies basis states)
    total += 1
    try:
        result, ideal = attempt_clone('0')
        assert result is not None, "Function returned None"
        assert result.equiv(ideal), "Cloning |0⟩ should succeed"
        print("   Clone |0⟩ (succeeds): ✅")
        passed += 1
    except Exception as e:
        print(f"   Clone |0⟩ (succeeds): ❌ {e}")

    # Cloning |+⟩ should FAIL (demonstrates no-cloning)
    total += 1
    try:
        result, ideal = attempt_clone('+')
        assert result is not None, "Function returned None"
        assert not result.equiv(ideal), \
            "Cloning |+⟩ should FAIL — no-cloning theorem!"
        print("   Clone |+⟩ (fails — correct!): ✅")
        passed += 1
    except Exception as e:
        print(f"   Clone |+⟩ (fails — correct!): ❌ {e}")

    # ── Test 6: Bell correlations ──
    print("\n📋 Test 6: Bell State Correlations")

    # Φ+ should have correlation +1
    total += 1
    try:
        qc_phi = QuantumCircuit(2)
        qc_phi.h(0)
        qc_phi.cx(0, 1)
        corr = bell_correlation(qc_phi)
        assert corr is not None, "Function returned None"
        assert abs(corr - 1.0) < 0.01, \
            f"|Φ+⟩ correlation should be +1, got {corr}"
        print(f"   |Φ+⟩ correlation = {corr:+.3f}: ✅")
        passed += 1
    except Exception as e:
        print(f"   |Φ+⟩ correlation: ❌ {e}")

    # Ψ- should have correlation -1
    total += 1
    try:
        qc_psi = QuantumCircuit(2)
        qc_psi.x(0)
        qc_psi.x(1)
        qc_psi.h(0)
        qc_psi.cx(0, 1)
        corr = bell_correlation(qc_psi)
        assert abs(corr - (-1.0)) < 0.01, \
            f"|Ψ-⟩ correlation should be -1, got {corr}"
        print(f"   |Ψ-⟩ correlation = {corr:+.3f}: ✅")
        passed += 1
    except Exception as e:
        print(f"   |Ψ-⟩ correlation: ❌ {e}")

    # ── Summary ──
    print(f"\n{'=' * 60}")
    print(f"Results: {passed}/{total} tests passed")
    if passed == total:
        print("🎉 All tests passed! Ready for Day 4.")
    else:
        print("💪 Keep working — check solutions.py for hints!")


if __name__ == '__main__':
    run_tests()
