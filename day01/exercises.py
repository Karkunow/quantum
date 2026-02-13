"""
Day 1: Engineering Foundations + Quantum State Formalism
=========================================================

BLOCK 1: Python Crash Upgrade for Quantum Computing
- numpy arrays & matrix operations
- complex numbers
- basic functions & list comprehensions

Your tasks:
1. Implement a function that normalizes a complex vector
2. Implement a function that checks if a matrix is unitary
3. Implement a function that computes tensor product manually
"""

import numpy as np
from typing import Tuple


# =============================================================================
# TASK 1: Normalize a Complex Vector
# =============================================================================
def normalize_vector(v: np.ndarray) -> np.ndarray:
    """
    Normalize a complex vector to have unit length (norm = 1).
    
    In quantum mechanics, state vectors must be normalized because
    the squared magnitudes of amplitudes represent probabilities,
    which must sum to 1.
    
    Args:
        v: A complex numpy array representing the vector
        
    Returns:
        The normalized vector (same direction, unit length)
        
    Example:
        >>> v = np.array([3+4j, 0])
        >>> normalize_vector(v)
        array([0.6+0.8j, 0.+0.j])
    """
    # TODO: Implement this function
    # Hint: The norm of a complex vector is sqrt(sum of |v_i|^2)
    # In numpy: np.linalg.norm(v) works for complex vectors
    norm = np.sum(v * np.conjugate(v)) ** 0.5  # Manual norm calculation
    if norm == 0:
        raise ValueError("Cannot normalize the zero vector")
    return v / norm

# =============================================================================
# TASK 2: Check if a Matrix is Unitary
# =============================================================================
def is_unitary(U: np.ndarray, tolerance: float = 1e-10) -> bool:
    """
    Check if a matrix is unitary.
    
    A matrix U is unitary if U†U = I (U-dagger times U equals Identity)
    where U† is the conjugate transpose of U.
    
    This is crucial in quantum computing because:
    - All quantum gates are unitary operations
    - Unitary operations preserve the norm of state vectors
    - Unitary operations are reversible
    
    Args:
        U: A square complex numpy matrix
        tolerance: Maximum allowed deviation from identity
        
    Returns:
        True if U is unitary within tolerance, False otherwise
        
    Example:
        >>> H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])  # Hadamard
        >>> is_unitary(H)
        True
    """
    # TODO: Implement this function
    # Hint: 
    # 1. Compute U† using np.conjugate(U.T) or U.conj().T
    # 2. Multiply U† @ U
    # 3. Compare to identity matrix using np.allclose()
    U_dagger = np.conjugate(U.T)
    identity = np.eye(U.shape[0])
    return np.allclose(U_dagger @ U, identity, atol=tolerance)


# =============================================================================
# TASK 3: Manual Tensor Product (Kronecker Product)
# =============================================================================
def tensor_product(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    Compute the tensor product (Kronecker product) of two matrices/vectors.
    
    For matrices A (m×n) and B (p×q), the result is (mp×nq).
    
    The tensor product is FUNDAMENTAL to quantum computing because:
    - Composite quantum systems are described by tensor products of their parts
    - An n-qubit system lives in a 2^n dimensional Hilbert space
    - This is why quantum computers can represent exponentially large states
    
    For vectors |a⟩ and |b⟩:
    |a⟩ ⊗ |b⟩ = [a₀|b⟩, a₁|b⟩, ...]ᵀ
    
    Args:
        A: First matrix/vector
        B: Second matrix/vector
        
    Returns:
        The tensor product A ⊗ B
        
    Example:
        >>> a = np.array([1, 0])  # |0⟩
        >>> b = np.array([0, 1])  # |1⟩
        >>> tensor_product(a, b)
        array([0, 1, 0, 0])  # |01⟩
    """
    # TODO: Implement this WITHOUT using np.kron()
    # This is to ensure you understand the operation
    # 
    # Algorithm for vectors:
    # 1. Get shapes of A and B
    # 2. Create result array of appropriate size
    # 3. For each element a_i in A, place a_i * B in the correct position
    #
    # For matrices, it's similar but you need to handle 2D blocks
    A = np.atleast_2d(A)
    B = np.atleast_2d(B)
    m, n = A.shape
    p, q = B.shape
    result = np.zeros((m * p, n * q), dtype=complex)
    for i in range(m):
        for j in range(n):
            result[i*p:(i+1)*p, j*q:(j+1)*q] = A[i, j] * B
    # If original inputs were 1D, we should return a 1D array
    if A.shape[0] == 1 or A.shape[1] == 1:
        result = result.flatten()
    return result


# =============================================================================
# TESTS - Run these to verify your implementations
# =============================================================================
def run_tests():
    """Test all implementations."""
    print("=" * 60)
    print("Testing Day 1 Implementations")
    print("=" * 60)
    
    # Test 1: normalize_vector
    print("\n📐 Test 1: Vector Normalization")
    v1 = np.array([3+4j, 0])
    result1 = normalize_vector(v1)
    expected1 = np.array([0.6+0.8j, 0])
    if result1 is not None and np.allclose(result1, expected1):
        print("   ✅ PASSED: [3+4j, 0] → [0.6+0.8j, 0]")
    else:
        print(f"   ❌ FAILED: Expected {expected1}, got {result1}")
    
    v2 = np.array([1, 1, 1, 1])
    result2 = normalize_vector(v2)
    if result2 is not None and np.isclose(np.linalg.norm(result2), 1.0):
        print("   ✅ PASSED: Normalized vector has unit norm")
    else:
        print("   ❌ FAILED: Normalized vector should have norm 1")
    
    # Test 2: is_unitary
    print("\n🔄 Test 2: Unitary Matrix Check")
    H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])  # Hadamard gate
    if is_unitary(H) == True:
        print("   ✅ PASSED: Hadamard matrix is unitary")
    else:
        print("   ❌ FAILED: Hadamard should be unitary")
    
    X = np.array([[0, 1], [1, 0]])  # Pauli-X gate
    if is_unitary(X) == True:
        print("   ✅ PASSED: Pauli-X matrix is unitary")
    else:
        print("   ❌ FAILED: Pauli-X should be unitary")
    
    non_unitary = np.array([[1, 1], [0, 1]])
    if is_unitary(non_unitary) == False:
        print("   ✅ PASSED: Non-unitary matrix correctly identified")
    else:
        print("   ❌ FAILED: [[1,1],[0,1]] is NOT unitary")
    
    # Test 3: tensor_product
    print("\n⊗ Test 3: Tensor Product")
    ket0 = np.array([1, 0])  # |0⟩
    ket1 = np.array([0, 1])  # |1⟩
    
    result_01 = tensor_product(ket0, ket1)
    expected_01 = np.array([0, 1, 0, 0])  # |01⟩
    if result_01 is not None and np.allclose(result_01, expected_01):
        print("   ✅ PASSED: |0⟩ ⊗ |1⟩ = |01⟩")
    else:
        print(f"   ❌ FAILED: Expected {expected_01}, got {result_01}")
    
    result_10 = tensor_product(ket1, ket0)
    expected_10 = np.array([0, 0, 1, 0])  # |10⟩
    if result_10 is not None and np.allclose(result_10, expected_10):
        print("   ✅ PASSED: |1⟩ ⊗ |0⟩ = |10⟩")
    else:
        print(f"   ❌ FAILED: Expected {expected_10}, got {result_10}")
    
    # Test matrix tensor product
    I = np.eye(2)
    X = np.array([[0, 1], [1, 0]])
    IX = tensor_product(I, X)
    expected_IX = np.array([[0, 1, 0, 0],
                            [1, 0, 0, 0],
                            [0, 0, 0, 1],
                            [0, 0, 1, 0]])
    if IX is not None and np.allclose(IX, expected_IX):
        print("   ✅ PASSED: I ⊗ X matrix tensor product correct")
    else:
        print("   ❌ FAILED: I ⊗ X matrix tensor product")
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
