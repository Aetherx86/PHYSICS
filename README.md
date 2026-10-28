# PHYSICS: Unified Foundational Physics & Quantum Theory Suite

A unified monorepo bringing together the monumental discoveries of physics giants—Newton, Maxwell, Boltzmann, Planck, Einstein, Schrodinger, Heisenberg, Dirac, and Feynman.

Every sub-repository contains an interactive readable digital edition, rigorous formal mathematical/physical engines, vector visualizations, unit test suites, and publication-ready PDF exports.

## Repository Directory

| Sub-Repository | Physical Scope & Key Formulations | Standalone Repository |
| :--- | :--- | :--- |
| **`Newton/`** | Classical mechanics, universal gravitation, orbital dynamics | [gitlab.com/jk9576/Newton](https://gitlab.com/jk9576/Newton) |
| **`Maxwell/`** | Classical electrodynamics, displacement current, electromagnetic waves ($c = 1/\sqrt{\mu_0 \varepsilon_0}$) | [gitlab.com/jk9576/Maxwell](https://gitlab.com/jk9576/Maxwell) |
| **`Boltzmann/`** | Statistical mechanics, entropy ($S = k_B \ln \Omega$), Maxwell-Boltzmann velocity distribution | [gitlab.com/jk9576/Boltzmann](https://gitlab.com/jk9576/Boltzmann) |
| **`Planck/`** | Quantum of action, blackbody spectral radiance, Ultraviolet Catastrophe resolution ($E = nh\nu$) | [gitlab.com/jk9576/Planck](https://gitlab.com/jk9576/Planck) |
| **`Einstein/`** | Special and General Relativity, Lorentz invariance, mass-energy equivalence ($E = mc^2$), spacetime geodesics | [gitlab.com/jk9576/Einstein](https://gitlab.com/jk9576/Einstein) |
| **`Schrodinger/`** | Wave mechanics, time-dependent and time-independent wave equations, bound state quantization | [gitlab.com/jk9576/Schrodinger](https://gitlab.com/jk9576/Schrodinger) |
| **`Heisenberg/`** | Matrix mechanics, non-commutative operator algebra, canonical commutation $[X, P] = i\hbar$, uncertainty principle | [gitlab.com/jk9576/Heisenberg](https://gitlab.com/jk9576/Heisenberg) |
| **`Dirac/`** | Relativistic quantum mechanics, Dirac equation, Clifford algebra Gamma matrices, antimatter prediction | [gitlab.com/jk9576/Dirac](https://gitlab.com/jk9576/Dirac) |
| **`Feynman/`** | Space-time path integrals, sum over histories ($K = \int \mathcal{D}[x] e^{iS/\hbar}$), principle of least action | [gitlab.com/jk9576/Feynman](https://gitlab.com/jk9576/Feynman) |

## Quick Start & Verification

### Running All Unit Test Suites

Each sub-repository can be tested independently:

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

### Exporting Interactive Books to HTML and PDF

Each interactive edition can be served locally or exported directly:

```bash
# Serve Maxwell Electrodynamics
python3 -m Maxwell.maxwell.cli serve --port 8080

# Export Dirac Relativistic Quantum Mechanics to PDF
python3 -m Dirac.dirac.cli export --out Dirac_Equation.pdf

# Export Feynman Path Integrals to PDF
python3 -m Feynman.feynman.cli export --out Feynman_Path_Integrals.pdf
```

## Structure & Architecture

```
PHYSICS/
├── LICENSE
├── README.md
├── Newton/
│   ├── newton/
│   └── tests/
├── Maxwell/
│   ├── maxwell/
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
