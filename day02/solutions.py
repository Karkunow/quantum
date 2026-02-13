"""
Day 2 Solutions: Single Qubit Rotations in Qiskit
===================================================

Complete reference implementations with detailed explanations.
Try to solve exercises.py first before looking here!
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator


# ═══════════════════════════════════════════════════════════════
# SOLUTION 1: Prepare |1⟩
# ═══════════════════════════════════════════════════════════════

def prepare_ket1() -> QuantumCircuit:
    """
    X gate (Pauli-X) flips |0⟩ → |1⟩.
    
    In Qiskit, all qubits start in |0⟩.
    The X gate is the quantum NOT gate:
    
        X = [[0, 1],
             [1, 0]]
    
    X|0⟩ = |1⟩  ✓
    """
    qc = QuantumCircuit(1)
    qc.x(0)
    return qc


# ═══════════════════════════════════════════════════════════════
# SOLUTION 2: Prepare |+⟩ and |-⟩
# ═══════════════════════════════════════════════════════════════

def prepare_plus() -> QuantumCircuit:
    """
    Hadamard gate on |0⟩ gives |+⟩.
    
    H|0⟩ = (|0⟩ + |1⟩)/√2 = |+⟩
    """
    qc = QuantumCircuit(1)
    qc.h(0)
    return qc


def prepare_minus() -> QuantumCircuit:
    """
    First flip to |1⟩ with X, then Hadamard gives |-⟩.
    
    X|0⟩ = |1⟩
    H|1⟩ = (|0⟩ - |1⟩)/√2 = |-⟩
    
    Why two gates? Because H|0⟩ = |+⟩ (positive superposition)
    and H|1⟩ = |-⟩ (negative superposition). The minus sign
    in |-⟩ comes from starting in |1⟩.
    """
    qc = QuantumCircuit(1)
    qc.x(0)   # |0⟩ → |1⟩
    qc.h(0)   # |1⟩ → |-⟩
    return qc


# ═══════════════════════════════════════════════════════════════
# SOLUTION 3: Rotation matrices
# ═══════════════════════════════════════════════════════════════

def manual_rx(theta: float) -> np.ndarray:
    """
    Rx(θ) = exp(-iθX/2) — rotation about X-axis on the Bloch sphere.
    
    Rx(θ) = cos(θ/2)·I - i·sin(θ/2)·X
    
          = [[cos(θ/2),    -i·sin(θ/2)],
             [-i·sin(θ/2),  cos(θ/2)   ]]
    
    Physical meaning:
    - Rx(π) = -iX (equivalent to X gate up to global phase)
    - Rx(π/2) rotates |0⟩ halfway toward |1⟩ on the Bloch sphere
      going through the +Y/−Y direction
    
    Key insight: Rx rotates AROUND the X-axis. So states ON the
    X-axis (|+⟩ and |-⟩) are unchanged by Rx!
    """
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([
        [c,      -1j * s],
        [-1j * s, c      ]
    ], dtype=complex)


def manual_ry(theta: float) -> np.ndarray:
    """
    Ry(θ) = exp(-iθY/2) — rotation about Y-axis on the Bloch sphere.
    
    Ry(θ) = cos(θ/2)·I - i·sin(θ/2)·Y
    
          = [[cos(θ/2),  -sin(θ/2)],
             [sin(θ/2),   cos(θ/2)]]
    
    NOTE: Ry is special — its matrix entries are ALL REAL!
    This is because Y = [[0,-i],[i,0]], and -i·Y = [[0,-1],[1,0]] is real.
    
    Physical meaning:
    - Ry(π) = -iY ≡ Y (bit+phase flip, up to global phase)
    - Ry(π/2) on |0⟩ → (|0⟩ + |1⟩)/√2 = |+⟩ (creates superposition!)
    
    Ry is often preferred for state preparation because it keeps
    amplitudes real, avoiding unnecessary phase complications.
    """
    c = np.cos(theta / 2)
    s = np.sin(theta / 2)
    return np.array([
        [c,  -s],
        [s,   c]
    ], dtype=complex)


def manual_rz(theta: float) -> np.ndarray:
    """
    Rz(θ) = exp(-iθZ/2) — rotation about Z-axis on the Bloch sphere.
    
    Rz(θ) = cos(θ/2)·I - i·sin(θ/2)·Z
    
          = [[exp(-iθ/2),  0          ],
             [0,            exp(iθ/2) ]]
    
    Physical meaning:
    - Rz(π) = -iZ ≡ Z (phase flip, up to global phase)
    - Rz changes the PHASE without changing measurement probabilities
      in the Z-basis (computational basis)
    
    Key insight: Rz rotates AROUND the Z-axis. So |0⟩ and |1⟩
    (which sit on the Z-axis) only pick up global phases under Rz.
    States on the equator (like |+⟩, |-⟩, |+i⟩) rotate around.
    """
    return np.array([
        [np.exp(-1j * theta / 2), 0],
        [0, np.exp(1j * theta / 2)]
    ], dtype=complex)


# ═══════════════════════════════════════════════════════════════
# SOLUTION 4: Hadamard from rotations
# ═══════════════════════════════════════════════════════════════

def hadamard_from_rotations() -> QuantumCircuit:
    """
    Decompose H into rotation gates.
    
    The Hadamard can be written as:
    
        H = Rz(π) · Ry(π/2)   (up to global phase)
    
    Let's verify:
    
    Ry(π/2)|0⟩ = cos(π/4)|0⟩ + sin(π/4)|1⟩
                = (|0⟩ + |1⟩)/√2 = |+⟩
    
    Rz(π)|+⟩ = e^(-iπ/2)|0⟩·(1/√2) + e^(iπ/2)|1⟩·(1/√2)
             = -i(|0⟩ + (-1)|1⟩)/√2
             = -i|+⟩ ... wait, that's not right.
    
    Actually, the correct decomposition is:
    
        H = Ry(π/2) · Rz(π)
    
    Remember: In Qiskit, gates are applied LEFT TO RIGHT in code,
    but RIGHT TO LEFT in matrix multiplication!
    
    So: qc.rz(π) then qc.ry(π/2) means the matrix is Ry(π/2)·Rz(π).
    
    This equals H up to a global phase of i.
    """
    qc = QuantumCircuit(1)
    qc.rz(np.pi, 0)      # First: Rz(π)
    qc.ry(np.pi / 2, 0)  # Then: Ry(π/2)
    # Matrix = Ry(π/2) · Rz(π) ≡ H (up to global phase)
    return qc


# ═══════════════════════════════════════════════════════════════
# SOLUTION 5: Arbitrary state preparation
# ═══════════════════════════════════════════════════════════════

def prepare_arbitrary_state(theta: float, phi: float) -> QuantumCircuit:
    """
    Prepare |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩.
    
    Strategy: Use Ry for the polar angle and Rz for the azimuthal phase.
    
    Step 1: Ry(θ)|0⟩ = cos(θ/2)|0⟩ + sin(θ/2)|1⟩
            This puts us at the right latitude on the Bloch sphere.
    
    Step 2: Rz(φ) adds relative phase between |0⟩ and |1⟩:
            Rz(φ)|ψ⟩ = e^(-iφ/2)cos(θ/2)|0⟩ + e^(iφ/2)sin(θ/2)|1⟩
    
    The relative phase between components is e^(iφ), which is correct!
    The overall e^(-iφ/2) factor is a global phase — physically unobservable.
    
    WHY THIS MATTERS:
    This is the U3 gate idea! Any single-qubit state can be reached
    from |0⟩ with just Ry and Rz. This is the basis for single-qubit
    transpilation on real quantum hardware.
    """
    qc = QuantumCircuit(1)
    qc.ry(theta, 0)   # Set polar angle (latitude)
    qc.rz(phi, 0)     # Set azimuthal phase (longitude)
    return qc


# ═══════════════════════════════════════════════════════════════
# DEEPER EXPLANATION: Why Rotations Are Everything
# ═══════════════════════════════════════════════════════════════
"""
THE EULER DECOMPOSITION THEOREM (for SU(2)):

Any single-qubit unitary U can be written as:

    U = e^(iα) · Rz(β) · Ry(γ) · Rz(δ)

where α, β, γ, δ are real numbers.

This means:
1. Only TWO types of rotation (Ry, Rz) are needed for ANY single-qubit gate
2. Hardware only needs to implement Ry and Rz physically
3. This is the ZYZ decomposition — the standard in quantum compilers

IBM quantum hardware natively supports:
    - Rz(θ) — implemented as a "virtual gate" (just frame change, zero error!)
    - √X (= Rx(π/2)) — physical microwave pulse
    - X (= Rx(π)) — physical microwave pulse

So when you write `qc.h(0)`, the transpiler decomposes it into
the native gate set automatically. Understanding this decomposition
is crucial for optimizing circuits for real hardware.


ROTATION GATES vs PAULI GATES — THE CONNECTION:

    Rx(π) = -iX    (X gate up to global phase)
    Ry(π) = -iY    (Y gate up to global phase)
    Rz(π) = -iZ    (Z gate up to global phase)

So Pauli gates are just π-rotations! This is deeply geometric:
a π rotation around any axis on the Bloch sphere is a 180° flip.


INTERVIEW QUESTION YOU SHOULD BE ABLE TO ANSWER:

Q: "How does IBM quantum hardware implement arbitrary single-qubit gates?"

A: "IBM uses the ZYZ Euler decomposition. Any single-qubit gate U can be
    decomposed as Rz(β)·Ry(γ)·Rz(δ) up to a global phase. On the hardware,
    Rz is a virtual gate (frame change in software, zero physical error),
    and Ry is implemented using √X pulses and Rz combinations. This means
    single-qubit gates are essentially free in terms of error — the expensive
    operations are two-qubit gates like CNOT."
"""


if __name__ == "__main__":
    print("=" * 60)
    print("Day 2 Solutions — Running verification")
    print("=" * 60)
    
    # Verify all solutions
    print("\n1. Prepare |1⟩")
    sv = Statevector.from_instruction(prepare_ket1())
    print(f"   Result: {sv}")
    
    print("\n2a. Prepare |+⟩")
    sv = Statevector.from_instruction(prepare_plus())
    print(f"   Result: {sv}")
    
    print("\n2b. Prepare |-⟩")
    sv = Statevector.from_instruction(prepare_minus())
    print(f"   Result: {sv}")
    
    print("\n3. Rotation matrices (θ = π/3)")
    theta = np.pi / 3
    
    qc_rx = QuantumCircuit(1); qc_rx.rx(theta, 0)
    print(f"   Rx match: {np.allclose(manual_rx(theta), Operator(qc_rx).data)}")
    
    qc_ry = QuantumCircuit(1); qc_ry.ry(theta, 0)
    print(f"   Ry match: {np.allclose(manual_ry(theta), Operator(qc_ry).data)}")
    
    qc_rz = QuantumCircuit(1); qc_rz.rz(theta, 0)
    print(f"   Rz match: {np.allclose(manual_rz(theta), Operator(qc_rz).data)}")
    
    print("\n4. Hadamard from rotations")
    sv = Statevector.from_instruction(hadamard_from_rotations())
    expected = Statevector([1/np.sqrt(2), 1/np.sqrt(2)])
    print(f"   Result: {sv}")
    print(f"   Equivalent to |+⟩: {sv.equiv(expected)}")
    
    print("\n5. Arbitrary states")
    test_cases = [
        (0, 0, "|0⟩"),
        (np.pi, 0, "|1⟩"),
        (np.pi/2, 0, "|+⟩"),
        (np.pi/2, np.pi, "|-⟩"),
        (np.pi/2, np.pi/2, "|+i⟩"),
    ]
    for theta, phi, name in test_cases:
        qc = prepare_arbitrary_state(theta, phi)
        sv = Statevector.from_instruction(qc)
        expected_vec = np.array([np.cos(theta/2), np.exp(1j*phi)*np.sin(theta/2)])
        ok = sv.equiv(Statevector(expected_vec))
        print(f"   θ={theta:.2f}, φ={phi:.2f} → {name}: {'✅' if ok else '❌'}")
