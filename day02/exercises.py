"""
Day 2 Exercises: Single Qubit Rotations in Qiskit
===================================================

Today you transition from manual NumPy to Qiskit — IBM's industry-standard
quantum computing SDK. You will:

1. Build circuits with Qiskit's QuantumCircuit
2. Implement rotation gates Rx(θ), Ry(θ), Rz(θ)
3. Understand how rotations relate to the Bloch sphere
4. Build parameterized circuits and sweep angles
5. Verify that your Day 1 manual math matches Qiskit outputs

Remember: You already know the math. Qiskit is just the engineering layer
that talks to real quantum hardware.
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator


# ═══════════════════════════════════════════════════════════════
# EXERCISE 1: Build a Qiskit circuit that prepares |1⟩
# ═══════════════════════════════════════════════════════════════
#
# Qiskit always starts qubits in |0⟩. Your job: apply the right
# gate to flip it to |1⟩.
#
# Hint: Which Pauli gate flips |0⟩ → |1⟩?

def prepare_ket1() -> QuantumCircuit:
    """
    Create a 1-qubit circuit that transforms |0⟩ → |1⟩.
    
    Returns:
        QuantumCircuit with the appropriate gate applied
    """
    qc = QuantumCircuit(1)
    # TODO: Apply the correct gate to qc
    
    return qc


# ═══════════════════════════════════════════════════════════════
# EXERCISE 2: Build a circuit that prepares |+⟩ and |-⟩
# ═══════════════════════════════════════════════════════════════
#
# |+⟩ = (|0⟩ + |1⟩)/√2  — start from |0⟩
# |-⟩ = (|0⟩ - |1⟩)/√2  — start from |1⟩
#
# Think about what gate creates equal superposition.

def prepare_plus() -> QuantumCircuit:
    """Create a circuit that prepares |+⟩ from |0⟩."""
    qc = QuantumCircuit(1)
    # TODO: Apply gate(s) to prepare |+⟩
    
    return qc


def prepare_minus() -> QuantumCircuit:
    """Create a circuit that prepares |-⟩ from |0⟩."""
    qc = QuantumCircuit(1)
    # TODO: Apply gate(s) to prepare |-⟩
    # Hint: You need TWO gates. First go to |1⟩, then...
    
    return qc


# ═══════════════════════════════════════════════════════════════
# EXERCISE 3: Verify rotation gate matrices
# ═══════════════════════════════════════════════════════════════
#
# The three rotation gates are:
#
#   Rx(θ) = exp(-iθX/2) = cos(θ/2)I - i·sin(θ/2)X
#   Ry(θ) = exp(-iθY/2) = cos(θ/2)I - i·sin(θ/2)Y
#   Rz(θ) = exp(-iθZ/2) = cos(θ/2)I - i·sin(θ/2)Z
#
# Build the matrix MANUALLY using NumPy, then compare it to
# Qiskit's version using Operator.

def manual_rx(theta: float) -> np.ndarray:
    """
    Build Rx(θ) matrix manually.
    
    Rx(θ) = [[cos(θ/2),    -i·sin(θ/2)],
             [-i·sin(θ/2),  cos(θ/2)   ]]
    
    Args:
        theta: Rotation angle in radians
        
    Returns:
        2x2 complex numpy array
    """
    # TODO: Implement the Rx matrix
    pass


def manual_ry(theta: float) -> np.ndarray:
    """
    Build Ry(θ) matrix manually.
    
    Ry(θ) = [[cos(θ/2),  -sin(θ/2)],
             [sin(θ/2),   cos(θ/2)]]
    
    Args:
        theta: Rotation angle in radians
        
    Returns:
        2x2 complex numpy array
    """
    # TODO: Implement the Ry matrix
    pass


def manual_rz(theta: float) -> np.ndarray:
    """
    Build Rz(θ) matrix manually.
    
    Rz(θ) = [[exp(-iθ/2),  0         ],
             [0,            exp(iθ/2) ]]
    
    Args:
        theta: Rotation angle in radians
        
    Returns:
        2x2 complex numpy array
    """
    # TODO: Implement the Rz matrix
    pass


# ═══════════════════════════════════════════════════════════════
# EXERCISE 4: Decompose Hadamard into rotations
# ═══════════════════════════════════════════════════════════════
#
# Any single-qubit gate can be written as rotations!
#
# H = Ry(π/2) · Rz(π)   (up to global phase)
#
# or equivalently:
# H = e^(iπ/4) · Rz(π/2) · Ry(π/2) · Rz(π/2)
#
# Build a circuit using ONLY rotation gates (rx, ry, rz)
# that acts the same as a Hadamard gate.

def hadamard_from_rotations() -> QuantumCircuit:
    """
    Construct Hadamard-equivalent circuit using only rotation gates.
    
    The result should satisfy: U|0⟩ = |+⟩ (up to global phase)
    
    Returns:
        QuantumCircuit using only rx, ry, rz gates
    """
    qc = QuantumCircuit(1)
    # TODO: Apply rotation gates that compose to Hadamard
    # Hint: Ry(π/2) followed by Rz(π) works!
    
    return qc


# ═══════════════════════════════════════════════════════════════
# EXERCISE 5: Parameterized state preparation
# ═══════════════════════════════════════════════════════════════
#
# Create a circuit that prepares an ARBITRARY qubit state
# given Bloch sphere angles θ and φ:
#
#   |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)·sin(θ/2)|1⟩
#
# This is the most general single-qubit state.

def prepare_arbitrary_state(theta: float, phi: float) -> QuantumCircuit:
    """
    Prepare |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩ using rotations.
    
    Starting from |0⟩:
    1. Ry(θ) rotates to cos(θ/2)|0⟩ + sin(θ/2)|1⟩
    2. Rz(φ) adds the phase: cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩
       (Rz adds relative phase between |0⟩ and |1⟩)
    
    Note: Rz also adds a global phase e^(-iφ/2), but global phase
    is physically unobservable!
    
    Args:
        theta: Polar angle [0, π]
        phi: Azimuthal angle [0, 2π)
        
    Returns:
        QuantumCircuit that prepares the state
    """
    qc = QuantumCircuit(1)
    # TODO: Apply rotation gates to prepare the arbitrary state
    
    return qc


# ═══════════════════════════════════════════════════════════════
# TEST SUITE
# ═══════════════════════════════════════════════════════════════

def run_tests():
    """Run all exercise tests."""
    print("🧪 Day 2 Exercise Tests")
    print("=" * 60)
    passed = 0
    total = 0
    
    # Test 1: Prepare |1⟩
    total += 1
    print("\n📝 Exercise 1: Prepare |1⟩")
    try:
        qc = prepare_ket1()
        sv = Statevector.from_instruction(qc)
        expected = Statevector([0, 1])
        if sv.equiv(expected):
            print("   ✅ PASSED — Circuit correctly prepares |1⟩")
            passed += 1
        else:
            print(f"   ❌ FAILED — Got {sv}, expected |1⟩ = [0, 1]")
    except Exception as e:
        print(f"   ❌ ERROR — {e}")
    
    # Test 2a: Prepare |+⟩
    total += 1
    print("\n📝 Exercise 2a: Prepare |+⟩")
    try:
        qc = prepare_plus()
        sv = Statevector.from_instruction(qc)
        expected = Statevector([1/np.sqrt(2), 1/np.sqrt(2)])
        if sv.equiv(expected):
            print("   ✅ PASSED — Circuit correctly prepares |+⟩")
            passed += 1
        else:
            print(f"   ❌ FAILED — Got {sv}, expected |+⟩")
    except Exception as e:
        print(f"   ❌ ERROR — {e}")
    
    # Test 2b: Prepare |-⟩
    total += 1
    print("\n📝 Exercise 2b: Prepare |-⟩")
    try:
        qc = prepare_minus()
        sv = Statevector.from_instruction(qc)
        expected = Statevector([1/np.sqrt(2), -1/np.sqrt(2)])
        if sv.equiv(expected):
            print("   ✅ PASSED — Circuit correctly prepares |-⟩")
            passed += 1
        else:
            print(f"   ❌ FAILED — Got {sv}, expected |-⟩")
    except Exception as e:
        print(f"   ❌ ERROR — {e}")
    
    # Test 3: Rotation matrices match Qiskit
    total += 1
    print("\n📝 Exercise 3: Rotation matrices match Qiskit")
    try:
        test_angle = np.pi / 3
        
        # Rx
        qc_rx = QuantumCircuit(1); qc_rx.rx(test_angle, 0)
        qiskit_rx = Operator(qc_rx).data
        my_rx = manual_rx(test_angle)
        rx_ok = np.allclose(my_rx, qiskit_rx)
        
        # Ry
        qc_ry = QuantumCircuit(1); qc_ry.ry(test_angle, 0)
        qiskit_ry = Operator(qc_ry).data
        my_ry = manual_ry(test_angle)
        ry_ok = np.allclose(my_ry, qiskit_ry)
        
        # Rz
        qc_rz = QuantumCircuit(1); qc_rz.rz(test_angle, 0)
        qiskit_rz = Operator(qc_rz).data
        my_rz = manual_rz(test_angle)
        rz_ok = np.allclose(my_rz, qiskit_rz)
        
        if rx_ok and ry_ok and rz_ok:
            print("   ✅ PASSED — All rotation matrices match Qiskit")
            passed += 1
        else:
            if not rx_ok: print("   ❌ Rx mismatch")
            if not ry_ok: print("   ❌ Ry mismatch")
            if not rz_ok: print("   ❌ Rz mismatch")
    except Exception as e:
        print(f"   ❌ ERROR — {e}")
    
    # Test 4: Hadamard from rotations
    total += 1
    print("\n📝 Exercise 4: Hadamard from rotations")
    try:
        qc = hadamard_from_rotations()
        sv = Statevector.from_instruction(qc)
        expected = Statevector([1/np.sqrt(2), 1/np.sqrt(2)])
        if sv.equiv(expected):
            print("   ✅ PASSED — Rotation circuit acts as Hadamard on |0⟩")
            passed += 1
        else:
            print(f"   ❌ FAILED — Got {sv}, expected |+⟩")
    except Exception as e:
        print(f"   ❌ ERROR — {e}")
    
    # Test 5: Arbitrary state preparation
    total += 1
    print("\n📝 Exercise 5: Arbitrary state preparation")
    try:
        test_cases = [
            (0, 0, "|0⟩"),               # North pole
            (np.pi, 0, "|1⟩"),            # South pole
            (np.pi/2, 0, "|+⟩"),          # +X axis
            (np.pi/2, np.pi, "|-⟩"),      # -X axis
            (np.pi/2, np.pi/2, "|+i⟩"),   # +Y axis
        ]
        
        all_ok = True
        for theta, phi, name in test_cases:
            qc = prepare_arbitrary_state(theta, phi)
            sv = Statevector.from_instruction(qc)
            
            # Expected state
            expected_vec = np.array([
                np.cos(theta/2),
                np.exp(1j * phi) * np.sin(theta/2)
            ])
            expected = Statevector(expected_vec)
            
            if sv.equiv(expected):
                print(f"   ✅ θ={theta:.2f}, φ={phi:.2f} → {name}")
            else:
                print(f"   ❌ θ={theta:.2f}, φ={phi:.2f} → Expected {name}, got {sv}")
                all_ok = False
        
        if all_ok:
            passed += 1
    except Exception as e:
        print(f"   ❌ ERROR — {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} exercises passed")
    if passed == total:
        print("🎉 ALL EXERCISES COMPLETE! You're ready for Day 3!")
    else:
        print(f"📝 {total - passed} exercise(s) remaining. Keep going!")
    
    return passed, total


if __name__ == "__main__":
    run_tests()
