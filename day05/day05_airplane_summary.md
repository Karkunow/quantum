---
title: "Day 5: Noise & Reality (NISQ Era)"
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
  - \fancyhead[L]{Day 5 — Noise \& Reality}
  - \fancyhead[R]{Quantum DevRel Bootcamp}
  - \fancyfoot[C]{\thepage}
---

\newpage

# Part 1: The Big Picture — Why Noise Matters

Every real quantum computer makes errors. Unlike classical computers, where a bit is
reliably 0 or 1, a qubit is fragile: it interacts with its environment and loses its
quantum properties over time. Day 5 is about understanding *why* this happens,
*how* we model it mathematically, and *what it means* for building useful quantum
applications.

**The key equation of the NISQ era:**

$$F \approx (1 - \varepsilon)^d$$

A circuit with depth $d$ and per-gate error rate $\varepsilon$ has fidelity that decays
*exponentially*. With current CNOT error rates of 0.1--1\%, you get at most a few
hundred useful gate layers. This single fact shapes the entire field.

---

# Part 2: Density Matrices — The Language of Noise

## Why We Need Density Matrices

Pure state vectors $|\psi\rangle$ cannot describe noise. When a qubit randomly
experiences an X error with probability $p$, it's not in *any single* quantum state ---
it's in a *classical mixture* of states. The **density matrix** handles both cases:

$$\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|$$

- **Pure state**: $\rho = |\psi\rangle\langle\psi|$ (rank 1, $\text{Tr}(\rho^2) = 1$)
- **Mixed state**: classical probability mixture ($\text{Tr}(\rho^2) < 1$)
- **Maximally mixed**: $\rho = I/d$ (no information, $\text{Tr}(\rho^2) = 1/d$)

## Purity: How "Quantum" Is Your State?

**Purity** $= \text{Tr}(\rho^2)$ measures how close a state is to a pure quantum state:

| State | Purity | Bloch Vector | Meaning |
|:------|:------:|:------------:|:--------|
| $|0\rangle$ | 1.0 | (0, 0, +1) | Pure, on sphere surface |
| $|+\rangle$ | 1.0 | (+1, 0, 0) | Pure, on sphere surface |
| 70/30 mix $|0\rangle$, $|1\rangle$ | 0.58 | (0, 0, +0.4) | Partially mixed, inside sphere |
| 50/50 mix $|0\rangle$, $|1\rangle$ | 0.5 | (0, 0, 0) | Maximally mixed, at center |

## Key Subtlety

A 50/50 mixture of $|0\rangle$ and $|1\rangle$ gives the *same* density matrix
($I/2$) as a 50/50 mixture of $|+\rangle$ and $|-\rangle$. Mixed states
erase the "recipe" --- you cannot tell which pure states were mixed to create them.

> **Interview insight:** "A density matrix is necessary whenever the system
> has classical uncertainty, not just quantum superposition. Noise *always*
> creates classical uncertainty, which is why density matrices are the
> native language of NISQ computing."

---

# Part 3: Quantum Noise Channels

## The Kraus Operator Formalism

A **quantum channel** (noise process) is described by a set of **Kraus operators** $\{K_i\}$:

$$\mathcal{E}(\rho) = \sum_i K_i \rho K_i^\dagger$$

with the **completeness relation** ensuring trace preservation:

$$\sum_i K_i^\dagger K_i = I$$

This is the most general description of a physical noise process on a quantum system.
Each $K_i$ represents one possible "way" the noise can act.

## The Five Standard Noise Channels

### 1. Bit-Flip Channel

**Physical model:** Random X errors (classical bit flip analog).

**Kraus operators:**
$$K_0 = \sqrt{1-p}\, I, \qquad K_1 = \sqrt{p}\, X$$

**Effect:** Shrinks the Z-axis of the Bloch sphere. The state's $z$-component
is multiplied by $(1-2p)$, while $x$ and $y$ components are preserved.

**Interview angle:** "The bit-flip channel is the quantum version of a binary
symmetric channel. With probability $p$, the qubit state is flipped by an X gate."

### 2. Phase-Flip Channel

**Physical model:** Random Z errors (pure dephasing, related to $T_2$).

**Kraus operators:**
$$K_0 = \sqrt{1-p}\, I, \qquad K_1 = \sqrt{p}\, Z$$

**Effect:** Shrinks the X-Y plane of the Bloch sphere (destroys coherence)
while preserving the Z component (populations stay the same).

**Interview angle:** "Phase flips are invisible in the computational basis ---
you only see them in superposition states. This is why quantum noise is
fundamentally different from classical noise."

### 3. Depolarizing Channel

**Physical model:** Equal probability of any Pauli error (X, Y, or Z).

**Kraus operators:**
$$K_0 = \sqrt{1 - \tfrac{3p}{4}}\, I, \quad
K_1 = \sqrt{\tfrac{p}{4}}\, X, \quad
K_2 = \sqrt{\tfrac{p}{4}}\, Y, \quad
K_3 = \sqrt{\tfrac{p}{4}}\, Z$$

**Equivalent form:**
$$\mathcal{E}(\rho) = (1-p)\,\rho + \frac{p}{3}(X\rho X + Y\rho Y + Z\rho Z)$$

At $p=1$, this maps any state to the maximally mixed state $I/2$.

**Effect:** Uniform shrinkage of the Bloch sphere --- it becomes a smaller sphere
centered at the origin. The Bloch vector is scaled by $(1-p)$.

**Interview angle:** "Depolarizing noise is the 'worst-case' model and often used
for back-of-the-envelope calculations. If a gate has depolarizing error $p$,
after $d$ gates the fidelity is roughly $(1-p)^d$."

### 4. Amplitude Damping Channel

**Physical model:** Energy relaxation ($T_1$ decay), like spontaneous emission.
An excited qubit ($|1\rangle$) decays to the ground state ($|0\rangle$) with
probability $\gamma$.

**Kraus operators:**
$$K_0 = \begin{pmatrix} 1 & 0 \\ 0 & \sqrt{1-\gamma} \end{pmatrix}, \qquad
K_1 = \begin{pmatrix} 0 & \sqrt{\gamma} \\ 0 & 0 \end{pmatrix}$$

**Effect:** The Bloch sphere shrinks *and drifts toward* $|0\rangle$ (the north pole).
Unlike other channels, this channel has a preferred direction --- it's not unital
(it doesn't preserve the maximally mixed state).

**Interview angle:** "Amplitude damping models $T_1$ relaxation. It's the only common
channel that's asymmetric --- $|1\rangle$ decays to $|0\rangle$ but not vice versa.
This is important for understanding qubit reset and measurement."

### 5. Phase Damping Channel

**Physical model:** Pure dephasing without energy loss; related to $T_2$ dephasing
beyond what $T_1$ contributes.

**Kraus operators:**
$$K_0 = \begin{pmatrix} 1 & 0 \\ 0 & \sqrt{1-\lambda} \end{pmatrix}, \qquad
K_1 = \begin{pmatrix} 0 & 0 \\ 0 & \sqrt{\lambda} \end{pmatrix}$$

**Effect:** Collapses the X-Y equatorial plane of the Bloch sphere while preserving
the Z axis. Destroys off-diagonal elements of $\rho$ (coherences) while leaving
diagonal elements (populations) unchanged.

**Interview angle:** "Phase damping is mathematically equivalent to measuring the
qubit in the Z basis with some probability. It kills superposition without
changing measurement probabilities."

## Summary Table: How Each Channel Deforms the Bloch Sphere

| Channel | X axis | Y axis | Z axis | Center drift? |
|:--------|:------:|:------:|:------:|:-------------:|
| Bit flip | $1$ | $1-2p$ | $1-2p$ | No |
| Phase flip | $1-2p$ | $1-2p$ | $1$ | No |
| Depolarizing | $1-p$ | $1-p$ | $1-p$ | No |
| Amplitude damping | $\sqrt{1-\gamma}$ | $\sqrt{1-\gamma}$ | $1-\gamma$ | Yes, toward $|0\rangle$ |
| Phase damping | $\sqrt{1-\lambda}$ | $\sqrt{1-\lambda}$ | $1$ | No |

> **Key visual:** If you plotted the Bloch sphere under depolarizing noise, it becomes
> a smaller sphere (uniform shrinkage). Under amplitude damping, it becomes an
> egg-shaped blob sliding toward the north pole. Under phase damping, it collapses
> into a vertical line segment on the Z axis.

---

# Part 4: T1 and T2 Coherence Times

## The Two Timescales of Qubit Death

Real qubit noise is dominated by two exponential decay processes:

### $T_1$ — Energy Relaxation Time

- **What it measures:** How long before $|1\rangle$ decays to $|0\rangle$
- **Physical process:** Spontaneous emission (energy loss to environment)
- **Channel model:** Amplitude damping with $\gamma = 1 - e^{-t/T_1}$
- **Decay law:** $P(|1\rangle$ at time $t) = e^{-t/T_1}$

### $T_2$ — Dephasing Time

- **What it measures:** How long before superposition coherence is lost
- **Physical process:** Random phase accumulation from environmental noise
- **Channel model:** Phase damping with $\lambda = 1 - e^{-t/T_2}$
- **Decay law:** Off-diagonal element $|\rho_{01}(t)| = |\rho_{01}(0)|\, e^{-t/T_2}$

### The $T_2 \leq 2T_1$ Constraint

$T_1$ processes *also* cause dephasing (if the qubit decays, it certainly loses
its phase). Therefore:

$$\frac{1}{T_2} = \frac{1}{2T_1} + \frac{1}{T_\phi}$$

where $T_\phi$ is the *pure dephasing* time. Since $T_\phi > 0$, we always have
$T_2 \leq 2T_1$.

## Typical Numbers (IBM Superconducting Qubits)

| Parameter | Typical Value | What It Means |
|:----------|:-------------|:--------------|
| $T_1$ | 100--300 $\mu$s | Qubit "lifetime" |
| $T_2$ | 50--200 $\mu$s | Coherence window |
| 1Q gate time | ~35 ns | Very fast |
| CNOT gate time | ~300--600 ns | 10x slower than 1Q |
| Gate budget | ~330--660 CNOTs | $T_2 / t_\text{CNOT}$ |

**The coherence budget:** You can execute roughly $T_2 / t_\text{gate}$ operations
before the qubit loses its quantum properties. For CNOTs at 300 ns with
$T_2 = 200\,\mu$s, that's about 660 CNOTs --- total, not per qubit.

> **Interview insight:** "When someone asks 'how many qubits does your processor
> have?' the real question should be 'what's your gate fidelity and $T_2$ time?'
> 1000 noisy qubits are less useful than 100 clean ones."

---

# Part 5: Qiskit Aer Noise Simulation

## Building Noise Models

Qiskit Aer lets you bridge the gap between ideal simulation and real hardware
by adding gate errors:

```python
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

model = NoiseModel()
model.add_all_qubit_quantum_error(
    depolarizing_error(0.001, 1),   # 0.1% error on 1Q gates
    ['h', 'x', 'sx', 'rz']
)
model.add_all_qubit_quantum_error(
    depolarizing_error(0.01, 2),    # 1% error on 2Q gates
    ['cx']
)
sim = AerSimulator(noise_model=model)
```

## Bell State Under Noise: A Concrete Example

A simple Bell state circuit ($H \to \text{CNOT}$) shows how noise manifests:

| Noise Level | $|00\rangle + |11\rangle$ (correct) | $|01\rangle + |10\rangle$ (errors) |
|:------------|:-----------------------------------:|:-----------------------------------:|
| Ideal | ~100% | ~0% |
| 1% CNOT error | ~97% | ~3% |
| 10% CNOT error | ~85% | ~15% |

The "leaked" probability into $|01\rangle$ and $|10\rangle$ comes directly from
depolarizing noise acting on the CNOT gate.

## Fidelity Scaling with Depth

When you chain more gates, noise compounds exponentially:

- **1% error, 10 layers:** $F \approx 0.99^{10} \approx 0.90$ (still usable)
- **1% error, 100 layers:** $F \approx 0.99^{100} \approx 0.37$ (garbage)
- **0.1% error, 100 layers:** $F \approx 0.999^{100} \approx 0.90$ (fine)

This is why error rates are the *single most important metric* for quantum hardware.

> **Interview insight:** "I always estimate circuit fidelity as $(1-\varepsilon)^d$
> before running on hardware. If that number is below 0.5, I know the results will
> be meaningless. This back-of-the-envelope check saves a lot of wasted QPU time."

---

# Part 6: The NISQ Wall

## What Is the NISQ Wall?

The useful circuit depth is bounded by:

$$d_{\max} \approx \frac{1}{\varepsilon}$$

| CNOT Error Rate | Max Useful Depth | What You Can Run |
|:----------------|:----------------:|:-----------------|
| 1% ($10^{-2}$) | ~100 layers | Simple VQE, QAOA $p=1$ |
| 0.1% ($10^{-3}$) | ~1,000 layers | Deeper variational circuits |
| 0.01% ($10^{-4}$) | ~10,000 layers | Approaching error correction threshold |

**The GHZ test:** A GHZ state on $n$ qubits requires $n-1$ CNOTs arranged linearly.
At 5% CNOT error, even a 5-qubit GHZ state drops below 50% fidelity. At 0.1%
error, you can reach ~20 qubits before significant degradation.

## Why NISQ Algorithms Are Shallow

This is why NISQ-era algorithms are specifically designed to be *shallow*:

- **VQE (Variational Quantum Eigensolver):** Short parameterized circuits, optimize
  classically
- **QAOA:** Circuit depth is a tuneable parameter $p$ (usually $p=1$ or $p=2$)
- **Quantum kernels:** Only need $O(n)$ gates per data point
- **Error mitigation:** Post-processing techniques (ZNE, PEC, Clifford data
  regression) that squeeze more signal from noisy results

None of these *solve* the noise problem --- they work *around* it by staying
within the coherence budget.

## The Path Forward

1. **Better qubits:** Lower error rates push the NISQ wall further out
2. **Error mitigation:** Extract useful signal from noisy results (near-term)
3. **Quantum error correction:** Logical qubits from many physical qubits (long-term)
   - Threshold theorem: if $\varepsilon < \varepsilon_\text{th} \approx 10^{-3}$ to $10^{-4}$,
     you can correct errors with polynomial overhead
   - Current best: surface codes, requiring ~1000 physical qubits per logical qubit

---

# Part 7: Exercise Solutions & Code Walkthrough

This section summarizes the key implementations from the exercises and solutions,
explaining the code logic without requiring you to run anything.

## Exercise 1: Density Matrix Foundations

**Functions implemented:**

- `pure_state_dm(state_label)` — Builds $\rho = |\psi\rangle\langle\psi|$ using
  `np.outer(psi, psi.conj())`
- `mixed_state_dm(states, probs)` — Computes $\rho = \sum p_i |\psi_i\rangle\langle\psi_i|$
- `purity(rho)` — Returns $\text{Tr}(\rho^2)$ using `np.trace(rho @ rho).real`

**Key test:** The maximally mixed state $I/2$ has purity exactly $0.5$, while any
pure state has purity $1.0$.

## Exercise 2: Kraus Operator Channels

**Functions implemented:**

- `apply_channel(rho, kraus_ops)` — The universal formula
  $\sum_i K_i \rho K_i^\dagger$
- `bit_flip_channel(p)` — Returns $[\sqrt{1-p}\,I, \sqrt{p}\,X]$
- `phase_flip_channel(p)` — Returns $[\sqrt{1-p}\,I, \sqrt{p}\,Z]$
- `depolarizing_channel(p)` — Returns four Kraus operators for Pauli noise
- `amplitude_damping_channel(gamma)` — Returns the asymmetric $K_0, K_1$ pair
- `noisy_superposition(p)` — Applies bit-flip to $|+\rangle$, returns purity

**Verification:** Each channel passes the completeness check
$\sum K_i^\dagger K_i = I$ (tested with `np.allclose`).

## Exercise 3: T1 Decay and Time Evolution

**Functions implemented:**

- `t1_decay(gamma)` — Applies amplitude damping to $|1\rangle$, returns $P(|1\rangle)$
- `t1_vs_time(T1, times)` — Maps time array to gamma values and tracks decay

**Key result:** The decay curve perfectly matches the analytical $e^{-t/T_1}$.

## Exercise 4: Qiskit Aer Noise Models

**Functions implemented:**

- `build_simple_noise_model(p1, p2)` — Creates a `NoiseModel` with depolarizing
  errors on single-qubit gates ($p_1$) and two-qubit gates ($p_2$)
- `simulate_with_noise(circuit, noise_model, shots)` — Runs on `AerSimulator`
  with the noise model attached
- `compare_bell_state(noise_model, shots)` — Measures Bell state fidelity as
  $(\text{count}_{00} + \text{count}_{11}) / \text{shots}$

**Key result:** Even mild noise (1% CNOT error) introduces measurable infidelity
in a Bell state.

## Exercise 5: Fidelity Scaling

**Functions implemented:**

- `calculate_fidelity_vs_noise(error_rates, circuit, shots)` — Sweeps CNOT
  error rate and measures fidelity degradation
- `bloch_under_noise(rho, channel_fn, params)` — Tracks Bloch vector
  trajectory as noise strength increases

**Key result:** Fidelity vs. error rate closely follows the theoretical
$(1-\varepsilon)^d$ curve for small error rates.

---

# Part 8: Portfolio Artifact — The NISQ Reality

*This section contains the polished portfolio write-up from Day 5.*

## The NISQ Reality: Why Quantum Error Matters

Quantum computing promises exponential speedups, but there is a catch: every
operation on a real quantum computer introduces errors. Understanding these errors
--- and how to work with them --- is one of the most important skills in quantum computing today.

### The Noise Model Zoo

Real quantum hardware faces several distinct noise processes, each with a different
physical origin and mathematical description.

**Bit-Flip (X Error):** The quantum analog of a classical bit flip. With probability $p$,
the qubit state is flipped: $|0\rangle \to |1\rangle$ and vice versa.

**Phase-Flip (Z Error):** Unique to quantum computing with no classical analog.
$|+\rangle \to |-\rangle$ while $|0\rangle$ and $|1\rangle$ appear unchanged.
This is why quantum error correction is fundamentally harder than classical.

**Depolarizing:** With probability $p$, the qubit is replaced by the maximally mixed state.
This is the "worst-case" noise model, often used for theoretical bounds.

**Amplitude Damping ($T_1$):** Energy relaxation where $|1\rangle$ decays to $|0\rangle$.
This is a *non-unital* channel --- it has a preferred direction.

**Phase Damping ($T_2$):** Pure dephasing that destroys off-diagonal coherences without
changing populations. The quantum equivalent of a clock running at a slightly random
speed.

### Fidelity: The Metric That Matters

Circuit fidelity decays exponentially with depth:

$$F \approx (1 - \varepsilon)^d$$

With $\varepsilon = 0.01$ (1% CNOT error), by depth 100 you retain only 37% fidelity.
With $\varepsilon = 0.001$ (0.1% error), you can reach depth 1000 at 90% fidelity.

This exponential decay is *the* central challenge of quantum computing. It's why:

- **NISQ algorithms** like VQE and QAOA use shallow circuits
- **Error mitigation** techniques exist (zero-noise extrapolation, probabilistic
  error cancellation)
- **Quantum error correction** will eventually be needed for deep circuits

### Why This Matters for DevRel

When communicating about quantum computing, the noise story is essential context:

1. **Don't overpromise:** A 1000-qubit processor with 1% error rates can only
   run circuits ~100 layers deep usefully
2. **Hardware metrics matter:** Quote gate fidelities, not just qubit counts
3. **Benchmarks need noise context:** A simulation result without noise modeling
   tells you about the algorithm, not the hardware
4. **Error mitigation is a real skill:** Knowing how to extract signal from noise
   is as important as circuit design

### Interview Takeaway

> "The NISQ era is defined by limited coherence: every gate adds noise, and fidelity
> drops as $(1-\varepsilon)^d$. I always start by estimating whether a circuit can
> survive the noise budget. For a typical IBM system with 0.5% CNOT error and
> $T_2 \approx 150\,\mu$s, you get roughly 200-500 useful two-qubit gates.
> Everything I design in the NISQ era --- VQE ansatze, QAOA layers, kernel circuits
> --- respects this budget."

---

# Part 9: Quick Reference Card

## Essential Formulas

| Concept | Formula |
|:--------|:--------|
| Density matrix | $\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|$ |
| Purity | $\text{Tr}(\rho^2)$, ranges from $1/d$ to $1$ |
| Quantum channel | $\mathcal{E}(\rho) = \sum_i K_i \rho K_i^\dagger$ |
| Completeness | $\sum_i K_i^\dagger K_i = I$ |
| Fidelity decay | $F \approx (1-\varepsilon)^d \approx e^{-\varepsilon d}$ |
| Max depth | $d_{\max} \approx 1/\varepsilon$ |
| $T_1$ decay | $P(|1\rangle) = e^{-t/T_1}$ |
| $T_2$ dephasing | $|\rho_{01}| = |\rho_{01}(0)| e^{-t/T_2}$ |
| $T_2$ constraint | $1/T_2 = 1/(2T_1) + 1/T_\phi$ |
| Gate budget | $\approx T_2 / t_\text{gate}$ operations |

## Five Channels At a Glance

| Channel | Kraus Operators | Bloch Effect |
|:--------|:---------------|:-------------|
| Bit flip | $\sqrt{1-p}\,I$, $\sqrt{p}\,X$ | Shrinks Z |
| Phase flip | $\sqrt{1-p}\,I$, $\sqrt{p}\,Z$ | Shrinks X-Y |
| Depolarizing | 4 operators (I, X, Y, Z weighted) | Uniform shrink |
| Amp. damping | $2\times 2$ matrices with $\sqrt{\gamma}$ | Shrink + drift to $|0\rangle$ |
| Phase damping | $2\times 2$ diagonal matrices | Collapses X-Y to Z |

## Key Numbers to Remember

- IBM $T_1$: 100--300 $\mu$s
- IBM $T_2$: 50--200 $\mu$s
- 1Q gate: ~35 ns, CNOT: ~300--600 ns
- CNOT fidelity: ~99.0--99.5% (state of the art: >99.9%)
- Gate budget: ~300--1000 CNOTs
- NISQ useful depth: ~$1/\varepsilon$ layers
- Error correction threshold: $\varepsilon \approx 10^{-3}$ to $10^{-4}$

---

*End of Day 5 Summary. Tomorrow: Grover's Search Algorithm!*
