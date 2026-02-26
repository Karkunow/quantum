"""
Day 6 Solutions: Grover's Search Algorithm
===========================================

14-Day Quantum DevRel Bootcamp

Complete implementations with interview insights.
Only check these AFTER attempting the exercises yourself!
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator
from qiskit_aer import AerSimulator


# ============================================================
# Solution 1: Oracle Construction
# ============================================================
# 💬 Interview insight: "The oracle is NOT the hard part of
# Grover's algorithm — constructing it IS! In real applications,
# the oracle encodes the problem structure. For SAT problems,
# database search, or constraint satisfaction, designing an
# efficient oracle is where the actual engineering happens."

def build_oracle_matrix(n_qubits: int, marked_states: list[int]) -> np.ndarray:
    """Oₓ = I - 2 Σᵢ |wᵢ⟩⟨wᵢ| — phase flip on marked states.

    💬 "The oracle is a diagonal matrix in the computational basis.
    It does nothing except flip the sign of marked states — but
    this tiny phase change is invisible after one application.
    The magic comes from combining it with the diffusion operator."
    """
    N = 2 ** n_qubits
    oracle = np.eye(N, dtype=complex)
    for state in marked_states:
        oracle[state, state] = -1
    return oracle


def build_oracle_circuit(n_qubits: int, marked_states: list[int]) -> QuantumCircuit:
    """Circuit implementation of the phase oracle.

    For each marked state |w⟩:
      1. Apply X to qubits where w has a 0 bit
      2. Apply multi-controlled Z (= H·MCX·H on target)
      3. Undo X gates

    💬 "For a single marked state, this uses O(n) gates and O(n)
    ancillas for the MCX decomposition. In practice, you'd use
    Qiskit's unitary synthesis or build problem-specific oracles."
    """
    qc = QuantumCircuit(n_qubits)

    for target in marked_states:
        # Determine which qubits need X (those that are 0 in target)
        for i in range(n_qubits):
            if not (target >> i) & 1:
                qc.x(i)

        # Multi-controlled Z = H on last, MCX, H on last
        if n_qubits == 1:
            qc.z(0)
        else:
            qc.h(n_qubits - 1)
            qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
            qc.h(n_qubits - 1)

        # Undo X gates
        for i in range(n_qubits):
            if not (target >> i) & 1:
                qc.x(i)

    return qc


# ============================================================
# Solution 2: Diffusion Operator
# ============================================================
# 💬 Interview insight: "The diffusion operator is really a
# reflection about the mean amplitude. Geometrically, Grover's
# algorithm performs rotations in a 2D plane spanned by the
# marked states and their complement. Each iteration rotates
# by 2θ where sin(θ) = √(M/N)."

def build_diffusion_matrix(n_qubits: int) -> np.ndarray:
    """D = 2|s⟩⟨s| - I — reflection about the uniform superposition.

    💬 "This is sometimes called the 'inversion about the mean.'
    States with amplitude above the mean get boosted, those below
    get suppressed. After the oracle marks a state (inverts its
    amplitude), the diffusion operator amplifies it."
    """
    N = 2 ** n_qubits
    s = np.ones(N, dtype=complex) / np.sqrt(N)
    return 2 * np.outer(s, s) - np.eye(N, dtype=complex)


def build_diffusion_circuit(n_qubits: int) -> QuantumCircuit:
    """Circuit implementation of the diffusion operator.

    H⊗ⁿ · (2|0⟩⟨0| - I) · H⊗ⁿ

    The inner part (2|0⟩⟨0| - I) flips the phase of all states
    except |0...0⟩. Implemented as:
        X⊗ⁿ → MCZ → X⊗ⁿ
    """
    qc = QuantumCircuit(n_qubits)

    # H on all qubits
    qc.h(range(n_qubits))

    # X on all qubits
    qc.x(range(n_qubits))

    # Multi-controlled Z
    qc.h(n_qubits - 1)
    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    qc.h(n_qubits - 1)

    # Undo X
    qc.x(range(n_qubits))

    # H on all qubits
    qc.h(range(n_qubits))

    return qc


# ============================================================
# Solution 3: Complete Grover's Algorithm
# ============================================================
# 💬 Interview insight: "Grover's speedup is quadratic — √N
# instead of N. This is provably optimal for unstructured search.
# It's not exponential, but it's still significant: searching
# a million items takes ~785 queries instead of 500,000."

def optimal_iterations(n_qubits: int, n_marked: int = 1) -> int:
    """k = round(π/(4·arcsin(√(M/N))) - 1/2)

    💬 "Too many iterations is as bad as too few — the state
    rotates PAST the target. This is called 'Grover's soufflé':
    you have to take it out of the oven at exactly the right time."
    """
    N = 2 ** n_qubits
    theta = np.arcsin(np.sqrt(n_marked / N))
    k = round(np.pi / (4 * theta) - 0.5)
    return max(1, k)


def grover_circuit(n_qubits: int, marked_states: list[int],
                   n_iterations: int | None = None) -> QuantumCircuit:
    """Complete Grover's algorithm circuit.

    1. H⊗ⁿ → uniform superposition
    2. Repeat k times: Oracle → Diffusion
    3. Measure all qubits
    """
    if n_iterations is None:
        n_iterations = optimal_iterations(n_qubits, len(marked_states))

    qc = QuantumCircuit(n_qubits, n_qubits)

    # Initial superposition
    qc.h(range(n_qubits))

    # Grover iterations
    oracle = build_oracle_circuit(n_qubits, marked_states)
    diffusion = build_diffusion_circuit(n_qubits)

    for _ in range(n_iterations):
        qc.compose(oracle, inplace=True)
        qc.barrier()
        qc.compose(diffusion, inplace=True)
        qc.barrier()

    # Measurement
    qc.measure(range(n_qubits), range(n_qubits))

    return qc


def run_grover(n_qubits: int, marked_states: list[int],
               n_iterations: int | None = None,
               shots: int = 1024) -> dict[str, int]:
    """Run Grover's algorithm and return counts.

    💬 "Always run multiple shots — quantum algorithms are
    probabilistic. Grover gives >90% success probability at
    optimal iterations, but you verify by statistics."
    """
    qc = grover_circuit(n_qubits, marked_states, n_iterations)
    sim = AerSimulator()
    result = sim.run(qc, shots=shots).result()
    return result.get_counts()


# ============================================================
# Solution 4: Amplitude Amplification Analysis
# ============================================================
# 💬 Interview insight: "Amplitude amplification is the general
# principle behind Grover's algorithm. It works for ANY initial
# state and ANY 'good' subspace — Grover's search is just the
# special case where the initial state is uniform. This
# generality makes it a subroutine in many quantum algorithms."

def success_probability(n_qubits: int, n_marked: int,
                        k_iterations: int) -> float:
    """P(k) = sin²((2k + 1)·θ) where sin²(θ) = M/N.

    💬 "The probability oscillates sinusoidally with iteration
    count. This is why you can OVER-iterate — the probability
    goes up, reaches ~1, then comes back down. The optimal
    iteration count puts you at the peak."
    """
    N = 2 ** n_qubits
    theta = np.arcsin(np.sqrt(n_marked / N))
    return float(np.sin((2 * k_iterations + 1) * theta) ** 2)


def amplitude_evolution(n_qubits: int, marked_states: list[int],
                        max_iterations: int) -> list[dict]:
    """Track amplitude evolution through Grover iterations.

    Uses statevector simulation (no measurement) to see exact
    amplitudes at each step.
    """
    N = 2 ** n_qubits
    n_marked = len(marked_states)
    marked_set = set(marked_states)

    # Oracle and diffusion as matrices
    oracle_mat = build_oracle_matrix(n_qubits, marked_states)
    diff_mat = build_diffusion_matrix(n_qubits)

    # Start with uniform superposition
    state = np.ones(N, dtype=complex) / np.sqrt(N)

    results = []

    for k in range(max_iterations + 1):
        # Record current state
        probs = np.abs(state) ** 2
        p_marked = sum(probs[i] for i in marked_set)
        p_unmarked = 1.0 - p_marked

        results.append({
            'iteration': k,
            'p_marked': float(p_marked),
            'p_unmarked': float(p_unmarked),
            'amplitudes': state.copy().tolist()
        })

        # Apply one Grover step (oracle then diffusion)
        if k < max_iterations:
            state = oracle_mat @ state
            state = diff_mat @ state

    return results


# ============================================================
# Solution 5: Multi-Solution Grover & Classical Comparison
# ============================================================
# 💬 Interview insight: "Grover's quadratic speedup holds for
# ANY number of marked states. With M solutions out of N items,
# the speedup is √(N/M). More solutions = fewer iterations needed.
# But there's a catch: if you don't KNOW M, you need quantum
# counting to estimate it first."

def classical_vs_quantum_queries(n_qubits: int, n_marked: int) -> dict:
    """Compare classical O(N/M) and quantum O(√(N/M)) query counts.

    💬 "This is the elevator pitch for Grover: searching a phone
    book with N entries takes N/2 lookups classically, but only
    ~√N quantum queries. For N = 1,000,000 that's 500,000 vs 785."
    """
    N = 2 ** n_qubits
    classical = N // n_marked  # expected queries for random search
    quantum = optimal_iterations(n_qubits, n_marked)

    return {
        'N': N,
        'M': n_marked,
        'classical_expected': classical,
        'quantum_iterations': quantum,
        'speedup': classical / quantum if quantum > 0 else float('inf')
    }


def multi_solution_grover(n_qubits: int, marked_states: list[int],
                          shots: int = 2048) -> dict:
    """Run Grover with multiple marked states and analyze.

    💬 "With M > 1 marked states, Grover's finds ANY of them.
    Each marked state gets roughly equal probability — the
    algorithm doesn't prefer one over another."
    """
    n_marked = len(marked_states)
    n_iter = optimal_iterations(n_qubits, n_marked)
    counts = run_grover(n_qubits, marked_states, n_iter, shots)

    # Classify outcomes
    marked_set = set()
    for state in marked_states:
        bitstring = format(state, f'0{n_qubits}b')
        marked_set.add(bitstring)

    marked_total = sum(c for bs, c in counts.items() if bs in marked_set)
    unmarked_total = sum(c for bs, c in counts.items() if bs not in marked_set)

    return {
        'counts': counts,
        'marked_total': marked_total,
        'unmarked_total': unmarked_total,
        'success_rate': marked_total / shots,
        'n_iterations': n_iter
    }


if __name__ == "__main__":
    print("Day 6 Solutions: Grover's Search Algorithm")
    print("=" * 55)

    # Demo: 2-qubit Grover
    print("\n🔍 2-Qubit Grover (target: |11⟩):")
    counts = run_grover(2, [3], shots=1024)
    for bs, c in sorted(counts.items()):
        print(f"  |{bs}⟩: {c} ({100 * c / 1024:.1f}%)")

    # Demo: 3-qubit Grover
    print("\n🔍 3-Qubit Grover (target: |101⟩):")
    counts = run_grover(3, [5], shots=1024)
    for bs, c in sorted(counts.items()):
        print(f"  |{bs}⟩: {c} ({100 * c / 1024:.1f}%)")

    # Demo: optimal iterations
    print("\nOptimal Iteration Counts:")
    for n in range(2, 7):
        k = optimal_iterations(n, 1)
        N = 2 ** n
        p = success_probability(n, 1, k)
        print(f"  n={n} (N={N:>3}): k={k}, P(success)={p:.4f}")

    # Demo: amplitude evolution
    print("\n📈 Amplitude Evolution (3-qubit, target |101⟩):")
    evo = amplitude_evolution(3, [5], 5)
    for step in evo:
        k = step['iteration']
        pm = step['p_marked']
        pu = step['p_unmarked']
        print(f"  k={k}: P(marked)={pm:.4f}, P(unmarked)={pu:.4f}")

    # Demo: classical vs quantum
    print("\n⚡ Classical vs Quantum Query Comparison:")
    for n in [4, 8, 10, 16, 20]:
        comp = classical_vs_quantum_queries(n, 1)
        print(f"  n={n:>2}: classical={comp['classical_expected']:>8}, "
              f"quantum={comp['quantum_iterations']:>5}, "
              f"speedup={comp['speedup']:.1f}×")

    # Demo: multi-solution
    print("\n🎯 Multi-Solution Grover (3-qubit, targets: |001⟩, |110⟩):")
    multi = multi_solution_grover(3, [1, 6], shots=2048)
    print(f"  Success rate: {multi['success_rate']:.2%}")
    print(f"  Iterations used: {multi['n_iterations']}")
    for bs, c in sorted(multi['counts'].items()):
        marker = " ← marked" if bs in ['001', '110'] else ""
        print(f"  |{bs}⟩: {c}{marker}")
