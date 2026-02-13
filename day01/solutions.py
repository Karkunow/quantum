"""
Day 1: SOLUTIONS
================

Study these AFTER attempting the exercises yourself!
Understanding WHY each line works is more important than copying.
"""

import numpy as np
from typing import Tuple


def normalize_vector(v: np.ndarray) -> np.ndarray:
    """
    Normalize a complex vector to have unit length.
    
    Mathematical basis:
    For vector |ψ⟩ = [α₀, α₁, ..., αₙ]ᵀ
    
    The norm is: ||ψ|| = √(∑|αᵢ|²) = √(⟨ψ|ψ⟩)
    
    Normalized: |ψ̂⟩ = |ψ⟩ / ||ψ||
    
    Why this matters in QC:
    - Quantum states must satisfy ∑|αᵢ|² = 1 (Born rule)
    - This ensures measurement probabilities sum to 1
    """
    norm = np.linalg.norm(v)  # Correctly handles complex numbers
    
    if norm == 0:
        raise ValueError("Cannot normalize zero vector")
    
    return v / norm


def is_unitary(U: np.ndarray, tolerance: float = 1e-10) -> bool:
    """
    Check if U†U = I within tolerance.
    
    Mathematical basis:
    U is unitary ⟺ U†U = UU† = I
    
    Where U† (U-dagger) is the conjugate transpose:
    (U†)ᵢⱼ = conj(Uⱼᵢ)
    
    Why unitary matrices matter in QC:
    1. REVERSIBILITY: U† is the inverse of U
    2. NORM PRESERVATION: ||Uψ|| = ||ψ|| 
       (quantum gates don't change total probability)
    3. EIGENVALUES: All eigenvalues have magnitude 1 (|λ| = 1)
       (relates to energy conservation)
    """
    # Compute conjugate transpose
    U_dagger = U.conj().T
    
    # Compute U†U
    product = U_dagger @ U
    
    # Compare to identity matrix
    identity = np.eye(U.shape[0])
    
    return np.allclose(product, identity, atol=tolerance)


def tensor_product(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    Manual tensor (Kronecker) product implementation.
    
    Mathematical basis:
    For vectors a ∈ ℂᵐ and b ∈ ℂⁿ:
    a ⊗ b = [a₀b, a₁b, ..., aₘ₋₁b]ᵀ ∈ ℂᵐⁿ
    
    For matrices A (m×n) and B (p×q):
    A ⊗ B is (mp×nq) with block structure:
    
    ┌                   ┐
    │ a₀₀B  a₀₁B  ...  │
    │ a₁₀B  a₁₁B  ...  │
    │ ...   ...   ...  │
    └                   ┘
    
    WHY tensor products are ESSENTIAL in QC:
    
    Single qubit lives in ℂ² (2D complex vector space)
    Two qubits live in ℂ² ⊗ ℂ² = ℂ⁴ (NOT ℂ² + ℂ² = ℂ⁴ directly!)
    n qubits live in ℂ^(2ⁿ)
    
    This EXPONENTIAL GROWTH is the source of quantum computational power.
    
    Key insight: Not all states in ℂ⁴ can be written as |a⟩⊗|b⟩
    Those that cannot are ENTANGLED!
    
    Example: |00⟩ + |11⟩ (Bell state) cannot be factored into |a⟩⊗|b⟩
    """
    # Handle 1D arrays (vectors)
    A = np.atleast_2d(A)
    B = np.atleast_2d(B)
    
    # If inputs were 1D, we need to track that for output
    a_was_1d = A.shape[0] == 1 or A.shape[1] == 1
    b_was_1d = B.shape[0] == 1 or B.shape[1] == 1
    
    m, n = A.shape
    p, q = B.shape
    
    # Result will be (m*p) × (n*q)
    result = np.zeros((m * p, n * q), dtype=complex)
    
    # Fill in blocks
    for i in range(m):
        for j in range(n):
            # Place A[i,j] * B in the appropriate block
            row_start = i * p
            row_end = (i + 1) * p
            col_start = j * q
            col_end = (j + 1) * q
            
            result[row_start:row_end, col_start:col_end] = A[i, j] * B
    
    # If both inputs were column or row vectors, flatten output
    if a_was_1d and b_was_1d:
        return result.flatten()
    
    return result


# =============================================================================
# BONUS: Why tensor products are required for composite quantum systems
# =============================================================================
"""
EXPLANATION FOR YOUR PORTFOLIO:

Why Tensor Products Are Required for Composite Quantum Systems
=============================================================

Consider two classical bits. Each can be 0 or 1.
To describe them, I need: (bit1_value, bit2_value) - just 2 numbers.

Now consider two quantum bits (qubits).

Qubit 1: |ψ₁⟩ = α|0⟩ + β|1⟩  (2 complex amplitudes)
Qubit 2: |ψ₂⟩ = γ|0⟩ + δ|1⟩  (2 complex amplitudes)

Can we describe the combined system with just 4 numbers (α,β,γ,δ)?

NO! Here's why:

The combined state is:
|ψ₁⟩ ⊗ |ψ₂⟩ = αγ|00⟩ + αδ|01⟩ + βγ|10⟩ + βδ|11⟩

This has 4 amplitudes, but they're not independent - they satisfy:
(αγ)(βδ) = (αδ)(βγ)   [they factor!]

But quantum mechanics allows states like:
|Φ⁺⟩ = (1/√2)(|00⟩ + |11⟩)

Try to factor this: α·γ = 1/√2 for |00⟩, β·δ = 1/√2 for |11⟩
But also: α·δ = 0 for |01⟩, β·γ = 0 for |10⟩

This requires α=0 or δ=0, AND β=0 or γ=0
But then we can't get the non-zero |00⟩ and |11⟩ terms!

CONCLUSION: The Bell state |Φ⁺⟩ cannot be written as |ψ₁⟩⊗|ψ₂⟩.

This means:
1. Two-qubit states need 4 independent complex numbers (2² = 4)
2. n-qubit states need 2ⁿ complex numbers
3. States that don't factor are called ENTANGLED
4. Entanglement is a quantum resource with no classical analog

The tensor product structure is not a choice - it's forced by the 
mathematical structure of quantum mechanics (specifically, how 
probabilities combine for independent systems).

This exponential state space is precisely why quantum computers
can potentially solve certain problems exponentially faster than
classical computers - but also why simulating them classically is hard!
"""


if __name__ == "__main__":
    # Demo the functions
    print("=== SOLUTION DEMONSTRATIONS ===\n")
    
    # 1. Normalization
    print("1. Vector Normalization")
    v = np.array([3+4j, 0])
    v_norm = normalize_vector(v)
    print(f"   Original: {v}")
    print(f"   Normalized: {v_norm}")
    print(f"   Norm check: {np.linalg.norm(v_norm):.6f}\n")
    
    # 2. Unitary check
    print("2. Unitary Matrix Check")
    H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
    print(f"   Hadamard is unitary: {is_unitary(H)}")
    
    X = np.array([[0, 1], [1, 0]])
    print(f"   Pauli-X is unitary: {is_unitary(X)}")
    
    bad = np.array([[1, 1], [0, 1]])
    print(f"   [[1,1],[0,1]] is unitary: {is_unitary(bad)}\n")
    
    # 3. Tensor product
    print("3. Tensor Product")
    ket0 = np.array([1, 0])
    ket1 = np.array([0, 1])
    
    print(f"   |0⟩ ⊗ |0⟩ = {tensor_product(ket0, ket0)}")
    print(f"   |0⟩ ⊗ |1⟩ = {tensor_product(ket0, ket1)}")
    print(f"   |1⟩ ⊗ |0⟩ = {tensor_product(ket1, ket0)}")
    print(f"   |1⟩ ⊗ |1⟩ = {tensor_product(ket1, ket1)}")
    
    # Verify against numpy's kron
    print(f"\n   Verification (matches np.kron): {np.allclose(tensor_product(ket0, ket1), np.kron(ket0, ket1))}")
