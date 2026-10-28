# James Clerk Maxwell: Classical Electrodynamics & Wave Theory

Interactive Maxwell Field Equations Engine, Displacement Current Demonstrator, Electromagnetic Wave Propagation, and Poynting Vector Suite

## Theoretical Foundation

In 1865, James Clerk Maxwell published *A Dynamical Theory of the Electromagnetic Field*, achieving the historic unification of electricity, magnetism, and optics. Prior to Maxwell, Ampere's circuital law was incomplete and violated electric charge conservation in time-varying configurations, such as during the charging of a capacitor. By introducing the displacement current density:

$$\mathbf{J}_D = \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}$$

Maxwell achieved mathematical and physical consistency across all dynamic electromagnetic phenomena. Taking the curl of the curl of the electric field in charge-free space ($\rho = 0, \mathbf{J} = 0$):

$$\nabla \times (\nabla \times \mathbf{E}) = \nabla(\nabla \cdot \mathbf{E}) - \nabla^2 \mathbf{E} = -\mu_0 \varepsilon_0 \frac{\partial^2 \mathbf{E}}{\partial t^2}$$

which establishes the three-dimensional electromagnetic wave equation:

$$\nabla^2 \mathbf{E} - \frac{1}{c^2}\frac{\partial^2 \mathbf{E}}{\partial t^2} = 0, \quad c = \frac{1}{\sqrt{\mu_0 \varepsilon_0}} \approx 299{,}792{,}458\text{ m/s}$$

This discovery demonstrated that light itself is a transverse electromagnetic wave, opening the era of modern physics and wireless transmission.

---

## The Four Maxwell Equations

### 1. Gauss's Law for Electricity
$$\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0} \iff \oint_{\partial V} \mathbf{E} \cdot d\mathbf{A} = \frac{Q_{\text{encl}}}{\varepsilon_0}$$

### 2. Gauss's Law for Magnetism
$$\nabla \cdot \mathbf{B} = 0 \iff \oint_{\partial V} \mathbf{B} \cdot d\mathbf{A} = 0$$

### 3. Maxwell-Faraday Law of Induction
$$\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t} \iff \oint_{\partial \Sigma} \mathbf{E} \cdot d\mathbf{l} = -\frac{d}{dt}\iint_{\Sigma} \mathbf{B} \cdot d\mathbf{A}$$

### 4. Ampere-Maxwell Law with Displacement Current
$$\nabla \times \mathbf{B} = \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t} \iff \oint_{\partial \Sigma} \mathbf{B} \cdot d\mathbf{l} = \mu_0 I_{\text{encl}} + \mu_0 \varepsilon_0 \frac{d}{dt}\iint_{\Sigma} \mathbf{E} \cdot d\mathbf{A}$$

---

## Installation & Setup

Zero third-party dependencies required. Built exclusively with Python 3.9+ standard libraries.

```bash
git clone https://gitlab.com/jk9576/Maxwell.git
cd Maxwell
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
python3 -m maxwell.cli serve --port 8080
```
Open `http://localhost:8080` in any web browser to view the interactive 3D electromagnetic wave diagram and displacement current simulator.

### Publication-Grade Document & PDF Export
Export directly to PDF (via headless Chrome) or HTML:
```bash
# Export PDF
python3 -m maxwell.cli export --out maxwell_electrodynamics.pdf

# Export standalone HTML
python3 -m maxwell.cli export --out maxwell_electrodynamics.html
```

### Computing Light Speed from Vacuum Constants
Verify $c = 1 / \sqrt{\mu_0 \varepsilon_0}$ from first principles:
```bash
python3 -m maxwell.cli wave-speed
```

---

## License

This software is released under the MIT License. Copyright (c) 2026 Jeong Hoon Kim.
