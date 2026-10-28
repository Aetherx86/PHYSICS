# PHYSICS: Unified Foundational Physics & Quantum Theory Suite

A unified monorepo bringing together the monumental discoveries of physics giants—Newton, Maxwell, Boltzmann, Planck, Einstein, Schrodinger, Heisenberg, Dirac, and Feynman.

Every sub-directory contains an interactive readable digital edition, rigorous formal mathematical/physical engines, vector visualizations, unit test suites, and publication-ready PDF exports.

## Repository Directory

| Sub-Directory | Physical Scope & Key Formulations | Interactive Book & Proof CLI | Key Test Suite |
| :--- | :--- | :--- | :--- |
| **[`Newton/`](./Newton)** | Classical mechanics, universal gravitation ($F = G \frac{m_1 m_2}{r^2}$), orbital dynamics | `python3 -m Newton.newton.cli serve` | `tests/test_mechanics.py` |
| **[`Maxwell/`](./Maxwell)** | Classical electrodynamics, displacement current, electromagnetic waves ($c = 1/\sqrt{\mu_0 \varepsilon_0}$) | `python3 -m Maxwell.maxwell.cli serve` | `tests/test_electrodynamics.py` |
| **[`Boltzmann/`](./Boltzmann)** | Statistical mechanics, entropy ($S = k_B \ln \Omega$), Maxwell-Boltzmann velocity distribution | `python3 -m Boltzmann.boltzmann.cli serve` | `tests/test_statistical_mechanics.py` |
| **[`Planck/`](./Planck)** | Quantum of action, blackbody spectral radiance, Ultraviolet Catastrophe resolution ($E = nh\nu$) | `python3 -m Planck.planck.cli serve` | `tests/test_blackbody.py` |
| **[`Einstein/`](./Einstein)** | Special and General Relativity, Lorentz invariance, mass-energy equivalence ($E = mc^2$), spacetime geodesics | `python3 -m Einstein.einstein.cli serve` | `tests/test_relativity.py` |
| **[`Schrodinger/`](./Schrodinger)** | Wave mechanics, time-dependent and time-independent wave equations, bound state quantization | `python3 -m Schrodinger.schrodinger.cli serve` | `tests/test_wave_mechanics.py` |
| **[`Heisenberg/`](./Heisenberg)** | Matrix mechanics, non-commutative operator algebra, canonical commutation $[X, P] = i\hbar$, uncertainty principle | `python3 -m Heisenberg.heisenberg.cli serve` | `tests/test_matrix_mechanics.py` |
| **[`Dirac/`](./Dirac)** | Relativistic quantum mechanics, Dirac equation, Clifford algebra Gamma matrices, antimatter prediction | `python3 -m Dirac.dirac.cli serve` | `tests/test_relativistic_qm.py` |
| **[`Feynman/`](./Feynman)** | Space-time path integrals, sum over histories ($K = \int \mathcal{D}[x] e^{iS/\hbar}$), principle of least action | `python3 -m Feynman.feynman.cli serve` | `tests/test_path_integral.py` |

## Quick Start & Verification

### Cloning the Repository

```bash
git clone https://gitlab.com/jk9576/PHYSICS.git
cd PHYSICS
```

### Running All Unit Test Suites

Each physical engine and proof module can be tested directly:

```bash
# Newton
cd Newton && python3 -W error -m unittest discover tests && cd ..

# Maxwell
cd Maxwell && python3 -W error -m unittest discover tests && cd ..

# Boltzmann
cd Boltzmann && python3 -W error -m unittest discover tests && cd ..

# Planck
cd Planck && python3 -W error -m unittest discover tests && cd ..

# Einstein
cd Einstein && python3 -W error -m unittest discover tests && cd ..

# Schrodinger
cd Schrodinger && python3 -W error -m unittest discover tests && cd ..

# Heisenberg
cd Heisenberg && python3 -W error -m unittest discover tests && cd ..

# Dirac
cd Dirac && python3 -W error -m unittest discover tests && cd ..

# Feynman
cd Feynman && python3 -W error -m unittest discover tests && cd ..
```

### Launching Interactive Books Locally

Each interactive digital edition features embedded KaTeX rendering, responsive vector graphics, and live parameter sliders:

```bash
# Newton's Principia
python3 -m Newton.newton.cli serve --port 8080

# Maxwell's Electrodynamics
python3 -m Maxwell.maxwell.cli serve --port 8081

# Boltzmann's Statistical Mechanics
python3 -m Boltzmann.boltzmann.cli serve --port 8082

# Planck's Blackbody Radiation
python3 -m Planck.planck.cli serve --port 8083

# Einstein's Relativity
python3 -m Einstein.einstein.cli serve --port 8084

# Schrodinger's Wave Mechanics
python3 -m Schrodinger.schrodinger.cli serve --port 8085

# Heisenberg's Matrix Mechanics
python3 -m Heisenberg.heisenberg.cli serve --port 8086

# Dirac's Relativistic Quantum Mechanics
python3 -m Dirac.dirac.cli serve --port 8087

# Feynman's Path Integrals
python3 -m Feynman.feynman.cli serve --port 8088
```

### Exporting Standalone Books (HTML & PDF)

```bash
# Export Maxwell Electrodynamics to publication PDF
python3 -m Maxwell.maxwell.cli export --out Maxwell_Electrodynamics.pdf

# Export Dirac Relativistic Quantum Mechanics to publication PDF
python3 -m Dirac.dirac.cli export --out Dirac_Equation.pdf

# Export Feynman Path Integrals to publication PDF
python3 -m Feynman.feynman.cli export --out Feynman_Path_Integrals.pdf

# Export Planck Blackbody Radiation to publication PDF
python3 -m Planck.planck.cli export --out Planck_Blackbody_Radiation.pdf
```

## Structure & Architecture

```
PHYSICS/
├── LICENSE
├── README.md
├── Newton/
│   ├── newton/
│   │   ├── mechanics.py
│   │   ├── propositions.py
│   │   ├── visualizer.py
│   │   ├── book.py
│   │   └── cli.py
│   └── tests/
├── Maxwell/
│   ├── maxwell/
│   │   ├── electrodynamics.py
│   │   ├── visualizer.py
│   │   ├── book.py
│   │   └── cli.py
│   └── tests/
├── Boltzmann/
│   ├── boltzmann/
│   └── tests/
├── Planck/
│   ├── planck/
│   └── tests/
├── Einstein/
│   ├── einstein/
│   └── tests/
├── Schrodinger/
│   ├── schrodinger/
│   └── tests/
├── Heisenberg/
│   ├── heisenberg/
│   └── tests/
├── Dirac/
│   ├── dirac/
│   └── tests/
└── Feynman/
    ├── feynman/
    └── tests/
```

## License

MIT License - Copyright (c) 2026 Jeong Hoon Kim. See `LICENSE` for details.
