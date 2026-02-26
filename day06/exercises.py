"""
Day 6 Exercises: Grover's Search Algorithm
===========================================

14-Day Quantum DevRel Bootcamp

Today's exercises cover:
1. Oracle construction for marked states
2. Diffusion (Grover) operator implementation
3. Full Grover's algorithm circuit
4. Multi-solution Grover search
5. Optimal iteration count analysis

Run this file to test your implementations:
    python day06/exercises.py
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator
from qiskit_aer import AerSimulator


# ============================================================
# Exercise 1: Oracle Construction
# ============================================================
# In Grover's algorithm, the oracle Oₓ flips the phase of the
# target state(s):
#
#   Oₓ|x⟩ = -|x⟩   if x is a marked (target) state
#   Oₓ|x⟩ =  |x⟩   otherwise
#
# This is a diagonal matrix with -1 entries for each marked state
# and +1 elsewhere.  For n qubits and marked state |w⟩:
#
#   Oₓ = I - 2|w⟩⟨w|
#
# For multiple marked states {w₁, w₂, ...}:
#   Oₓ = I - 2 Σᵢ |wᵢ⟩⟨wᵢ|

def build_oracle_matrix(n_qubits: int, marked_states: list[int]) -> np.ndarray:
    """Build the oracle matrix for given marked states.

    The oracle flips the phase of marked computational basis states.

    Args:
        n_qubits: Number of qubits
        marked_states: List of integer indices of marked states
                       (e.g. [5] means |101⟩ for 3 qubits)

    Returns:
        2ⁿ × 2ⁿ diagonal unitary matrix

    Example:
        build_oracle_matrix(2, [3]) flips phase of |11⟩:
        diag(1, 1, 1, -1)
    """
    # TODO: Build a 2ⁿ × 2ⁿ identity matrix
    # TODO: Set diagonal entries to -1 for each marked state
    pass


def build_oracle_circuit(n_qubits: int, marked_states: list[int]) -> QuantumCircuit:
    """Build a Qiskit QuantumCircuit implementing the phase oracle.

    For a single marked state, one approach:
      1. Apply X gates to qubits that are |0⟩ in the binary
         representation of the marked state
      2. Apply a multi-controlled Z gate (all controls on, target Z)
      3. Undo the X gates from step 1

    For multiple marked states, compose oracles or use the
    unitary matrix approach.

    Args:
        n_qubits: Number of qubits
        marked_states: List of integer indices of marked states

    Returns:
        QuantumCircuit implementing the oracle

    Hint: For the multi-controlled Z, use:
        qc.h(target)
        qc.mcx(controls, target)   # multi-controlled X = Toffoli generalisation
        qc.h(target)
    This gives controlled-Z because HXH = Z.
    """
    # TODO: Build the oracle circuit
    # Hint: For each marked state, flip X on qubits where bit is 0,
    #       apply MCZ, then unflip.
    pass


# ============================================================
# Exercise 2: Diffusion Operator
# ============================================================
# The diffusion operator (Grover's operator) reflects about the
# uniform superposition |s⟩ = H⊗ⁿ|0⟩ⁿ:
#
#   D = 2|s⟩⟨s| - I
#
# In circuit form:
#   1. Apply H⊗ⁿ
#   2. Apply conditional phase flip: 2|0⟩⟨0| - I
#      (flip phase of everything EXCEPT |00...0⟩)
#   3. Apply H⊗ⁿ
#
# The "phase flip about |0⟩" subcircuit:
#   - Apply X to all qubits
#   - Apply multi-controlled Z
#   - Apply X to all qubits

def build_diffusion_matrix(n_qubits: int) -> np.ndarray:
    """Build the diffusion operator matrix D = 2|s⟩⟨s| - I.

    |s⟩ = (1/√N) Σ|x⟩ is the uniform superposition.

    Args:
        n_qubits: Number of qubits

    Returns:
        2ⁿ × 2ⁿ unitary matrix
    """
    # TODO: Build |s⟩ = uniform superposition vector
    # TODO: Return 2|s⟩⟨s| - I
    pass


def build_diffusion_circuit(n_qubits: int) -> QuantumCircuit:
    """Build a QuantumCircuit implementing the diffusion operator.

    Steps:
        1. H on all qubits
        2. X on all qubits
        3. Multi-controlled Z (on last qubit)
        4. X on all qubits
        5. H on all qubits

    Args:
        n_qubits: Number of qubits

    Returns:
        QuantumCircuit implementing diffusion
    """
    # TODO: Implement the diffusion circuit
    pass


# ============================================================
# Exercise 3: Complete Grover's Algorithm
# ============================================================
# Grover's algorithm:
#   1. Initialise: |ψ₀⟩ = H⊗ⁿ|0⟩ⁿ  (uniform superposition)
#   2. Repeat k times:
#      a. Apply oracle Oₓ
#      b. Apply diffusion D
#   3. Measure
#
# Optimal iteration count for M marked states out of N = 2ⁿ:
#
#   k_opt = round(π/(4·arcsin(√(M/N))) - 1/2)
#
# For M = 1: k_opt ≈ π√N/4

def optimal_iterations(n_qubits: int, n_marked: int = 1) -> int:
    """Calculate the optimal number of Grover iterations.

    Uses the formula: k = round(π/(4·arcsin(√(M/N))) - 1/2)

    Args:
        n_qubits: Number of qubits (N = 2ⁿ)
        n_marked: Number of marked states (M)

    Returns:
        Optimal number of iterations (integer ≥ 1)
    """
    # TODO: Compute and return optimal iteration count
    pass


def grover_circuit(n_qubits: int, marked_states: list[int],
                   n_iterations: int | None = None) -> QuantumCircuit:
    """Build the complete Grover's algorithm circuit.

    Args:
        n_qubits: Number of qubits
        marked_states: List of marked state indices
        n_iterations: Number of Grover iterations
                      (if None, use optimal_iterations)

    Returns:
        QuantumCircuit with measurement gates
    """
    # TODO: 1. Create circuit, apply H to all qubits
    # TODO: 2. Determine iteration count
    # TODO: 3. Loop: apply oracle then diffusion
    # TODO: 4. Add measurements
    pass


def run_grover(n_qubits: int, marked_states: list[int],
               n_iterations: int | None = None,
               shots: int = 1024) -> dict[str, int]:
    """Run Grover's algorithm and return measurement counts.

    Args:
        n_qubits: Number of qubits
        marked_states: Marked state indices
        n_iterations: Grover iterations (None = optimal)
        shots: Number of measurement shots

    Returns:
        Dictionary of bitstring → count
    """
    # TODO: Build circuit, simulate with AerSimulator, return counts
    pass


# ============================================================
# Exercise 4: Amplitude Amplification Analysis
# ============================================================
# After k iterations of Grover's algorithm, the probability of
# measuring a marked state is:
#
#   P(k) = sin²((2k + 1)·θ)
#
# where sin²(θ) = M/N  (M marked states, N = 2ⁿ total)
#
# This shows the "rotation in the 2D subspace" picture:
#   - |w⟩ = superposition of marked states
#   - |w⊥⟩ = superposition of unmarked states
#   - Each iteration rotates by 2θ toward |w⟩

def success_probability(n_qubits: int, n_marked: int,
                        k_iterations: int) -> float:
    """Calculate the theoretical success probability after k iterations.

    P(k) = sin²((2k + 1)·θ)  where  sin²(θ) = M/N

    Args:
        n_qubits: Number of qubits (N = 2ⁿ)
        n_marked: Number of marked states (M)
        k_iterations: Number of Grover iterations

    Returns:
        Probability of measuring a marked state
    """
    # TODO: Compute θ from M/N, then return sin²((2k+1)θ)
    pass


def amplitude_evolution(n_qubits: int, marked_states: list[int],
                        max_iterations: int) -> list[dict]:
    """Track amplitude evolution through Grover iterations.

    For each iteration k from 0 to max_iterations, record:
    - Probability of marked states
    - Probability of unmarked states
    - Statevector amplitudes for all basis states

    Args:
        n_qubits: Number of qubits
        marked_states: Marked state indices
        max_iterations: Maximum iterations to track

    Returns:
        List of dicts with keys:
            'iteration': int
            'p_marked': float (total probability of marked states)
            'p_unmarked': float
            'amplitudes': list of complex amplitudes
    """
    # TODO: Build circuit incrementally, computing statevector at each step
    # Hint: Start with H⊗ⁿ|0⟩, then repeatedly apply oracle + diffusion
    pass


# ============================================================
# Exercise 5: Multi-Solution Grover & Classical Comparison
# ============================================================
# When M > 1 marked states exist:
#   - Fewer iterations needed: k ∝ √(N/M)
#   - Each marked state gets roughly equal probability
#
# Classical search: expected N/M queries to find a marked item
# Grover search:   ≈ π√(N/M)/4 queries  →  quadratic speedup

def classical_vs_quantum_queries(n_qubits: int, n_marked: int) -> dict:
    """Compare classical and quantum query counts.

    Classical: expected N/M queries (linear search)
    Quantum:   ≈ (π/4)√(N/M) queries (Grover)

    Args:
        n_qubits: Number of qubits (N = 2ⁿ)
        n_marked: Number of marked items (M)

    Returns:
        Dict with keys:
            'N': total items
            'M': marked items
            'classical_expected': expected classical queries
            'quantum_iterations': optimal Grover iterations
            'speedup': classical / quantum ratio
    """
    # TODO: Calculate and return comparison dict
    pass


def multi_solution_grover(n_qubits: int, marked_states: list[int],
                          shots: int = 2048) -> dict:
    """Run Grover with multiple marked states and analyze results.

    Args:
        n_qubits: Number of qubits
        marked_states: List of marked state indices
        shots: Number of shots

    Returns:
        Dict with keys:
            'counts': measurement counts dict
            'marked_total': total counts for marked states
            'unmarked_total': total counts for unmarked states
            'success_rate': fraction of marked state measurements
            'n_iterations': number of iterations used
    """
    # TODO: Run Grover, analyze success rate for marked vs unmarked
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

    # ── Exercise 1: Oracle Construction ──
    print("\n📝 Exercise 1: Oracle Construction")

    oracle_mat = build_oracle_matrix(2, [3])
    if oracle_mat is not None:
        check("Oracle is 4×4", oracle_mat.shape == (4, 4))
        check("Oracle flips |11⟩ phase", oracle_mat[3, 3] == -1)
        check("Oracle preserves |00⟩", oracle_mat[0, 0] == 1)
        check("Oracle is unitary",
              np.allclose(oracle_mat @ oracle_mat.conj().T, np.eye(4)))
    else:
        check("build_oracle_matrix implemented", False)

    oracle_mat_2 = build_oracle_matrix(3, [0, 7])
    if oracle_mat_2 is not None:
        check("Multi-marked oracle: |000⟩ flipped", oracle_mat_2[0, 0] == -1)
        check("Multi-marked oracle: |111⟩ flipped", oracle_mat_2[7, 7] == -1)
        check("Multi-marked oracle: |001⟩ preserved", oracle_mat_2[1, 1] == 1)
    else:
        check("build_oracle_matrix (multi) implemented", False)

    oracle_circ = build_oracle_circuit(2, [3])
    if oracle_circ is not None:
        check("Oracle circuit is QuantumCircuit",
              isinstance(oracle_circ, QuantumCircuit))
        # Verify it matches the matrix
        op = Operator(oracle_circ)
        target_op = Operator(np.diag([1, 1, 1, -1]))
        check("Oracle circuit matches expected unitary",
              op.equiv(target_op))
    else:
        check("build_oracle_circuit implemented", False)

    # ── Exercise 2: Diffusion Operator ──
    print("\n📝 Exercise 2: Diffusion Operator")

    diff_mat = build_diffusion_matrix(2)
    if diff_mat is not None:
        N = 4
        s = np.ones(N) / np.sqrt(N)
        expected = 2 * np.outer(s, s) - np.eye(N)
        check("Diffusion matrix shape", diff_mat.shape == (4, 4))
        check("Diffusion matrix correct",
              np.allclose(diff_mat, expected))
        check("Diffusion is unitary",
              np.allclose(diff_mat @ diff_mat.conj().T, np.eye(N)))
    else:
        check("build_diffusion_matrix implemented", False)

    diff_circ = build_diffusion_circuit(2)
    if diff_circ is not None:
        check("Diffusion circuit is QuantumCircuit",
              isinstance(diff_circ, QuantumCircuit))
        op = Operator(diff_circ)
        N = 4
        s = np.ones(N) / np.sqrt(N)
        expected = 2 * np.outer(s, s) - np.eye(N)
        check("Diffusion circuit matches matrix",
              op.equiv(Operator(expected)))
    else:
        check("build_diffusion_circuit implemented", False)

    # ── Exercise 3: Complete Grover's Algorithm ──
    print("\n📝 Exercise 3: Complete Grover's Algorithm")

    k = optimal_iterations(2, 1)
    if k is not None:
        check("2-qubit optimal iterations = 1", k == 1)
    else:
        check("optimal_iterations implemented", False)

    k3 = optimal_iterations(3, 1)
    if k3 is not None:
        check("3-qubit optimal iterations = 2", k3 == 2)
    else:
        check("optimal_iterations (3q) implemented", False)

    counts = run_grover(2, [3], shots=1024)
    if counts is not None:
        total = sum(counts.values())
        check("Grover returns correct shots", total == 1024)
        # |11⟩ should be dominant
        target_count = counts.get('11', 0)
        check("2-qubit Grover: |11⟩ dominant (>90%)",
              target_count / total > 0.90)
    else:
        check("run_grover implemented", False)

    counts3 = run_grover(3, [5], shots=1024)
    if counts3 is not None:
        target_count = counts3.get('101', 0)
        total = sum(counts3.values())
        check("3-qubit Grover: |101⟩ dominant (>80%)",
              target_count / total > 0.80)
    else:
        check("run_grover (3q) implemented", False)

    # ── Exercise 4: Amplitude Amplification ──
    print("\n📝 Exercise 4: Amplitude Amplification")

    p = success_probability(2, 1, 1)
    if p is not None:
        check("2-qubit, 1 iter: P ≈ 1.0", abs(p - 1.0) < 0.05)
    else:
        check("success_probability implemented", False)

    p_0 = success_probability(3, 1, 0)
    if p_0 is not None:
        check("0 iterations: P = 1/N", abs(p_0 - 1 / 8) < 0.01)
    else:
        check("success_probability (k=0) implemented", False)

    evolution = amplitude_evolution(2, [3], 4)
    if evolution is not None:
        check("Evolution has 5 entries (k=0..4)", len(evolution) == 5)
        check("k=0: uniform distribution",
              abs(evolution[0]['p_marked'] - 0.25) < 0.01)
        check("k=1: near certainty",
              evolution[1]['p_marked'] > 0.95)
    else:
        check("amplitude_evolution implemented", False)

    # ── Exercise 5: Multi-Solution & Classical Comparison ──
    print("\n📝 Exercise 5: Multi-Solution & Classical Comparison")

    comparison = classical_vs_quantum_queries(4, 1)
    if comparison is not None:
        check("N = 16", comparison['N'] == 16)
        check("Classical: 16 queries", comparison['classical_expected'] == 16)
        check("Quantum speedup > 1", comparison['speedup'] > 1)
    else:
        check("classical_vs_quantum_queries implemented", False)

    multi = multi_solution_grover(3, [1, 6], shots=2048)
    if multi is not None:
        check("Multi-solution: success rate > 80%",
              multi['success_rate'] > 0.80)
        check("Multi-solution: both states found",
              multi['counts'].get('001', 0) > 0 and
              multi['counts'].get('110', 0) > 0)
    else:
        check("multi_solution_grover implemented", False)

    # ── Summary ──
    print(f"\n{'=' * 60}")
    print(f"Results: {passed}/{passed + failed} tests passed")
    if failed == 0:
        print("🎉 All tests passed! Ready for Day 7!")
    else:
        print(f"💪 {failed} test(s) remaining. Check the TODOs above.")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
