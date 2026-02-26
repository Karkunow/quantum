---
title: "Day 7: Quantum Fourier Transform"
subtitle: "14-Day Quantum DevRel Bootcamp — Airplane Reading Summary"
author: "Quantum Bootcamp"
date: \today
geometry: margin=2.5cm
fontsize: 11pt
colorlinks: true
toc: true
header-includes:
  - \usepackage{booktabs}
  - \usepackage{amsmath}
  - \usepackage{amssymb}
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhead[L]{Day 7 — Quantum Fourier Transform}
  - \fancyhead[R]{Quantum DevRel Bootcamp}
  - \fancyfoot[C]{\thepage}
---

\newpage

# Part 1: The Big Picture — The Transform That Powers Quantum Advantage

The Quantum Fourier Transform (QFT) is the single most important subroutine in
quantum computing. It's the engine inside Shor's factoring algorithm --- the algorithm
that, more than any other, drove investment in quantum computing. Understanding QFT
means understanding *why* quantum computers can break RSA encryption, estimate molecular
energies, and solve problems that classical computers cannot efficiently touch.

**The key chain of ideas:**

$$\text{Factoring} \xrightarrow{\text{reduce}} \text{Order Finding}
\xrightarrow{\text{QPE}} \text{Phase Estimation}
\xrightarrow{\text{uses}} \text{QFT}$$

Everything traces back to the QFT's ability to detect *periodicity* exponentially faster
than any classical algorithm.

---

# Part 2: Classical DFT to Quantum QFT

## The Discrete Fourier Transform

The DFT maps $N$ complex numbers to $N$ frequency components:

$$y_k = \frac{1}{\sqrt{N}} \sum_{j=0}^{N-1} x_j \cdot \omega^{jk}, \qquad \omega = e^{2\pi i / N}$$

The DFT matrix has entries $(\text{DFT})_{kj} = \omega^{jk}/\sqrt{N}$.

Key properties:

- **Unitary:** $\text{DFT}^\dagger \cdot \text{DFT} = I$
- **Symmetric:** $\text{DFT} = \text{DFT}^T$
- **Fourth power identity:** $\text{DFT}^4 = I$ (order 4)
- **$\text{DFT}|0\rangle$ = uniform superposition** (all amplitudes equal)

## QFT = DFT on Quantum Amplitudes

The QFT does the same thing, but on quantum state amplitudes:

$$\text{QFT}|j\rangle = \frac{1}{\sqrt{N}} \sum_{k=0}^{N-1} e^{2\pi i jk/N}|k\rangle$$

The QFT matrix is simply the DFT matrix with $N = 2^n$.

## The Efficiency Gap

| $n$ (qubits) | $N = 2^n$ | QFT gates ($O(n^2)$) | Classical FFT ops ($O(N\log N)$) | Ratio |
|:---:|:---:|:---:|:---:|:---:|
| 5 | 32 | 15 | 160 | 11$\times$ |
| 10 | 1,024 | 55 | 10,240 | 186$\times$ |
| 20 | 1,048,576 | 210 | approximately 20M | 95,000$\times$ |
| 30 | approximately 1 billion | 465 | approximately 30B | 65M$\times$ |

**But there's a catch:** you can't read all the amplitudes --- measurement collapses the
state to a single outcome. The QFT's power comes only when embedded in algorithms that
extract *structured information* from the transformed state (like QPE).

> **Interview insight:** "The QFT is the quantum analog of the classical DFT. Classically,
> the FFT takes $O(N \log N)$ operations. The QFT circuit uses $O(n^2)$ gates on $n$
> qubits, which is exponentially fewer since $N = 2^n$. But you can't read out all the
> amplitudes --- the speedup is real only when combined with algorithms like QPE or
> Shor's that extract useful information from the transformed state."

---

# Part 3: The QFT Circuit --- Building Frequencies Qubit by Qubit

## Circuit Structure

The QFT circuit has an elegant recursive structure. For each qubit $j$ (most significant
to least significant):

1. **Hadamard** on qubit $j$ --- creates the base frequency component
2. **Controlled-$R_k$** rotation from qubit $j+k$ for $k = 2, 3, \ldots$ --- adds fine
   phase structure
3. After all qubits processed, **SWAP** to reverse bit order

The controlled rotation gate:

$$R_k = \begin{pmatrix} 1 & 0 \\ 0 & e^{2\pi i/2^k} \end{pmatrix}$$

This adds phase $2\pi/2^k$ when both the control and target qubits are $|1\rangle$.

## Gate Count

- $n$ Hadamard gates
- $n(n-1)/2$ controlled-phase gates
- $\lfloor n/2 \rfloor$ SWAP gates
- **Total: $O(n^2)$ gates** for $n$ qubits

Think of it as constructing a Fourier series qubit by qubit: the Hadamard creates the
fundamental frequency, and each subsequent controlled rotation adds higher-frequency
harmonics.

## Key Subtlety: Bit Reversal

The QFT naturally outputs qubits in reverse order compared to the mathematical
convention. The final SWAP gates correct this. Some implementations omit the SWAPs and
account for the reversal in the surrounding algorithm instead.

> **Interview insight:** "The QFT circuit has a beautiful recursive structure. For each
> qubit: one Hadamard + $(n-1)$ controlled rotations, giving $n(n+1)/2$ total gates.
> This $O(n^2)$ is exponentially better than the classical FFT's $O(N \log N) = O(n \cdot 2^n)$.
> The final SWAPs reverse the bit order --- a consequence of the big-endian vs
> little-endian convention."

---

# Part 4: What QFT Does --- Periodicity Detection

## QFT on Basis States

When applied to a computational basis state $|j\rangle$:

$$\text{QFT}|j\rangle = \frac{1}{\sqrt{N}} \sum_{k=0}^{N-1} e^{2\pi i jk/N}|k\rangle$$

The result has **uniform probabilities** ($1/N$ for every outcome) but different
**phases**. The information is entirely in the phases, which is why direct measurement
after QFT is useless --- you need structure (like QPE) to extract it.

## QFT on Periodic States --- The Critical Application

The QFT's superpower is converting **periodicity** in the computational basis into
**peaks** in the Fourier basis.

If the input state is periodic with period $r$:

$$|\psi\rangle = \frac{1}{\sqrt{N/r}} \sum_{k=0}^{N/r-1} |kr\rangle$$

Then the QFT output peaks at multiples of $N/r$:

$$\text{QFT}|\psi\rangle \quad \text{has peaks at} \quad |0\rangle, |N/r\rangle, |2N/r\rangle, \ldots$$

Read off the peak spacing $\rightarrow$ determine $N/r$ $\rightarrow$ compute $r$.

### Concrete Examples (3 qubits, $N = 8$)

| Input period $r$ | Input states | QFT peaks at | Peak spacing |
|:---:|:---|:---|:---:|
| 1 | All 8 states | $|000\rangle$ only | 8 |
| 2 | $|000\rangle, |010\rangle, |100\rangle, |110\rangle$ | $|000\rangle, |100\rangle$ | 4 |
| 4 | $|000\rangle, |100\rangle$ | $|000\rangle, |010\rangle, |100\rangle, |110\rangle$ | 2 |
| 8 | $|000\rangle$ only | All 8 states (uniform) | 1 |

Notice the *duality*: short period in input $\leftrightarrow$ wide spacing in output,
and vice versa. This is exactly the time--frequency duality from classical Fourier analysis.

> **Interview insight:** "The QFT interconverts between time and frequency representations.
> A state periodic in the computational basis transforms to peaks at multiples of $N/r$
> in the Fourier basis. This is EXACTLY what Shor's algorithm exploits: the modular
> exponentiation creates a periodic state, and QPE (which uses QFT) reveals the period."

---

# Part 5: Quantum Phase Estimation (QPE) --- QFT's Killer Application

QPE answers a fundamental question: given a unitary $U$ and its eigenstate
$|\psi\rangle$ with $U|\psi\rangle = e^{2\pi i \phi}|\psi\rangle$, what is $\phi$?

## The QPE Circuit

1. **$n$ counting qubits** initialized to $|0\rangle$, eigenstate $|\psi\rangle$ in
   the target register
2. **Hadamard** on all counting qubits
3. **Controlled-$U^{2^j}$** from counting qubit $j$ to the eigenstate register
4. **Inverse QFT** on the counting register
5. **Measure** counting register $\rightarrow$ $n$-bit binary estimate of $\phi$

## Why It Works

The controlled-$U^{2^j}$ operations encode the phase as:

$$|j\rangle \otimes |\psi\rangle \xrightarrow{\text{c-}U^{2^j}}
e^{2\pi i \cdot 2^j \phi}|j\rangle \otimes |\psi\rangle$$

After all $j$ values, the counting register holds:

$$\sum_j e^{2\pi i \cdot 2^j \phi}|j\rangle$$

This is exactly the QFT of the binary representation of $\phi$. Applying the inverse QFT
decodes $\phi$ into binary.

## Precision

- $n$ counting qubits give precision $2^{-n}$
- Each additional qubit **doubles** the precision
- For exact binary fractions ($\phi = k/2^n$), QPE gives the **exact** answer

## QPE Results on Standard Gates

| Gate | Eigenstate | Eigenvalue | Exact $\phi$ | QPE (3 qubits) |
|:-----|:-----------|:-----------|:-------------|:----------------|
| T | $|1\rangle$ | $e^{i\pi/4}$ | $1/8 = 0.125$ | 0.125 (exact) |
| S | $|1\rangle$ | $i = e^{i\pi/2}$ | $1/4 = 0.25$ | 0.25 (exact) |
| Z | $|1\rangle$ | $-1 = e^{i\pi}$ | $1/2 = 0.5$ | 0.5 (exact) |
| $R_z(\pi/3)$ | $|1\rangle$ | $e^{i\pi/6}$ | $1/12 \approx 0.083$ | $\approx 0.0625$ (4 qubits) |

The last example shows QPE's limitation: when $\phi$ isn't an exact binary fraction,
more counting qubits improve precision, but perfect accuracy requires infinite precision ---
just like finite-precision arithmetic.

**Precision scaling for $R_z(\pi/3)$** ($\phi = 1/12$, non-terminating binary):

| Counting qubits | Precision ($1/2^n$) | Typical error |
|:---:|:---:|:---:|
| 2 | 0.25 | approximately 0.08 |
| 4 | 0.0625 | approximately 0.02 |
| 6 | 0.0156 | approximately 0.005 |
| 8 | 0.0039 | approximately 0.001 |

Each qubit roughly halves the error.

> **Interview insight:** "QPE is arguably the most important subroutine in quantum
> computing. It's the engine inside Shor's algorithm, quantum chemistry (ground state
> energy estimation), and HHL (linear systems). The precision scales as $2^{-n}$ with $n$
> counting qubits, and the circuit depth scales polynomially."

---

# Part 6: From QPE to Shor --- The Factoring Connection

This is the chain of reductions that makes quantum factoring possible.

## Step 1: Factoring $\rightarrow$ Order Finding

To factor $N$, pick a random $a < N$ and find the smallest $r$ such that:

$$a^r \equiv 1 \pmod{N}$$

Once $r$ is known (and $r$ is even), compute:

$$\gcd(a^{r/2} + 1,\, N) \quad \text{and} \quad \gcd(a^{r/2} - 1,\, N)$$

With probability $\geq 1/2$, one of these is a non-trivial factor of $N$.

## Step 2: Order Finding $\rightarrow$ Phase Estimation

The modular exponentiation unitary $U_a|x\rangle = |ax \bmod N\rangle$ has eigenstates:

$$|u_s\rangle = \frac{1}{\sqrt{r}} \sum_{k=0}^{r-1} e^{-2\pi i sk/r} |a^k \bmod N\rangle$$

with eigenvalues $e^{2\pi i s/r}$ for $s = 0, 1, \ldots, r-1$.

QPE estimates $s/r$.

## Step 3: Phase Estimation $\rightarrow$ Period Extraction

From the QPE measurement $\approx s/r$, the **continued fractions algorithm** extracts
$r$ (the denominator). This classical post-processing step is efficient.

## Worked Example: $N = 15$, $a = 7$

**Find the order:**

- $7^1 \bmod 15 = 7$
- $7^2 \bmod 15 = 49 \bmod 15 = 4$
- $7^3 \bmod 15 = 343 \bmod 15 = 13$
- $7^4 \bmod 15 = 2401 \bmod 15 = 1$ $\leftarrow$ order $r = 4$

**Factor using $r$:**

- $a^{r/2} = 7^2 = 49 \bmod 15 = 4$
- $\gcd(4 + 1, 15) = \gcd(5, 15) = \mathbf{5}$ 
- $\gcd(4 - 1, 15) = \gcd(3, 15) = \mathbf{3}$ 
- $15 = 3 \times 5$

**QPE eigenvalues:**

The eigenvalues of $U_7$ are $e^{2\pi i s/4}$ for $s = 0, 1, 2, 3$:

| $s$ | Phase $\phi = s/r$ | QPE measurement |
|:---:|:---:|:---:|
| 0 | 0.0 | $|000\rangle$ |
| 1 | 0.25 | $|010\rangle$ |
| 2 | 0.5 | $|100\rangle$ |
| 3 | 0.75 | $|110\rangle$ |

From any non-zero measurement, continued fractions recover $r = 4$.

## The Quantum Speedup

- **Quantum (Shor):** $O(n^3)$ time on $O(n)$ qubits, where $n = \log_2 N$
- **Classical (General Number Field Sieve):** Sub-exponential $e^{O(n^{1/3})}$
- For large $N$, this is an **exponential** quantum advantage

**For RSA-2048:** quantum needs approximately 4,096 logical qubits with error correction.
Current largest processors: approximately 1,200 physical qubits (IBM). Still a significant
engineering gap.

> **Interview insight:** "This is one of the most important explanations in quantum
> computing: factoring reduces to order finding, order finding reduces to phase estimation,
> and phase estimation uses the QFT. The quantum speedup comes from QPE finding $r$ in
> $O(n^3)$ time on $O(n)$ qubits, where $n = \log_2 N$. Classically, the best known
> algorithms take sub-exponential time. This is an exponential quantum speedup."

---

# Part 7: Why QFT Matters for DevRel

## Calibrating Expectations

- **The QFT itself is efficient** --- $O(n^2)$ gates. The bottleneck in Shor's is the
  **modular exponentiation oracle**, not the QFT. This nuance matters when discussing
  when quantum computers will break RSA.
- **Don't conflate QFT efficiency with overall algorithm efficiency.** The oracle cost
  dominates in practice.

## Bridge Between Math and Hardware

Explaining QFT requires connecting:

- **Fourier analysis** (pure math)
- **Circuit construction** (engineering)
- **Applications** (cryptography, chemistry)

This makes it ideal DevRel territory.

## Quantum Chemistry Connection

QPE is how future quantum computers will estimate molecular ground state energies ---
the most commercially promising application. The Hamiltonian $H$ is exponentiated to
create $U = e^{-iHt}$, and QPE extracts the eigenvalues (energy levels).

---

# Part 8: Exercise Solutions Walkthrough

## Exercise 1: DFT and QFT Matrix

- `classical_dft_matrix(N)` --- Builds the $N \times N$ DFT matrix using
  $\omega^{jk}/\sqrt{N}$ with `np.meshgrid` for the index products.
- `qft_matrix(n)` --- Simply calls `classical_dft_matrix(2**n)`.
- `verify_qft_properties(n)` --- Checks unitarity ($Q Q^\dagger = I$), symmetry
  ($Q = Q^T$), fourth power identity ($Q^4 = I$), and that QFT maps
  $|0\rangle$ to uniform superposition.

## Exercise 2: QFT Circuit

- `qft_circuit(n)` --- For each qubit $j$: Hadamard, then controlled-$R_k$ from later
  qubits with angle $2\pi/2^{k+1}$, finally SWAPs. Uses `qc.cp(angle, ctrl, tgt)`.
- `inverse_qft_circuit(n)` --- Simply `qft_circuit(n).inverse()`, leveraging Qiskit's
  built-in adjoint.

**Verification:** Circuit operator matches the QFT matrix, and QFT $\cdot$ QFT$^\dagger$ = $I$.

## Exercise 3: QFT on States

- `qft_on_basis_state(n, j)` --- Prepares $|j\rangle$ using X gates on appropriate
  qubits, applies QFT circuit, returns `Statevector`.
- `qft_on_periodic_state(n, r)` --- Builds periodic state vector manually (uniform
  over $\{|0\rangle, |r\rangle, |2r\rangle, \ldots\}$), applies QFT matrix directly.

## Exercise 4: QPE

- `qpe_circuit(U, n_c, prep)` --- Builds the full QPE circuit: Hadamards on counting
  qubits, eigenstate preparation, controlled-$U^{2^j}$ via `Operator.power()`, inverse
  QFT on counting register, measurement.
- `estimate_phase(U, eigenstate, n_c)` --- Runs QPE, takes the most-frequent bitstring,
  converts to phase: `measured_int / 2**n_counting`.

## Exercise 5: QPE Applications

- `qpe_t_gate(n_c)` --- QPE on T gate with $|1\rangle$ eigenstate. Exact for $\geq 3$
  counting qubits since $1/8 = 0.001_2$.
- `qpe_rotation_gate(θ, n_c)` --- QPE on $R_z(\theta)$, demonstrates precision
  limitations for non-binary phases.
- `shor_connection(N)` --- Returns a detailed text explanation tracing the full chain
  from factoring through order finding to QPE to QFT.

---

# Part 9: Quick Reference Card

## Essential QFT Formulas

| Concept | Formula |
|:--------|:--------|
| DFT matrix entry | $(\text{DFT})_{kj} = \omega^{jk}/\sqrt{N}$ where $\omega = e^{2\pi i/N}$ |
| QFT on basis state | $\text{QFT}|j\rangle = (1/\sqrt{N}) \sum_k e^{2\pi ijk/N}|k\rangle$ |
| Controlled rotation | $R_k = \text{diag}(1, e^{2\pi i/2^k})$ |
| QFT gate count | $n(n+1)/2 + \lfloor n/2 \rfloor = O(n^2)$ |
| Periodicity $\to$ peaks | Period $r$ input $\to$ peaks at multiples of $N/r$ |

## Essential QPE Formulas

| Concept | Formula |
|:--------|:--------|
| Eigenvalue problem | $U|\psi\rangle = e^{2\pi i\phi}|\psi\rangle$ |
| Precision | $2^{-n}$ for $n$ counting qubits |
| Shor: order finding | $a^r \equiv 1 \pmod{N}$, eigenvalues $e^{2\pi is/r}$ |
| Shor: factoring | $\gcd(a^{r/2} \pm 1, N)$ |
| Shor: quantum cost | $O(n^3)$ gates, $O(n)$ qubits, $n = \log_2 N$ |

## Key Numbers to Remember

- QFT on 20 qubits: 210 gates (vs 20M classical FFT operations)
- QPE precision: 3 qubits $\to 1/8$, 10 qubits $\to 1/1024$
- Shor for RSA-2048: approximately 4,096 logical qubits needed
- Current hardware: approximately 1,200 physical qubits (IBM Eagle/Condor)
- Surface code overhead: approximately 1,000--10,000 physical qubits per logical qubit

## Key Interview Quote

> "The Quantum Fourier Transform converts periodicity in the computational basis to
> peaks in the Fourier basis, using only $O(n^2)$ gates --- exponentially fewer than the
> classical FFT. Its most important application is Quantum Phase Estimation, which
> estimates eigenvalues of unitaries. QPE is the engine inside Shor's factoring algorithm:
> the modular exponentiation unitary has eigenvalues encoding the order $r$, QPE extracts
> $s/r$, and continued fractions give $r$. This chain --- factoring $\to$ order finding
> $\to$ phase estimation $\to$ QFT --- is the canonical example of exponential quantum
> advantage."

---

*End of Day 7 Summary. Week 1 complete!*
*Next: Day 8 --- Variational Quantum Algorithms (VQE, QAOA).*
