# Quantum Computing Intensive Training

## 14-Day Bootcamp: From Mathematician to Quantum DevRel

> *"Two weeks won't make you a quantum engineer. But two weeks can absolutely make you dangerous."*

This repository documents my intensive journey from strong mathematical background to industry-ready **Quantum Developer Advocate**. Each day produces working code, portfolio artifacts, and interview-ready knowledge.

## 🎯 Goals

- Master applied quantum computing fundamentals through hands-on implementation
- Build working **Qiskit** competence with real SDK patterns
- Create visible **portfolio artifacts** that demonstrate technical communication
- Prepare for technical interviews at quantum companies
- Develop the ability to **explain quantum concepts** to diverse audiences

## 🏢 Target Companies

| Company | Focus | Why They Hire DevRel |
|---------|-------|---------------------|
| **IBM Quantum** | Superconducting qubits, Qiskit | Largest ecosystem, need educators for Qiskit adoption |
| **Xanadu** | Photonic QC, PennyLane | Growing framework, need developer community |
| **Rigetti** | Superconducting, pyQuil | Cloud-first, need users for QCS platform |
| **Quantinuum** | Trapped ions, TKET | Enterprise focus, need technical evangelists |
| **D-Wave** | Quantum annealing, Ocean | Optimization focus, need industry outreach |

---

## 📋 Daily Curriculum

Each day follows the same structure:
- 📓 **Interactive Notebook** — guided learning with runnable code
- 💪 **Exercises** — implement functions yourself (with test suite)
- ✅ **Solutions** — reference implementations with detailed explanations
- 📝 **Portfolio Artifact** — written piece demonstrating understanding

---

### Week 1 — Foundations + Quantum Control

#### Day 1: Python Engineering + Quantum State Formalism ✅
> *Build your engineering foundation and master single-qubit math*

**Concepts:**
- Complex vector normalization (Born rule connection)
- Unitary matrix verification (why quantum gates must be unitary)
- Tensor products — manual Kronecker product implementation
- Single qubit states: |0⟩, |1⟩, |+⟩, |−⟩, |+i⟩, |−i⟩
- Pauli gates (X, Y, Z) and Hadamard gate
- Measurement probabilities via Born's rule
- Bloch sphere visualization

**Deliverables:**
- `normalize_vector()` — normalizes complex quantum state vectors
- `is_unitary()` — verifies quantum gate validity
- `tensor_product()` — manual implementation (no `np.kron`)
- Portfolio: *"Why a Qubit is NOT a Probabilistic Bit"*

**Key files:** `day01/exercises.py` · `day01/solutions.py` · `day01/block2_single_qubit.py` · `day01/day01_notebook.ipynb`

---

#### Day 2: Single Qubit Rotations in Qiskit ✅
> *Transition from NumPy to industry-standard Qiskit SDK*

**Concepts:**
- Qiskit `QuantumCircuit`, `Statevector`, `Operator`
- Rotation gates Rx(θ), Ry(θ), Rz(θ) as continuous gate families
- Bloch sphere trajectories — each rotation traces a great circle
- Euler decomposition (ZYZ): any gate = Rz·Ry·Rz
- Arbitrary state preparation with Ry(θ)·Rz(φ)
- Circuit transpilation to IBM native gates (rz, sx, x)
- Gate composition: circuit order vs matrix multiplication order

**Deliverables:**
- Manual rotation matrices verified against Qiskit
- Interactive Bloch sphere rotation trajectories (Plotly)
- Hadamard decomposed into rotation gates
- `prepare_arbitrary_state(θ, φ)` circuit
- Portfolio: *"The Geometry of Single-Qubit Gates"*

**Key files:** `day02/exercises.py` · `day02/solutions.py` · `day02/day02_notebook.ipynb`

---

#### Day 3: Multi-Qubit Systems & Entanglement ✅
> *The source of quantum computational power*

**Concepts:**
- Multi-qubit state spaces: ℂ²ⁿ tensor product structure
- CNOT gate — the fundamental two-qubit entangling gate
- Bell states — the four maximally entangled two-qubit states
- Separable vs entangled states (Schmidt decomposition)
- Partial measurement and post-measurement states
- No-cloning theorem
- GHZ and W states (3+ qubits)

**Deliverables:**
- Build all 4 Bell state circuits in Qiskit
- Entanglement verification (partial trace test)
- Bell state measurement and correlation analysis
- Portfolio: *"Entanglement: The Resource That Makes Quantum Computing Possible"*

---

#### Day 4: Quantum Circuits as Matrix Operations ✅
> *Deep circuit-matrix correspondence and universal gate sets*

**Concepts:**
- Multi-qubit gate matrices (CNOT, SWAP, Toffoli)
- Controlled gates: controlled-Z, controlled-phase
- Universal gate sets: {H, T, CNOT} and why they're sufficient
- Circuit identities and equivalences
- Quantum circuit depth vs width
- Introduction to Qiskit Aer simulator

**Deliverables:**
- Manual multi-qubit gate matrices verified against Qiskit
- SWAP gate from three CNOTs
- Toffoli gate decomposition
- Simulate circuits with measurement statistics
- Portfolio: *"What Makes a Gate Set Universal?"*

---

#### Day 5: Noise & Reality (NISQ Era) ✅
> *Understand why real quantum computers make errors*

**Concepts:**
- Density matrices and mixed states
- Quantum channels: depolarizing, amplitude damping, phase damping
- Qiskit Aer noise models
- Gate fidelity and error rates
- T1/T2 coherence times
- NISQ (Noisy Intermediate-Scale Quantum) limitations
- Simulating circuits with realistic noise

**Deliverables:**
- Implement basic noise channels as Kraus operators
- Compare ideal vs noisy simulation results
- Visualize noise effects on Bloch sphere
- Portfolio: *"The NISQ Reality: Why Quantum Error Matters"*

---

#### Day 6: Grover's Search Algorithm
> *Your first real quantum algorithm with provable speedup*

**Concepts:**
- Oracle-based quantum computing model
- Grover's algorithm: O(√N) search in unstructured databases
- Amplitude amplification — geometric interpretation
- Oracle construction for specific search problems
- Multi-qubit Grover: marking multiple solutions
- Optimal number of iterations
- Comparison: classical O(N) vs quantum O(√N)

**Deliverables:**
- Implement Grover's oracle for 2, 3, and 4 qubit cases
- Visualize amplitude amplification step by step
- Analyze success probability vs iteration count
- Portfolio: *"Grover's Algorithm: A Visual Explanation"*

---

#### Day 7: Quantum Fourier Transform
> *The mathematical heart of Shor's algorithm*

**Concepts:**
- Classical DFT → QFT correspondence
- QFT circuit construction (Hadamard + controlled rotations)
- Quantum phase estimation (QPE)
- Connection to Shor's factoring algorithm
- QFT as a change of basis
- Inverse QFT and measurement

**Deliverables:**
- Build QFT circuit from scratch for n qubits
- Implement quantum phase estimation
- Demonstrate QPE on a known eigenvalue problem
- Portfolio: *"From Fourier to Factoring: Why QFT Matters"*

---

### Week 2 — Industry Positioning & Applications

#### Day 8: Variational Quantum Algorithms (VQAs)
> *The dominant paradigm for near-term quantum applications*

**Concepts:**
- Variational Quantum Eigensolver (VQE)
- Parameterized quantum circuits (ansätze)
- Classical-quantum hybrid optimization loop
- Cost function landscapes and barren plateaus
- QAOA for combinatorial optimization
- Qiskit Runtime primitives: Sampler and Estimator

**Deliverables:**
- Implement VQE for H₂ molecule ground state energy
- Visualize the optimization landscape
- Compare different ansatz choices
- Portfolio: *"VQE Explained: Quantum Chemistry on Today's Hardware"*

---

#### Day 9: Error Mitigation Techniques
> *Practical techniques for extracting signal from noisy quantum computers*

**Concepts:**
- Zero-noise extrapolation (ZNE)
- Probabilistic error cancellation (PEC)
- Measurement error mitigation (readout correction)
- Dynamical decoupling
- Twirled readout error extinction (TREX)
- Qiskit Runtime resilience levels

**Deliverables:**
- Implement ZNE on a simple circuit
- Compare mitigated vs unmitigated results
- Benchmark different mitigation strategies
- Portfolio: *"Error Mitigation: Making NISQ Computers Useful"*

---

#### Day 10: Technical Talk Preparation
> *Build a 10-minute conference-quality technical talk*

**Concepts:**
- DevRel presentation structure (hook → concept → demo → takeaway)
- Live coding demonstration techniques
- Audience calibration: physicist vs developer vs executive
- Storytelling with quantum concepts

**Deliverables:**
- Slide deck outline for "Introduction to Quantum Computing for Developers"
- Live demo script with working Qiskit code
- Record practice run (self-review)
- Portfolio: *Talk materials + demo notebook*

---

#### Day 11: Deep Dive Technical Article
> *Write a publication-quality technical blog post*

**Concepts:**
- Technical writing for developer audiences
- Balancing depth with accessibility
- Code examples as teaching tools
- SEO and discoverability for technical content

**Deliverables:**
- 2000+ word technical article (publishable on Medium/dev.to)
- Topic: Choose from quantum advantage, VQE walkthrough, or error mitigation guide
- Include working code examples and visualizations
- Portfolio: *Published technical article*

---

#### Day 12: Mock Interview Practice
> *Prepare for real DevRel interview questions*

**Concepts:**
- Common quantum DevRel interview formats
- Technical depth questions (explain X to different audiences)
- Live coding / whiteboard quantum circuits
- "Teach me quantum computing in 5 minutes" scenarios
- Community building and developer experience questions

**Deliverables:**
- Written answers to 10 common interview questions
- 5-minute "explain quantum computing" recorded pitch
- Technical exercise: design a workshop curriculum
- Portfolio: *Interview preparation document*

---

#### Day 13: Portfolio Polish & GitHub Presence
> *Make everything presentation-ready*

**Concepts:**
- GitHub profile optimization for quantum roles
- README documentation best practices
- Code quality and documentation review
- Portfolio website / blog setup

**Deliverables:**
- All notebooks cleaned, tested, and well-commented
- Repository README with clear navigation
- LinkedIn/GitHub profile updated with quantum focus
- Portfolio: *Polished public repository*

---

#### Day 14: Application Strategy & Next Steps
> *Convert preparation into job applications*

**Concepts:**
- Quantum computing job market landscape
- Tailoring applications to specific companies
- Networking in the quantum community
- Continuing education roadmap

**Deliverables:**
- Customized cover letter templates for each target company
- List of quantum conferences, meetups, and communities to join
- 30-day continuation plan for ongoing learning
- Portfolio: *Application materials + learning roadmap*

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.14 | Core language |
| Qiskit | IBM's quantum computing SDK |
| NumPy | Linear algebra computations |
| Matplotlib | Static visualizations |
| Plotly | Interactive 3D visualizations (Bloch sphere) |
| Jupyter | Interactive notebooks |
| Git | Version control + portfolio building |

## 📊 Progress

| Day | Topic | Status |
|-----|-------|--------|
| 1 | Python Engineering + Quantum State Formalism | ✅ Complete |
| 2 | Single Qubit Rotations in Qiskit | ✅ Complete |
| 3 | Multi-Qubit Systems & Entanglement | ✅ Complete |
| 4 | Quantum Circuits as Matrix Operations | ✅ Complete |
| 5 | Noise & Reality (NISQ Era) | ✅ Complete |
| 6 | Grover's Search Algorithm | ⬜ |
| 7 | Quantum Fourier Transform | ⬜ |
| 8 | Variational Quantum Algorithms | ⬜ |
| 9 | Error Mitigation Techniques | ⬜ |
| 10 | Technical Talk Preparation | ⬜ |
| 11 | Deep Dive Technical Article | ⬜ |
| 12 | Mock Interview Practice | ⬜ |
| 13 | Portfolio Polish | ⬜ |
| 14 | Application Strategy | ⬜ |
