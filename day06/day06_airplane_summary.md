---
title: "Day 6: Grover's Search Algorithm"
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
  - \fancyhead[L]{Day 6 — Grover's Search Algorithm}
  - \fancyhead[R]{Quantum DevRel Bootcamp}
  - \fancyfoot[C]{\thepage}
---

\newpage

# Part 1: The Big Picture — Searching Without Structure

Imagine a phone book with a million entries in random order. You're looking for one
specific name. Classically, there's no shortcut --- on average you check 500,000
entries. A quantum computer can find it in about 785 queries. That's Grover's
algorithm.

This isn't hype: it's a **provably optimal** quadratic speedup for unstructured
search, first discovered by Lov Grover in 1996.

**The core comparison:**

| Method | Queries for $N$ items | 1 million items | 1 billion items |
|:-------|:---------------------|:---------------|:---------------|
| Classical | $O(N)$ | 500,000 | 500,000,000 |
| Grover | $O(\sqrt{N})$ | 785 | 24,836 |

This quadratic speedup is **provably optimal** --- no quantum algorithm can do better
for unstructured search (Bennett, Bernstein, Brassard, Vazirani, 1997).

---

# Part 2: Oracles and Superposition — The Setup

## The Oracle Model

Grover's algorithm operates in the **oracle model**: you have a black box $O_f$ that
recognizes the answer. Feed it an input $x$, and it tells you "yes" ($f(x) = 1$) or
"no" ($f(x) = 0$). The question is: how many times do you need to call this oracle?

The quantum oracle works by **phase kickback**:

$$O_f|x\rangle = (-1)^{f(x)}|x\rangle$$

It flips the phase of the marked state --- a change invisible to direct measurement,
but crucial for interference.

## The Starting State

The algorithm begins by preparing a uniform superposition over all $N = 2^n$ states:

$$|s\rangle = H^{\otimes n}|0\rangle^{\otimes n} = \frac{1}{\sqrt{N}}\sum_{x=0}^{N-1}|x\rangle$$

Every state has amplitude $1/\sqrt{N}$. The marked state is hiding in plain sight ---
it has the same probability as everything else.

## Building the Oracle

The oracle as a matrix is diagonal in the computational basis:

$$O_f = I - 2|w\rangle\langle w|$$

For multiple marked states $\{w_1, w_2, \ldots\}$:

$$O_f = I - 2\sum_i |w_i\rangle\langle w_i|$$

As a circuit, for each marked state $|w\rangle$:

1. Apply X gates to qubits that are $|0\rangle$ in the binary representation of $w$
2. Apply a multi-controlled-Z gate (H-MCX-H on the target qubit)
3. Undo the X gates from step 1

> **Interview insight:** "The oracle is NOT the hard part of understanding Grover's
> algorithm --- *constructing* the oracle IS the hard part in real applications! For SAT
> problems, database search, or constraint satisfaction, designing an efficient oracle is
> where the actual engineering happens."

---

# Part 3: The Diffusion Operator — Inversion About the Mean

The diffusion operator reflects about the uniform superposition $|s\rangle$:

$$D = 2|s\rangle\langle s| - I$$

This is also called **inversion about the mean** because of what it does to amplitudes:
each amplitude $a_i$ is mapped to $2\bar{a} - a_i$ where $\bar{a}$ is the mean
amplitude.

## What Inversion About the Mean Does

States with amplitude *above* the mean get boosted. States *below* the mean get
suppressed. After the oracle flips the marked state's amplitude to negative, the mean
drops slightly, and the diffusion operator amplifies the marked state while suppressing
everything else.

**Concrete example** (2-qubit, target $|11\rangle$):

- After superposition: all amplitudes $= 0.5$
- After oracle: $|11\rangle$ has amplitude $-0.5$, others $= 0.5$
- Mean amplitude $= (0.5 + 0.5 + 0.5 + (-0.5))/4 = 0.25$
- After diffusion: $|11\rangle$: $2(0.25) - (-0.5) = 1.0$, others: $2(0.25) - 0.5 = 0.0$
- **One iteration gives 100\% success** for 2 qubits!

## Diffusion Circuit

| Step | Operation | Purpose |
|:-----|:----------|:--------|
| 1 | $H^{\otimes n}$ | Map $|s\rangle \to |0\rangle^n$ |
| 2 | $X^{\otimes n}$ | Prepare for multi-controlled Z |
| 3 | MCZ | Phase flip everything except $|0\rangle$ |
| 4 | $X^{\otimes n}$ | Undo step 2 |
| 5 | $H^{\otimes n}$ | Map back to original basis |

> **Interview insight:** "The diffusion operator is really a reflection about the mean
> amplitude. Geometrically, Grover's algorithm performs rotations in a 2D plane spanned
> by the marked states and their complement. Each iteration rotates by $2\theta$ where
> $\sin(\theta) = \sqrt{M/N}$."

---

# Part 4: The Geometry — Rotation in a 2D Plane

Here's the key insight that makes Grover's algorithm truly click. Define two states:

$$|w\rangle = \text{marked state(s)}, \qquad |w^\perp\rangle = \text{everything else}$$

The initial superposition $|s\rangle$ lives in the 2D plane spanned by $|w\rangle$
and $|w^\perp\rangle$:

$$|s\rangle = \sin\theta\,|w\rangle + \cos\theta\,|w^\perp\rangle, \quad \text{where } \sin\theta = \sqrt{M/N}$$

## Two Reflections = One Rotation

The oracle $O_f$ is a reflection about the $|w^\perp\rangle$ axis. The diffusion
operator $D$ is a reflection about the $|s\rangle$ direction. The composition
$D \cdot O_f$ is a rotation by $2\theta$ toward $|w\rangle$.

After $k$ iterations:

$$P(\text{success}) = \sin^2\left((2k+1)\theta\right)$$

The optimal number of iterations puts the argument at $\pi/2$:

$$k_{\text{opt}} = \left\lfloor\frac{\pi}{4\theta}\right\rceil \approx \frac{\pi}{4}\sqrt{\frac{N}{M}}$$

## How This Scales

| Qubits | $N$ | Optimal $k$ | $P(\text{success})$ | Classical queries |
|:------:|:---:|:-----------:|:-------------------:|:-----------------:|
| 2 | 4 | 1 | 100\% | 4 |
| 3 | 8 | 2 | 94.5\% | 8 |
| 4 | 16 | 3 | 96.1\% | 16 |
| 10 | 1,024 | 25 | 99.9\% | 1,024 |
| 20 | 1,048,576 | 804 | 99.9\% | 1,048,576 |

> **Interview insight:** "Grover's speedup is quadratic --- $\sqrt{N}$ instead of $N$.
> This is provably optimal for unstructured search. It's not exponential, but it's still
> significant: searching a million items takes about 785 queries instead of 500,000."

---

# Part 5: Amplitude Amplification Step by Step

Watching the amplitudes evolve makes the algorithm tangible. For a 3-qubit search with
target $|101\rangle$:

**After 0 iterations** (just $H^{\otimes 3}$):

- All 8 states: amplitude $= 1/\sqrt{8} \approx 0.354$
- $P(|101\rangle) = 12.5\%$

**After 1 iteration:**

- $|101\rangle$: amplitude $\approx 0.78$
- Others: amplitude $\approx 0.09$
- $P(|101\rangle) \approx 61\%$

**After 2 iterations (optimal):**

- $|101\rangle$: amplitude $\approx 0.97$
- Others: amplitude $\approx -0.02$
- $P(|101\rangle) \approx 94.5\%$

**After 4 iterations (over-iterated):**

- $P(|101\rangle)$ drops back to about 6\%

The probability oscillates sinusoidally. Each iteration adds another $2\theta$ rotation.
Going past the peak means rotating *beyond* the target.

> **Interview insight:** "Amplitude amplification is the general principle behind
> Grover's algorithm. It works for ANY initial state and ANY 'good' subspace ---
> Grover's search is just the special case where the initial state is uniform. This
> generality makes it a subroutine in many quantum algorithms."

---

# Part 6: The Soufflé Problem — Don't Over-Iterate

Here's a subtlety that surprises many: **too many iterations makes things worse.**
The success probability oscillates:

$$P(k) = \sin^2\left((2k+1)\theta\right)$$

If you apply 3 iterations to a 3-qubit search, success probability drops back to
about 33\%. Four iterations? Just 6\%. The state rotates past the target and keeps going.

This is sometimes called **Grover's soufflé** --- you must take it out of the oven at
exactly the right time.

**Practical implications:**

- You need to know (or estimate) the number of marked states $M$ to choose the optimal $k$
- If $M$ is unknown, **quantum counting** (QPE on the Grover operator) can estimate it ---
  combining Day 6 with Day 7
- Running with a random number of iterations gives roughly $50\%$ success probability
  (still better than classical for large $N$)

---

# Part 7: Multi-Solution Search

When $M > 1$ marked states exist, Grover's becomes *even more efficient*:

- **Fewer iterations:** $k \propto \sqrt{N/M}$
- **Equal distribution:** Each marked state gets roughly $1/M$ of the total success probability
- **Speedup preserved:** Classical $N/M$ vs quantum $\sqrt{N/M}$

For 8 items with 2 marked states: 1 iteration achieves about 78\% success, compared to
2 iterations needed for a single target.

| $N$ | $M$ | Optimal $k$ | Classical queries | Quantum queries | Speedup |
|:---:|:---:|:-----------:|:-----------------:|:---------------:|:-------:|
| 16 | 1 | 3 | 16 | 3 | 5.3$\times$ |
| 16 | 2 | 2 | 8 | 2 | 4.0$\times$ |
| 16 | 4 | 1 | 4 | 1 | 4.0$\times$ |
| 1024 | 1 | 25 | 1024 | 25 | 41$\times$ |

> **Interview insight:** "Grover's quadratic speedup holds for ANY number of marked
> states. With $M$ solutions out of $N$ items, the speedup is $\sqrt{N/M}$. But
> there's a catch: if you don't KNOW $M$, you need quantum counting to estimate it
> first."

---

# Part 8: What Grover's Is (and Isn't)

## Grover's IS:

- A provably optimal $O(\sqrt{N})$ algorithm for unstructured search
- A building block for **amplitude amplification** in many quantum algorithms
- Useful for constraint satisfaction, optimization heuristics, and cryptography analysis

## Grover's IS NOT:

- An exponential speedup (it's quadratic)
- A database query optimizer (you still need $O(\sqrt{N})$ oracle calls, and each
  call may be expensive to implement)
- Immediately practical on NISQ hardware (the depth grows with $\sqrt{N}$, and
  noise accumulates)

## Cryptographic Impact

For AES-128 key search: Grover reduces the search from $2^{128}$ to $2^{64}$ operations.
This is why post-quantum cryptography recommends **doubling key sizes** (AES-256),
not abandoning symmetric crypto entirely.

For RSA/ECC: the threat comes from Shor's algorithm (exponential speedup), not Grover
(quadratic).

---

# Part 9: Exercise Solutions Walkthrough

This section summarizes the key implementations, explaining the code logic for
airplane reading.

## Exercise 1: Oracle Construction

- `build_oracle_matrix(n, marked)` --- Creates a $2^n \times 2^n$ identity matrix and
  sets diagonal entries to $-1$ for each marked state index. Simple and direct.
- `build_oracle_circuit(n, marked)` --- For each marked state: X gates on zero-bits,
  MCZ (via H-MCX-H), undo X gates. Uses $O(n)$ gates per marked state.

## Exercise 2: Diffusion Operator

- `build_diffusion_matrix(n)` --- Computes $|s\rangle = \mathbf{1}/\sqrt{N}$ then
  returns $2|s\rangle\langle s| - I$ using `np.outer`.
- `build_diffusion_circuit(n)` --- H-all, X-all, MCZ, X-all, H-all. Exactly five
  layers of gates.

## Exercise 3: Complete Grover's Algorithm

- `optimal_iterations(n, M)` --- Implements $k = \text{round}(\pi/(4\theta) - 0.5)$
  where $\theta = \arcsin(\sqrt{M/N})$. Returns at least 1.
- `grover_circuit(n, marked, k)` --- H on all qubits, then $k$ repetitions of
  oracle + diffusion with barriers between, then measurement.
- `run_grover(n, marked)` --- Builds circuit, runs on `AerSimulator`, returns counts.

## Exercise 4: Amplitude Amplification Analysis

- `success_probability(n, M, k)` --- Analytical formula
  $\sin^2((2k+1)\theta)$, matching simulation exactly.
- `amplitude_evolution(n, marked, k_{max})` --- Incrementally applies oracle and
  diffusion matrices to a state vector, tracking probabilities at each step. No
  measurement --- pure statevector simulation.

## Exercise 5: Multi-Solution & Classical Comparison

- `classical_vs_quantum_queries(n, M)` --- Compares $N/M$ classical vs
  $\pi\sqrt{N/M}/4$ quantum queries. Returns speedup ratio.
- `multi_solution_grover(n, marked)` --- Runs Grover with multiple targets, measures
  success rate. Each marked state gets roughly equal probability.

---

# Part 10: Quick Reference Card

## Essential Formulas

| Concept | Formula |
|:--------|:--------|
| Oracle | $O_f = I - 2\sum_i|w_i\rangle\langle w_i|$ |
| Diffusion | $D = 2|s\rangle\langle s| - I$ |
| Initial angle | $\sin\theta = \sqrt{M/N}$ |
| Success probability | $P(k) = \sin^2((2k+1)\theta)$ |
| Optimal iterations | $k_{\text{opt}} \approx (\pi/4)\sqrt{N/M}$ |
| Speedup | $O(\sqrt{N/M})$ quantum vs $O(N/M)$ classical |

## Key Interview Quote

> "Grover's algorithm is a rotation in a 2D subspace. The oracle marks the target
> by flipping its phase, and the diffusion operator reflects about the mean --- two
> reflections make a rotation. After $\pi\sqrt{N}/4$ rotations, you land on the
> target with near-certainty. It's a quadratic speedup, not exponential, but it's
> provably optimal for unstructured search and serves as a building block for
> amplitude amplification across many quantum algorithms."

## Numbers to Remember

- 2 qubits: 1 iteration, 100\% success
- 3 qubits: 2 iterations, 94.5\% success
- 10 qubits (1,024 items): 25 iterations
- 20 qubits (1M items): 804 iterations
- Speedup for $N=10^6$: 500,000 vs 785 queries (about 640$\times$)
- Cryptographic impact: AES-128 $\to$ AES-256 (double key length)

---

*End of Day 6 Summary. Tomorrow: Quantum Fourier Transform!*
