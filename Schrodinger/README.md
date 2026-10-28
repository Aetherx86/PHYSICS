# Erwin Schrödinger: Wave Mechanics & The Wave Equation

Interactive Wave Equation Engine, Infinite Potential Well Solver, Quantum Harmonic Oscillator Spectrum, and Probability Density Suite

## Theoretical Foundation

In 1926, Erwin Schrödinger published his foundational series of papers entitled *Quantisierung als Eigenwertproblem* ("Quantization as an Eigenvalue Problem"). Synthesizing Louis de Broglie's matter-wave hypothesis with Hamiltonian analytical mechanics, Schrödinger replaced classical particle trajectories with complex continuous wavefields $\psi(\mathbf{r}, t)$. The temporal evolution is governed by the Time-Dependent Schrödinger Equation (TDSE):

$$i\hbar \frac{\partial \psi(\mathbf{r}, t)}{\partial t} = \hat{H}\psi(\mathbf{r}, t) = \left( -\frac{\hbar^2}{2m}\nabla^2 + V(\mathbf{r}, t) \right) \psi(\mathbf{r}, t)$$

Under conservative potentials $V(\mathbf{r})$, separation of variables yields the stationary Time-Independent Schrödinger Equation (TISE):

$$\hat{H}\psi_n(\mathbf{r}) = E_n \psi_n(\mathbf{r})$$

By Max Born's statistical postulate, the probability of locating the particle in an infinitesimal spatial volume $d^3\mathbf{r}$ is given by the positive definite scalar density:

$$\rho(\mathbf{r}, t) = |\psi(\mathbf{r}, t)|^2 = \psi^*(\mathbf{r}, t)\psi(\mathbf{r}, t)$$

which rigorously satisfies local probability conservation via the probability current density $\mathbf{j}$:

$$\frac{\partial \rho}{\partial t} + \nabla \cdot \mathbf{j} = 0, \quad \mathbf{j} = \frac{\hbar}{2mi}\left(\psi^* \nabla\psi - \psi\nabla\psi^*\right)$$

---

## Canonical Solved Potentials

### 1. The Infinite Potential Well (Particle in a Box)
For a particle confined within $[0, L]$ by infinite barrier walls $V(x) = \infty$ for $x \notin [0, L]$, the stationary wavefunctions are sinusoidal standing waves:

$$\psi_n(x) = \sqrt{\frac{2}{L}} \sin\left(\frac{n\pi x}{L}\right), \quad n \in \{1, 2, 3, \dots\}$$

The boundary conditions enforce exact discrete energy quantization:

$$E_n = \frac{n^2 \pi^2 \hbar^2}{2mL^2} \propto n^2$$

### 2. The Quantum Harmonic Oscillator
For a restoring potential $V(x) = \frac{1}{2}m\omega^2 x^2$, the stationary energy eigenvalues possess a non-vanishing vacuum ground-state energy:

$$E_n = \left(n + \frac{1}{2}\right)\hbar\omega$$

---

## Installation & Setup

Zero third-party dependencies required. Built exclusively with Python 3.9+ standard libraries.

```bash
git clone https://gitlab.com/jk9576/Schrodinger.git
cd Schrodinger
```

Run test suite:
```bash
python3 -m unittest discover tests -v
```

---

## Usage

### Interactive Web Server
Launch the local interactive reader:
```bash
python3 -m schrodinger.cli serve --port 8080
```
Open `http://localhost:8080` in any web browser to view the interactive stationary wavefunctions and harmonic oscillator distributions.

### Publication-Grade Document & PDF Export
Export directly to PDF (via headless Chrome) or standalone HTML:
```bash
# Export PDF
python3 -m schrodinger.cli export --out schrodinger_wave_mechanics.pdf

# Export standalone HTML
python3 -m schrodinger.cli export --out schrodinger_wave_mechanics.html
```

### Computing Energy Eigenvalues
Calculate discrete energy levels for a nanoscale potential box:
```bash
python3 -m schrodinger.cli well-spectrum --length 1.5 --states 6
```

---

## License

This software is released under the MIT License. Copyright (c) 2026 Jeong Hoon Kim.
