# Max Planck: The Quantum of Action & Blackbody Radiation

An interactive readable edition and numerical proof engine for Max Planck's December 1900 discovery of the quantum of action $h$, the resolution of the classical Ultraviolet Catastrophe, and the blackbody radiation law.

## Overview

This repository provides an interactive digital book and computational engine demonstrating:
1. **The Ultraviolet Catastrophe Resolution**: Exact spectral radiance $B_\lambda(\lambda, T)$ contrasting the classical Rayleigh-Jeans divergence with Planck's quantum formulation.
2. **Quanta of Action**: Discrete energy states $E = n h \nu$ of cavity resonators.
3. **Wien's Displacement Law**: Accurate computation of peak wavelength $\lambda_{\max} \cdot T = b$.
4. **Stefan-Boltzmann Exitance**: Numerical integration demonstrating convergence to $j^* = \sigma T^4$.
5. **Interactive Blackbody Spectrum Explorer**: Real-time evaluation of radiation parameters across thermal cavity temperatures.

## Installation

```bash
git clone https://gitlab.com/jk9576/PHYSICS.git
cd PHYSICS/Planck
pip install -e .
```

## Usage

### Run Unit Tests
```bash
python3 -W error -m unittest discover tests
```

### Serve Interactive Book Locally
```bash
python3 -m planck.cli serve --port 8080
```
Open `http://localhost:8080` in your web browser.

### Export to HTML or PDF
```bash
# Export standalone HTML
python3 -m planck.cli export --out Planck_Blackbody_Radiation.html

# Export publication-quality PDF via headless Chrome
python3 -m planck.cli export --out Planck_Blackbody_Radiation.pdf
```

### Radiance and Wien CLI Tools
```bash
# Calculate spectral radiance at solar surface temperature (5778 K) and green light (500 nm)
python3 -m planck.cli radiance --temp 5778.0 --wavelength 500e-9

# Calculate Wien peak wavelength and total Stefan-Boltzmann radiant exitance
python3 -m planck.cli wien --temp 5778.0
```

## License

MIT License - Copyright (c) 2026 Jeong Hoon Kim. See `LICENSE` for details.
