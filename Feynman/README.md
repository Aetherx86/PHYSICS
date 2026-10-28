# Richard Feynman: The Path Integral Formulation of Quantum Mechanics

An interactive readable edition and numerical proof engine for Richard Feynman's 1948 space-time path integral formulation of non-relativistic quantum mechanics.

## Overview

This repository provides an interactive digital book and computational engine demonstrating:
1. **The Quantum Propagator**: Discretization and evaluation of transition amplitudes $K(b, a) = \int \mathcal{D}[x(t)] \exp(i S[x]/\hbar)$.
2. **Principle of Least Action as Stationary Phase Limit**: How macroscopic classical trajectories ($\delta S = 0$) arise naturally from destructive interference of non-stationary quantum histories.
3. **Exact Free Particle Propagator**: Analytical closed-form evaluations matching path integral limits.
4. **Interactive Spacetime Exploration**: Dynamic parameter adjustment of variational path fluctuations and phase phasor sums.

## Installation

```bash
git clone https://gitlab.com/jk9576/PHYSICS.git
cd PHYSICS/Feynman
pip install -e .
```

## Usage

### Run Unit Tests
```bash
python3 -W error -m unittest discover tests
```

### Serve Interactive Book Locally
```bash
python3 -m feynman.cli serve --port 8080
```
Open `http://localhost:8080` in your web browser.

### Export to HTML or PDF
```bash
# Export standalone HTML
python3 -m feynman.cli export --out Feynman_Path_Integrals.html

# Export publication-quality PDF via headless Chrome
python3 -m feynman.cli export --out Feynman_Path_Integrals.pdf
```

### Action and Propagator CLI Tools
```bash
# Calculate classical action for an electron
python3 -m feynman.cli action --mass 9.1093837e-31 --xa 0.0 --xb 1.0e-9 --time 1.0e-15

# Calculate exact analytical propagator
python3 -m feynman.cli propagate --mass 9.1093837e-31 --xa 0.0 --xb 1.0e-9 --time 1.0e-15
```

## License

MIT License - Copyright (c) 2026 Jeong Hoon Kim. See `LICENSE` for details.
