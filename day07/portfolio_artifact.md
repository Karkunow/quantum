# From Fourier to Factoring: Why QFT Matters

*Day 7 Portfolio Artifact — 14-Day Quantum DevRel Bootcamp*

---

## The Transform That Powers Quantum Advantage

The Quantum Fourier Transform (QFT) is the single most important subroutine in quantum computing. It's the engine inside Shor's factoring algorithm — the algorithm that, more than any other, drove investment in quantum computing. Understanding QFT means understanding *why* quantum computers can break RSA encryption, estimate molecular energies, and solve problems that classical computers cannot efficiently touch.

Today I built QFT circuits from scratch, implemented Quantum Phase Estimation, and traced the line from Fourier analysis to integer factorization.

---

## Classical DFT → Quantum QFT

The Discrete Fourier Transform (DFT) maps $N$ complex numbers to $N$ frequency components:

$$y_k = \frac{1}{\sqrt{N}} \sum_{j=0}^{N-1} x_j \cdot \omega^{jk}, \quad \omega = e^{2\pi i / N}$$

The QFT does the same thing on quantum amplitudes:

$$\text{QFT}|j\rangle = \frac{1}{\sqrt{N}} \sum_{k=0}^{N-1} e^{2\pi i jk/N}|k\rangle$$

The difference is efficiency. The classical Fast Fourier Transform takes $O(N \log N)$ operations. The QFT circuit uses $O(n^2)$ gates where $n = \log_2 N$. For $N = 2^{20}$, that's ~20 million vs ~400 gates.

**But there's a catch:** you can't read all the amplitudes — measurement collapses the state to a single outcome. The QFT's power comes only when embedded in algorithms that extract *structured information* from the transformed state.

---

## The QFT Circuit: Building Frequencies Qubit by Qubit

The QFT circuit has an elegant recursive structure:

For each qubit $j$ (most significant to least):
1. Apply Hadamard to qubit $j$
2. Apply controlled-$R_k$ rotation from qubit $j+k$ for $k = 2, 3, \ldots$
3. After all qubits processed, swap to reverse bit order

The controlled rotation $R_k$ adds phase $2\pi/2^k$ when both control and target are $|1\rangle$:

$$R_k = \begin{pmatrix} 1 & 0 \\ 0 & e^{2\pi i/2^k} \end{pmatrix}$$

**Gate count:** $n$ Hadamards + $n(n-1)/2$ controlled rotations + $\lfloor n/2 \rfloor$ SWAPs = $O(n^2)$ total. For 20 qubits: 210 gates. For the equivalent classical FFT on $2^{20}$ numbers: ~20 million operations.

| Qubits | $N = 2^n$ | QFT gates | Classical FFT ops | Ratio |
| :---: | :---: | :---: | :---: | :---: |
| 5 | 32 | 15 | 160 | 11× |
| 10 | 1,024 | 55 | 10,240 | 186× |
| 20 | 1,048,576 | 210 | ~20M | 95,000× |
| 30 | ~1 billion | 465 | ~30B | 65M× |

---

## What QFT Actually Does: Periodicity Detection

The QFT's superpower is converting **periodicity** in the computational basis into **peaks** in the Fourier basis.

If the input state is periodic with period $r$:

$$|\psi\rangle = \frac{1}{\sqrt{N/r}} \sum_{k=0}^{N/r-1} |kr\rangle$$

Then the QFT output peaks at multiples of $N/r$:

$$\text{QFT}|\psi\rangle \quad \text{has peaks at} \quad |0\rangle, |N/r\rangle, |2N/r\rangle, \ldots$$

Read off the peak spacing $\rightarrow$ determine $N/r$ $\rightarrow$ compute $r$. This is the mechanism behind Shor's algorithm.

---

## Quantum Phase Estimation: QFT's Killer Application

QPE answers: given a unitary $U$ and its eigenstate $|\psi\rangle$ with $U|\psi\rangle = e^{2\pi i \phi}|\psi\rangle$, what is $\phi$?

**The circuit:**
1. $n$ counting qubits initialized to $|+\rangle$ via Hadamard
2. Controlled-$U^{2^j}$ from counting qubit $j$ to the eigenstate register
3. Inverse QFT on the counting register
4. Measure → $n$-bit estimate of $\phi$

**Why it works:** The controlled-$U^{2^j}$ operations encode the phase as:

$$|j\rangle \otimes |\psi\rangle \xrightarrow{\text{c-}U^{2^j}} e^{2\pi i \cdot 2^j \phi}|j\rangle \otimes |\psi\rangle$$

After all $j$, the counting register holds $\sum_j e^{2\pi i \cdot 2^j \phi}|j\rangle$ — which is exactly the QFT of the binary representation of $\phi$. Inverse QFT decodes it.

**Precision:** $n$ counting qubits give precision $2^{-n}$. For an exact binary fraction (like $\phi = 1/8 = 0.001_2$), QPE gives the exact answer with 3 qubits.

### QPE Results I Verified

| Unitary | Eigenvalue | Exact $\phi$ | QPE Estimate | Qubits |
| :--- | :--- | :--- | :--- | :---: |
| T gate on $\|1\rangle$ | $e^{i\pi/4}$ | 1/8 = 0.125 | 0.125 (exact) | 3 |
| S gate on $\|1\rangle$ | $i = e^{i\pi/2}$ | 1/4 = 0.25 | 0.25 (exact) | 3 |
| Z gate on $\|1\rangle$ | $-1 = e^{i\pi}$ | 1/2 = 0.5 | 0.5 (exact) | 3 |
| $R_z(\pi/3)$ on $\|1\rangle$ | $e^{i\pi/6}$ | 1/12 ≈ 0.0833 | ~0.0625 | 4 |

The last example shows QPE's limitation: when $\phi$ isn't an exact binary fraction, more counting qubits improve precision but perfect accuracy requires infinite qubits — just like finite-precision arithmetic.

---

## From QPE to Shor: The Factoring Connection

This is the chain of reductions that makes quantum factoring possible:

1. **Factoring → Order Finding:** To factor $N$, find the smallest $r$ such that $a^r \equiv 1 \pmod{N}$ for random $a$. Then $\gcd(a^{r/2} \pm 1, N)$ often yields a factor.

2. **Order Finding → Phase Estimation:** The modular exponentiation unitary $U_a|x\rangle = |ax \bmod N\rangle$ has eigenstates with eigenvalues $e^{2\pi i s/r}$. QPE estimates $s/r$.

3. **Phase Estimation → Period Extraction:** From the QPE measurement $\approx s/r$, the continued fractions algorithm extracts $r$ (the denominator).

**For $N = 15$, $a = 7$:**
- $7^1 \bmod 15 = 7$, $7^2 = 49 \bmod 15 = 4$, $7^3 = 343 \bmod 15 = 13$, $7^4 = 2401 \bmod 15 = 1$
- Order $r = 4$
- $\gcd(7^2 + 1, 15) = \gcd(50, 15) = 5$ ✓
- $\gcd(7^2 - 1, 15) = \gcd(48, 15) = 3$ ✓
- $15 = 3 \times 5$

The quantum speedup: QPE runs in $O(n^3)$ time on $O(n)$ qubits, where $n = \log_2 N$. The best known classical algorithm (General Number Field Sieve) runs in sub-exponential time $e^{O(n^{1/3})}$. For large $N$, this is an **exponential** quantum advantage.

---

## Why QFT Matters for DevRel

The QFT is where quantum computing gets serious:

- **It's the "why" behind quantum advantage.** When someone asks "what can quantum computers actually do better?", the answer traces back to QFT and its ability to detect structure (periodicity, phases) exponentially faster.

- **It's a bridge between math and hardware.** Explaining QFT requires connecting Fourier analysis (pure math), circuit construction (engineering), and applications (cryptography, chemistry). Perfect DevRel territory.

- **It calibrates expectations.** The QFT itself is efficient — $O(n^2)$ gates. The bottleneck in Shor's is the **modular exponentiation oracle**, not the QFT. This nuance matters when discussing when quantum computers will break RSA.

- **It connects to quantum chemistry.** QPE is how future quantum computers will estimate molecular ground state energies — the most commercially promising near-term application.

---

## Interview-Ready Takeaway

> *"The Quantum Fourier Transform converts periodicity in the computational basis to peaks in the Fourier basis, using only O(n²) gates — exponentially fewer than the classical FFT. Its most important application is Quantum Phase Estimation, which estimates eigenvalues of unitaries. QPE is the engine inside Shor's factoring algorithm: the modular exponentiation unitary has eigenvalues encoding the order r, QPE extracts s/r, and continued fractions give r. This chain — factoring → order finding → phase estimation → QFT — is the canonical example of exponential quantum advantage."*

---

*Written as part of my Quantum DevRel preparation journey — Day 7.*
*Week 1 complete! Next: Day 8 — Variational Quantum Algorithms, the dominant paradigm for near-term applications.*
