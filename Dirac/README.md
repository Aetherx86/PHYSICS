# Paul Dirac: Relativistic Quantum Mechanics & Spinor Field Theory

Interactive Dirac Equation Solver, 4x4 Clifford Algebra Engine, Dirac Sea Demonstrator, and Antimatter Suite

## Theoretical Foundation

In 1928, Paul Adrien Maurice Dirac formulated the relativistic wave equation for the electron. Prior attempts based directly on the relativistic dispersion relation $E^2 - p^2 c^2 = m^2 c^4$, notably the Klein-Gordon equation:

$$\left(\frac{1}{c^2}\frac{\partial^2}{\partial t^2} - \nabla^2 + \frac{m^2 c^2}{\hbar^2}\right)\psi = 0$$

suffered from two fatal flaws: the existence of negative probability densities and the inability to incorporate intrinsic electron spin. Dirac discovered that factoring the relativistic energy-momentum invariant requires an equation strictly linear in space-time derivatives:

$$(i\hbar \gamma^\mu \partial_\mu - mc)\psi = 0 \iff i\hbar \frac{\partial \psi}{\partial t} = \left(c \boldsymbol{\alpha}\cdot\mathbf{p} + \beta mc^2\right)\psi$$

For this linear Hamiltonian to yield $E^2 = p^2 c^2 + m^2 c^4$, the coefficients $\gamma^\mu$ cannot be scalar numbers; they must be elements of a Clifford algebra satisfying the anti-commutation relations:

$$\{\gamma^\mu, \gamma^\nu\} \equiv \gamma^\mu \gamma^\nu + \gamma^\nu \gamma^\mu = 2 \eta^{\mu\nu} I_4, \quad \eta = \text{diag}(+1, -1, -1, -1)$$

The minimal matrix dimension that admits this algebra is $4 \times 4$. Consequently, the quantum state $\psi$ is a four-component complex bispinor. This four-component structure naturally yielded two profound discoveries:
1. The electron intrinsically possesses spin-$\frac{1}{2}$ and an anomalous gyromagnetic factor $g = 2$.
2. The spectrum admits negative energy states $E = -\sqrt{p^2 c^2 + m^2 c^4}$, which Dirac interpreted as an all-pervading vacuum sea; missing states ("holes") in this sea behave as positively charged anti-electrons, predicting the existence of antimatter (the positron).

---

## 4x4 Gamma Matrix Algebra (Dirac-Pauli Representation)

$$\gamma^0 = \begin{pmatrix} I_2 & 0 \\ 0 & -I_2 \end{pmatrix}, \quad \gamma^i = \begin{pmatrix} 0 & \sigma^i \\ -\sigma^i & 0 \end{pmatrix} \quad (i = 1, 2, 3)$$

where $\sigma^1, \sigma^2, \sigma^3$ are the Hermitian $2 \times 2$ Pauli spin matrices.

Conserved 4-Current:
$$j^\mu = c \bar{\psi}\gamma^\mu \psi, \quad \partial_\mu j^\mu = 0, \quad \rho = \frac{j^0}{c} = \psi^\dagger \psi \ge 0$$
which is strictly positive definite everywhere.

---

## Installation & Setup

Zero external dependencies required. Compatible with Python 3.9+.

```bash
git clone https://gitlab.com/jk9576/Dirac.git
cd Dirac
```

Run test suite:
```bash
python3 -m unittest discover tests -v
```

---

## Usage

### Interactive Web Server
Launch the interactive web reader:
```bash
python3 -m dirac.cli serve --port 8080
```
Open `http://localhost:8080` in any web browser to view the interactive Dirac Sea energy diagram and $4 \times 4$ Gamma matrix block-structure.

### Publication-Grade Document & PDF Export
Export directly to publication PDF (via headless Chrome) or standalone HTML:
```bash
# Export PDF
python3 -m dirac.cli export --out dirac_relativistic_qm.pdf

# Export standalone HTML
python3 -m dirac.cli export --out dirac_relativistic_qm.html
```

### Clifford Algebra Verification
Verify all 16 Clifford anti-commutation relations $\{\gamma^\mu, \gamma^\nu\} = 2\eta^{\mu\nu}I_4$:
```bash
python3 -m dirac.cli clifford
```

### Relativistic Dispersion Calculation
Calculate positive and negative energy eigenvalues for electron momentum states:
```bash
python3 -m dirac.cli dispersion --momentum 400000
```

---

## License

This software is released under the MIT License. Copyright (c) 2026 Jeong Hoon Kim.
