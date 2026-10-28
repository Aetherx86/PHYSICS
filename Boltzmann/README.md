# Ludwig Boltzmann: Statistical Mechanics and Entropy

An interactive readable edition and numerical proof engine for Ludwig Boltzmann's 1877 foundation of statistical mechanics, the entropy equation $S = k_B \ln \Omega$, and the Maxwell-Boltzmann molecular velocity distribution.

## Overview

This repository provides an interactive digital book and computational engine demonstrating:
1. **The Statistical Nature of Entropy**: Ludwig Boltzmann's fundamental relation between microscopic multiplicity $\Omega$ and macroscopic thermodynamic entropy $S = k_B \ln \Omega$.
2. **Maxwell-Boltzmann Speed Distribution**: Exact probability density function $f(v)$ derived by entropy maximization under energy and particle constraints.
3. **Characteristic Statistical Speeds**: Mathematical proof and calculation of the speed hierarchy $v_p < \langle v \rangle < v_{\text{rms}}$.
4. **Energy Equipartition**: Verification of translational kinetic energy $\langle E_k \rangle = \frac{3}{2} k_B T$.
5. **Interactive Thermal Velocity Explorer**: Real-time evaluation of speed distributions and thermal energies across molecular gas species and temperatures.

## Installation

```bash
git clone https://gitlab.com/jk9576/Boltzmann.git
cd Boltzmann
pip install -e .
```

## Usage

### Run Unit Tests
```bash
python3 -W error -m unittest discover tests
```

### Serve Interactive Book Locally
```bash
python3 -m boltzmann.cli serve --port 8080
```
Open `http://localhost:8080` in your web browser.

### Export to HTML or PDF
```bash
# Export standalone HTML
python3 -m boltzmann.cli export --out Boltzmann_Statistical_Mechanics.html

# Export publication-quality PDF via headless Chrome
python3 -m boltzmann.cli export --out Boltzmann_Statistical_Mechanics.pdf
```

### Speeds and Entropy CLI Tools
```bash
# Calculate characteristic molecular speeds at room temperature (300 K)
python3 -m boltzmann.cli speeds --temp 300.0

# Calculate Boltzmann entropy for 10^20 microstates
python3 -m boltzmann.cli entropy --omega 1.0e20
```

## License

MIT License - Copyright (c) 2026 Jeong Hoon Kim. See `LICENSE` for details.
