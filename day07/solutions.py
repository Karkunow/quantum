"""
Day 7 Solutions: Quantum Fourier Transform
============================================

14-Day Quantum DevRel Bootcamp

Complete implementations with interview insights.
Only check these AFTER attempting the exercises yourself!
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator
from qiskit_aer import AerSimulator


# ============================================================
# Solution 1: Classical DFT and QFT Matrix
# ============================================================
# 💬 Interview insight: "The QFT is the quantum analog of the
# classical DFT. Classically, the FFT takes O(N log N) operations.
# The QFT circuit uses O(n²) gates on n qubits, which is
# exponentially fewer since N = 2ⁿ. But you can't read out all
# the amplitudes — the speedup is real only when combined with
# algorithms like QPE or Shor's that extract useful information
# from the transformed state."

def classical_dft_matrix(N: int) -> np.ndarray:
    """(DFT)_kj = ω^(jk) / √N where ω = e^(2πi/N).

    💬 "The DFT matrix is symmetric and unitary. Each column is
    a different frequency, and each row samples that frequency
    at a different point. In quantum computing, each column is
    a basis state's image under QFT."
    """
    omega = np.exp(2j * np.pi / N)
    j, k = np.meshgrid(range(N), range(N))
    return omega ** (j * k) / np.sqrt(N)


def qft_matrix(n_qubits: int) -> np.ndarray:
    """QFT matrix = DFT matrix with N = 2ⁿ.

    💬 "The QFT is just the DFT on 2ⁿ amplitudes. What makes it
    quantum is that it acts on superpositions — transforming
    2ⁿ amplitudes simultaneously using only O(n²) gates."
    """
    return classical_dft_matrix(2 ** n_qubits)


def verify_qft_properties(n_qubits: int) -> dict:
    """Verify key mathematical properties of the QFT matrix."""
    N = 2 ** n_qubits
    Q = qft_matrix(n_qubits)

    # 1. Unitarity
    is_unitary = np.allclose(Q @ Q.conj().T, np.eye(N))

    # 2. Symmetry
    is_symmetric = np.allclose(Q, Q.T)

    # 3. QFT⁴ = I (for standard DFT)
    Q4 = np.linalg.matrix_power(Q, 4)
    fourth_power_identity = np.allclose(Q4, np.eye(N))

    # 4. QFT|0⟩ = uniform superposition
    e0 = np.zeros(N, dtype=complex)
    e0[0] = 1
    result = Q @ e0
    is_uniform = np.allclose(np.abs(result), np.ones(N) / np.sqrt(N))

    return {
        'unitary': is_unitary,
        'symmetric': is_symmetric,
        'fourth_power_identity': fourth_power_identity,
        'zero_to_uniform': is_uniform
    }


# ============================================================
# Solution 2: QFT Circuit Construction
# ============================================================
# 💬 Interview insight: "The QFT circuit has a beautiful recursive
# structure. For each qubit: one Hadamard + (n-1) controlled
# rotations, giving n(n+1)/2 total gates. This O(n²) is
# exponentially better than the classical FFT's O(N log N) = O(n·2ⁿ).
# The final SWAPs reverse the bit order — a consequence of the
# big-endian vs little-endian convention."

def qft_circuit(n_qubits: int, swap: bool = True) -> QuantumCircuit:
    """Build the QFT circuit using H and controlled-phase gates.

    💬 "Each controlled-R_k gate adds phase 2π/2^k when both
    qubits are |1⟩. The Hadamard creates the base frequencies,
    and the controlled rotations build up the fine phase structure.
    Think of it as constructing a Fourier series qubit by qubit."
    """
    qc = QuantumCircuit(n_qubits)

    for j in range(n_qubits):
        # Hadamard on qubit j
        qc.h(j)

        # Controlled rotations from subsequent qubits
        for k in range(1, n_qubits - j):
            angle = 2 * np.pi / (2 ** (k + 1))
            qc.cp(angle, j + k, j)

    # Swap qubits to reverse bit order
    if swap:
        for i in range(n_qubits // 2):
            qc.swap(i, n_qubits - 1 - i)

    return qc


def inverse_qft_circuit(n_qubits: int, swap: bool = True) -> QuantumCircuit:
    """QFT† = reverse circuit with negated angles.

    💬 "The inverse QFT undoes the Fourier transform. In QPE,
    we apply controlled-U powers (which encode phase info in
    the Fourier basis), then inverse-QFT to read it out in
    the computational basis."
    """
    return qft_circuit(n_qubits, swap).inverse()


# ============================================================
# Solution 3: QFT on Specific States
# ============================================================
# 💬 Interview insight: "The QFT interconverts between time
# and frequency representations. A state periodic in the
# computational basis transforms to peaks at multiples of N/r
# in the Fourier basis. This is EXACTLY what Shor's algorithm
# exploits: the modular exponentiation creates a periodic state,
# and QPE (which uses QFT) reveals the period."

def qft_on_basis_state(n_qubits: int, j: int) -> Statevector:
    """Apply QFT to |j⟩ and return the resulting statevector.

    QFT|j⟩ = (1/√N) Σ_k e^(2πijk/N) |k⟩

    This shows that the QFT of a basis state is a state where
    all probabilities are equal (1/N), but the phases vary.
    """
    qc = qft_circuit(n_qubits)

    # Prepare |j⟩
    prep = QuantumCircuit(n_qubits)
    for bit_idx in range(n_qubits):
        if (j >> bit_idx) & 1:
            prep.x(bit_idx)

    full_circuit = QuantumCircuit(n_qubits)
    full_circuit.compose(prep, inplace=True)
    full_circuit.compose(qc, inplace=True)

    return Statevector.from_instruction(full_circuit)


def qft_on_periodic_state(n_qubits: int, period: int) -> Statevector:
    """Apply QFT to a periodic state and show frequency peaks.

    Input: uniform over {|0⟩, |r⟩, |2r⟩, ...}
    Output: peaks at multiples of N/r

    💬 "This is the core of Shor's algorithm: periodicity in
    the computational basis becomes peaks in the Fourier basis.
    Read off the peak spacing → get the period → factor the number."
    """
    N = 2 ** n_qubits

    # Build periodic state
    state_vec = np.zeros(N, dtype=complex)
    positions = list(range(0, N, period))
    amplitude = 1.0 / np.sqrt(len(positions))
    for pos in positions:
        state_vec[pos] = amplitude

    # Apply QFT matrix directly
    Q = qft_matrix(n_qubits)
    result_vec = Q @ state_vec

    return Statevector(result_vec)


# ============================================================
# Solution 4: Quantum Phase Estimation (QPE)
# ============================================================
# 💬 Interview insight: "QPE is arguably the most important
# subroutine in quantum computing. It's the engine inside
# Shor's algorithm, quantum chemistry (ground state energy
# estimation), and HHL (linear systems). The precision scales
# as 2^(-n) with n counting qubits, and the circuit depth
# scales polynomially."

def qpe_circuit(unitary: QuantumCircuit | np.ndarray,
                n_counting: int,
                eigenstate: QuantumCircuit | None = None) -> QuantumCircuit:
    """Build the QPE circuit.

    💬 "QPE works by encoding the phase φ as a binary fraction
    in the counting register. The controlled-U^(2^j) operations
    create the state Σ e^(2πi·2^j·φ)|j⟩ in the counting register —
    which is exactly the QFT of the binary representation of φ.
    Applying inverse QFT then reveals φ."
    """
    # Determine target qubit count
    if isinstance(unitary, np.ndarray):
        n_target = int(np.log2(unitary.shape[0]))
        u_gate = Operator(unitary)
    else:
        n_target = unitary.num_qubits
        u_gate = Operator(unitary)

    n_total = n_counting + n_target
    qc = QuantumCircuit(n_total, n_counting)

    # H on counting qubits
    qc.h(range(n_counting))

    # Prepare eigenstate in target register
    if eigenstate is not None:
        qc.compose(eigenstate, qubits=range(n_counting, n_total), inplace=True)

    # Controlled-U^(2^j) for each counting qubit j
    for j in range(n_counting):
        power = 2 ** j
        u_power = u_gate.power(power)
        cu = u_power.to_instruction()
        # Controlled version
        controlled_u = cu.control(1)
        qubits = [j] + list(range(n_counting, n_total))
        qc.append(controlled_u, qubits)

    # Inverse QFT on counting register
    iqft = inverse_qft_circuit(n_counting)
    qc.compose(iqft, qubits=range(n_counting), inplace=True)

    # Measure counting qubits
    qc.measure(range(n_counting), range(n_counting))

    return qc


def estimate_phase(unitary: np.ndarray,
                   eigenstate: np.ndarray,
                   n_counting: int = 4,
                   shots: int = 1024) -> float:
    """Estimate eigenvalue phase using QPE.

    💬 "The most-frequent measurement outcome gives the best
    n-bit approximation to φ. For exact phases (φ = k/2ⁿ),
    QPE gives the exact answer with certainty. For irrational
    phases, you get the nearest binary fraction with high
    probability."
    """
    n_target = int(np.log2(unitary.shape[0]))

    # Build eigenstate preparation circuit
    prep = QuantumCircuit(n_target)
    sv = Statevector(eigenstate)
    prep.initialize(sv)

    # Build and run QPE
    qc = qpe_circuit(unitary, n_counting, prep)
    sim = AerSimulator()
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()

    # Find most frequent outcome
    best_bitstring = max(counts, key=counts.get)

    # Convert to phase: reverse bitstring (Qiskit little-endian),
    # interpret as binary fraction
    measured_int = int(best_bitstring, 2)
    phase = measured_int / (2 ** n_counting)

    return phase


# ============================================================
# Solution 5: QPE Applications
# ============================================================
# 💬 Interview insight: "QPE on the T gate is the 'Hello World'
# of phase estimation — it gives an exact answer because 1/8
# is exactly representable in 3 binary digits. Real applications
# (quantum chemistry, Shor's) deal with phases that aren't
# exact binary fractions, requiring more precision qubits and
# classical post-processing."

def qpe_t_gate(n_counting: int = 3, shots: int = 1024) -> dict:
    """QPE on T|1⟩ = e^(iπ/4)|1⟩ → φ = 1/8.

    💬 "The T gate adds phase π/4 to |1⟩. Since e^(2πi·φ) = e^(iπ/4),
    we get φ = 1/8. With 3 counting qubits, this is exactly
    representable as 0.001 in binary → measurement gives |001⟩
    with certainty."
    """
    T_matrix = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)
    eigenstate = np.array([0, 1], dtype=complex)  # |1⟩

    estimated = estimate_phase(T_matrix, eigenstate, n_counting, shots)

    # Also get full counts
    prep = QuantumCircuit(1)
    prep.x(0)  # Prepare |1⟩
    qc = qpe_circuit(T_matrix, n_counting, prep)
    sim = AerSimulator()
    counts = sim.run(qc, shots=shots).result().get_counts()

    return {
        'estimated_phase': estimated,
        'exact_phase': 1 / 8,
        'counts': counts,
        'error': abs(estimated - 1 / 8)
    }


def qpe_rotation_gate(theta: float, n_counting: int = 4,
                      shots: int = 1024) -> dict:
    """QPE on Rz(θ)|1⟩ = e^(-iθ/2)|1⟩ → φ = 1 - θ/(4π).

    The Rz gate: Rz(θ) = [[e^(-iθ/2), 0], [0, e^(iθ/2)]]
    Actually Qiskit convention: Rz(θ)|1⟩ = e^(iθ/2)|1⟩
    So eigenvalue = e^(2πiφ) = e^(iθ/2) → φ = θ/(4π)
    """
    Rz = np.array([
        [np.exp(-1j * theta / 2), 0],
        [0, np.exp(1j * theta / 2)]
    ], dtype=complex)
    eigenstate = np.array([0, 1], dtype=complex)

    estimated = estimate_phase(Rz, eigenstate, n_counting, shots)

    # Exact phase for |1⟩ eigenvalue
    exact = (theta / (4 * np.pi)) % 1.0

    return {
        'estimated_phase': estimated,
        'exact_phase': exact,
        'error': min(abs(estimated - exact), abs(estimated - exact - 1), abs(estimated - exact + 1)),
        'theta': theta
    }


def shor_connection(N_to_factor: int = 15) -> str:
    """Explain the QPE → Shor's algorithm connection.

    💬 "This is one of the most important explanations in quantum
    computing: why factoring reduces to phase estimation."
    """
    return f"""
Shor's Algorithm and QPE — The Connection
==========================================

Goal: Factor N = {N_to_factor} into its prime factors.

Step 1: REDUCTION TO ORDER FINDING
   Factoring reduces to finding the ORDER r of a random a < N:
   the smallest r such that a^r ≡ 1 (mod N).
   Once r is known, gcd(a^(r/2) ± 1, N) often gives a factor.

Step 2: ORDER FINDING VIA QPE
   Define the modular exponentiation unitary:
     U_a|x⟩ = |ax mod N⟩
   
   The eigenstates of U_a are:
     |u_s⟩ = (1/√r) Σ_k e^(-2πisk/r) |a^k mod N⟩
   
   with eigenvalues e^(2πis/r) for s = 0, 1, ..., r-1.

Step 3: QPE EXTRACTS s/r
   QPE on U_a with eigenstate |u_s⟩ gives an n-bit estimate
   of the phase s/r. Using continued fractions on the measured
   value, we can extract r (the denominator).

Step 4: CLASSICAL POST-PROCESSING
   Given r, compute gcd(a^(r/2) + 1, N) and gcd(a^(r/2) - 1, N).
   With probability ≥ 1/2, one of these is a non-trivial factor.

For N = {N_to_factor}: a = 7, r = 4 (since 7^4 = 2401 ≡ 1 mod 15)
   gcd(7^2 + 1, 15) = gcd(50, 15) = 5  ← factor!
   gcd(7^2 - 1, 15) = gcd(48, 15) = 3  ← factor!
   15 = 3 × 5 ✓

The quantum speedup comes from QPE finding r in O(n²) gates
on O(n) qubits, where n = log₂(N). Classically, the best known
algorithms take sub-exponential time. This is an EXPONENTIAL
quantum speedup — the crown jewel of quantum algorithms.
"""


if __name__ == "__main__":
    print("Day 7 Solutions: Quantum Fourier Transform")
    print("=" * 55)

    # Demo: QFT properties
    print("\n📐 QFT Properties (3 qubits):")
    props = verify_qft_properties(3)
    for prop, val in props.items():
        print(f"  {prop}: {'✓' if val else '✗'}")

    # Demo: QFT circuit
    print("\nQFT Circuit (3 qubits):")
    qc = qft_circuit(3)
    print(qc.draw())

    # Demo: QFT on basis states
    print("\n🔊 QFT on basis states (3 qubits):")
    for j in [0, 1, 4]:
        sv = qft_on_basis_state(3, j)
        probs = np.abs(sv.data) ** 2
        print(f"  QFT|{j:03b}⟩: probs = [{', '.join(f'{p:.3f}' for p in probs)}]")

    # Demo: periodic states
    print("\n📊 QFT on periodic states (3 qubits):")
    for period in [1, 2, 4]:
        sv = qft_on_periodic_state(3, period)
        probs = np.abs(sv.data) ** 2
        peaks = [i for i, p in enumerate(probs) if p > 0.1]
        print(f"  Period={period}: peaks at {[f'|{p:03b}⟩' for p in peaks]}")

    # Demo: QPE
    print("\n⚡ QPE on standard gates:")

    t_result = qpe_t_gate(n_counting=3)
    print(f"  T gate: φ_est = {t_result['estimated_phase']:.4f}, "
          f"exact = {t_result['exact_phase']:.4f}, "
          f"error = {t_result['error']:.4f}")

    for theta in [np.pi / 4, np.pi / 3, np.pi / 2, np.pi]:
        rz_result = qpe_rotation_gate(theta, n_counting=5)
        print(f"  Rz({theta/np.pi:.2f}π): φ_est = {rz_result['estimated_phase']:.4f}, "
              f"exact = {rz_result['exact_phase']:.4f}, "
              f"error = {rz_result['error']:.4f}")

    # Demo: Shor connection
    print("\n" + shor_connection(15))
