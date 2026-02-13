# The Geometry of Single-Qubit Gates

*Portfolio Artifact — Day 2*

---

## Why Geometry Matters in Quantum Computing

When engineers at IBM, Google, or Rigetti design quantum circuits, they don't think in matrices — they think in **rotations on a sphere**. Every single-qubit operation is a rotation of the Bloch vector, and understanding this geometry is the bridge between abstract linear algebra and physical hardware control.

---

## The Bloch Sphere: A Qubit's State Space

Any single-qubit pure state can be written as:

$$|\psi\rangle = \cos(\theta/2)|0\rangle + e^{i\phi}\sin(\theta/2)|1\rangle$$

This parametrization maps every qubit state to a point on the unit sphere:
- **θ** (polar angle): controls the balance between |0⟩ and |1⟩
- **φ** (azimuthal angle): controls the relative phase

The six cardinal states sit at the axis endpoints:

| Axis | + Direction | − Direction |
|------|-------------|-------------|
| Z    | \|0⟩ (north pole) | \|1⟩ (south pole) |
| X    | \|+⟩ = (|0⟩+|1⟩)/√2 | \|−⟩ = (|0⟩−|1⟩)/√2 |
| Y    | \|+i⟩ = (|0⟩+i|1⟩)/√2 | \|−i⟩ = (|0⟩−i|1⟩)/√2 |

---

## Rotation Gates: The Continuous Family

The three fundamental rotation gates are:

$$R_x(\theta) = e^{-i\theta X/2}, \quad R_y(\theta) = e^{-i\theta Y/2}, \quad R_z(\theta) = e^{-i\theta Z/2}$$

Each rotates the Bloch vector by angle θ around the corresponding axis.

### What this looks like geometrically:

**Rx(θ) on |0⟩:** Traces a great circle in the YZ plane.  
Path: |0⟩ → |−i⟩ → |1⟩ → |+i⟩ → |0⟩

**Ry(θ) on |0⟩:** Traces a great circle in the XZ plane.  
Path: |0⟩ → |+⟩ → |1⟩ → |−⟩ → |0⟩

**Rz(θ) on |+⟩:** Traces a circle around the equator.  
Path: |+⟩ → |+i⟩ → |−⟩ → |−i⟩ → |+⟩

### Critical observation:
Rz on |0⟩ does **nothing visible** — because |0⟩ sits on the Z-axis, and rotating around the axis you're already on leaves you in place (only adding a global phase).

---

## The Euler Decomposition: Why Two Axes Are Enough

The ZYZ Euler decomposition theorem states:

$$U = e^{i\alpha} \, R_z(\beta) \, R_y(\gamma) \, R_z(\delta)$$

for any single-qubit unitary U.

**Consequences for hardware:**
1. You only need Ry and Rz to implement **any** single-qubit gate
2. Named gates (H, T, S, X, Y, Z) are just specific rotation angles
3. The quantum compiler (transpiler) performs this decomposition automatically

### Named gates as rotations:

| Gate | Rotation Equivalent |
|------|-------------------|
| X | Rx(π) up to global phase |
| Y | Ry(π) up to global phase |
| Z | Rz(π) up to global phase |
| H | Ry(π/2) · Rz(π) up to global phase |
| S | Rz(π/2) up to global phase |
| T | Rz(π/4) up to global phase |

---

## State Preparation: Two Rotations Reach Anywhere

To prepare an arbitrary state from |0⟩:

1. **Ry(θ)** — sets the latitude (polar angle)
2. **Rz(φ)** — sets the longitude (azimuthal phase)

$$|\psi\rangle = R_z(\phi) \, R_y(\theta) |0\rangle$$

This is the essence of the **U3 gate** that IBM hardware implements. Any single-qubit state is two rotations away from |0⟩.

---

## What This Means for Real Hardware

On IBM quantum processors:

- **Rz is free.** It's implemented as a "frame change" in the control software — no physical microwave pulse needed, so it introduces zero error.
- **Physical gates** are √X (= Rx(π/2)) and X. These require actual microwave pulses and have finite error (~0.01-0.1%).
- **Ry is synthesized** from Rz and √X combinations.

So when you write `qc.h(0)` in Qiskit, the transpiler decomposes it to:

```
Rz(π/2) → √X → Rz(π/2)
```

Only the √X costs anything physically. **Single-qubit gates are essentially free compared to two-qubit gates (CNOT),** which have ~10× higher error rates.

This is why quantum circuit optimization focuses on minimizing CNOT count, not single-qubit gate count.

---

## Interview-Ready Insight

> "Every single-qubit gate is a rotation on the Bloch sphere, decomposable into Rz-Ry-Rz via Euler angles. On IBM hardware, Rz is virtual (zero error), so single-qubit operations are nearly free. The real challenge in quantum circuit optimization is minimizing two-qubit gate count."

This understanding separates someone who *knows the math* from someone who *understands the engineering*.

---

*Written as part of my Quantum DevRel preparation journey — Day 2.*
