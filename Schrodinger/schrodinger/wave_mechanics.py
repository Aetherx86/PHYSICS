import math
from dataclasses import dataclass
from typing import Callable, List, Tuple

HBAR = 1.054571817e-34    # Reduced Planck constant [J*s]
M_ELECTRON = 9.1093837e-31 # Electron mass [kg]

class PotentialWellSolver:
    """Analytical and numerical solver for 1D Infinite Potential Well (Particle in a Box)."""

    def __init__(self, length: float = 1.0e-9, mass: float = M_ELECTRON, hbar: float = HBAR):
        self.L = length
        self.m = mass
        self.hbar = hbar

    def energy_eigenvalue(self, n: int) -> float:
        """Computes quantized energy: E_n = (n^2 * pi^2 * hbar^2) / (2 * m * L^2) in Joules."""
        if n < 1:
            raise ValueError("Quantum number n must be a positive integer (n >= 1).")
        return (n ** 2) * (math.pi ** 2) * (self.hbar ** 2) / (2.0 * self.m * (self.L ** 2))

    def wavefunction(self, n: int, x: float) -> float:
        """Stationary spatial wavefunction: psi_n(x) = sqrt(2/L) * sin(n * pi * x / L)."""
        if x < 0.0 or x > self.L:
            return 0.0
        return math.sqrt(2.0 / self.L) * math.sin(n * math.pi * x / self.L)

    def probability_density(self, n: int, x: float) -> float:
        """Probability density P(x) = |psi_n(x)|^2."""
        val = self.wavefunction(n, x)
        return val * val

    def integrate_overlap(self, n1: int, n2: int, steps: int = 1000) -> float:
        """Calculates overlap integral int_0^L psi_n1(x) * psi_n2(x) dx via Simpson rule."""
        dx = self.L / steps
        total = 0.0
        for i in range(steps + 1):
            x = i * dx
            weight = 4.0 if i % 2 == 1 else 2.0
            if i == 0 or i == steps:
                weight = 1.0
            total += weight * self.wavefunction(n1, x) * self.wavefunction(n2, x)
        return (dx / 3.0) * total

class HarmonicOscillatorWavefunctions:
    """Wavefunctions and stationary energy levels for the 1D Quantum Harmonic Oscillator."""

    def __init__(self, omega: float = 1.0e15, mass: float = M_ELECTRON, hbar: float = HBAR):
        self.omega = omega
        self.m = mass
        self.hbar = hbar
        self.alpha = (self.m * self.omega / self.hbar) ** 0.5 # Characteristic inverse length [1/m]

    def energy_level(self, n: int) -> float:
        """Quantized energy level: E_n = (n + 1/2) * hbar * omega."""
        return (n + 0.5) * self.hbar * self.omega

    def ground_state(self, x: float) -> float:
        """Ground state wavefunction psi_0(x) = (alpha / sqrt(pi))^(1/2) * exp(-alpha^2 * x^2 / 2)."""
        norm = (self.alpha / math.sqrt(math.pi)) ** 0.5
        return norm * math.exp(-0.5 * (self.alpha * x) ** 2)

    def first_excited_state(self, x: float) -> float:
        """First excited state psi_1(x) = (alpha / sqrt(pi))^(1/2) * sqrt(2) * alpha * x * exp(-alpha^2 * x^2 / 2)."""
        norm = (self.alpha / math.sqrt(math.pi)) ** 0.5
        return norm * math.sqrt(2.0) * (self.alpha * x) * math.exp(-0.5 * (self.alpha * x) ** 2)
