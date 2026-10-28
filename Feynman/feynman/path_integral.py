import math
import cmath
from typing import List, Tuple, Callable

# Fundamental Constants
HBAR = 1.054571817e-34  # Reduced Planck constant in J*s
M_ELECTRON = 9.1093837015e-31 # Electron rest mass in kg

class PathIntegralEngine:
    """
    Computes classical actions, path variations, and quantum path-integral propagators
    according to Richard Feynman's 1948 formulation:
        K(b, a) = \\int \\mathcal{D}[x(t)] \\exp(i S[x(t)] / \\hbar)
    """

    @staticmethod
    def classical_action_free_particle(mass: float, x_a: float, x_b: float, t_total: float) -> float:
        """
        Exact classical action for a free particle moving from (0, x_a) to (t_total, x_b):
        S_cl = m * (x_b - x_a)^2 / (2 * t_total)
        """
        if t_total <= 0:
            raise ValueError("Time duration must be positive.")
        return mass * ((x_b - x_a) ** 2) / (2.0 * t_total)

    @staticmethod
    def compute_path_action(
        times: List[float],
        positions: List[float],
        mass: float,
        potential_fn: Callable[[float], float] = lambda x: 0.0
    ) -> float:
        """
        Calculates action S = int (T - V) dt along a discretized trajectory x(t).
        S = sum_{j=0}^{N-2} Delta_t * [ 1/2 m ((x_{j+1}-x_j)/Delta_t)^2 - V((x_{j+1}+x_j)/2) ]
        """
        n = len(times)
        if n != len(positions) or n < 2:
            raise ValueError("Times and positions must have equal length >= 2.")

        total_action = 0.0
        for j in range(n - 1):
            dt = times[j + 1] - times[j]
            if dt <= 0:
                raise ValueError("Time coordinates must be strictly increasing.")
            v = (positions[j + 1] - positions[j]) / dt
            t_mid = (positions[j + 1] + positions[j]) / 2.0
            kinetic = 0.5 * mass * (v ** 2)
            potential = potential_fn(t_mid)
            total_action += (kinetic - potential) * dt

        return total_action

    @staticmethod
    def generate_variational_path(
        times: List[float],
        x_a: float,
        x_b: float,
        perturbation_amplitude: float,
        mode: int = 1
    ) -> List[float]:
        """
        Generates a perturbed path:
        x(t) = x_cl(t) + A * sin(n * pi * (t - t_0) / T)
        which preserves endpoints: x(0) = x_a and x(T) = x_b.
        """
        t_0 = times[0]
        t_end = times[-1]
        t_total = t_end - t_0
        positions = []
        for t in times:
            # Classical straight-line free trajectory
            tau = (t - t_0) / t_total
            x_cl = x_a + (x_b - x_a) * tau
            # Variation vanishing at boundaries
            delta_x = perturbation_amplitude * math.sin(mode * math.pi * tau)
            positions.append(x_cl + delta_x)
        return positions

    @staticmethod
    def path_phase(action: float, hbar_effective: float = HBAR) -> complex:
        """
        Computes the quantum phase factor exp(i * S / hbar).
        """
        phase_angle = action / hbar_effective
        return cmath.exp(1j * phase_angle)

    @staticmethod
    def free_particle_propagator_analytical(
        mass: float,
        x_a: float,
        x_b: float,
        t_total: float,
        hbar: float = HBAR
    ) -> complex:
        """
        Exact Feynman propagator for a free particle in 1D:
        K(x_b, T; x_a, 0) = sqrt(m / (2 * pi * i * hbar * T)) * exp(i * m * (x_b - x_a)^2 / (2 * hbar * T))
        """
        action = mass * ((x_b - x_a) ** 2) / (2.0 * t_total)
        prefactor = cmath.sqrt(mass / (2.0 * math.pi * 1j * hbar * t_total))
        return prefactor * cmath.exp(1j * action / hbar)
