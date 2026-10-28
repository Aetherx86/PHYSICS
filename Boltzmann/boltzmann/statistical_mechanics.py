import math
from typing import Tuple, List, Dict

# Fundamental Physical Constants
K_B = 1.380649e-23        # Boltzmann constant in J / K
N_A = 6.02214076e23       # Avogadro constant in mol^-1
M_N2 = 0.0280134 / N_A    # Nitrogen molecule N2 mass in kg (~4.6517e-26 kg)

class BoltzmannStatisticalEngine:
    """
    Implements Ludwig Boltzmann's statistical mechanics formulations:
    - Boltzmann entropy equation: S = k_B * ln(Omega)
    - Maxwell-Boltzmann speed distribution f(v)
    - Characteristic statistical speeds (v_p, v_mean, v_rms)
    - Kinetic energy equipartition
    """

    @staticmethod
    def entropy(microstates: float) -> float:
        """
        Boltzmann's entropy equation carved on his gravestone in Vienna:
        S = k_B * ln(Omega)
        """
        if microstates <= 0:
            raise ValueError("Microstates Omega must be strictly positive.")
        return K_B * math.log(microstates)

    @staticmethod
    def characteristic_speeds(temperature_k: float, mass_kg: float) -> Dict[str, float]:
        """
        Calculates characteristic molecular speeds:
        v_p   = sqrt(2 * k_B * T / m)
        v_avg = sqrt(8 * k_B * T / (pi * m))
        v_rms = sqrt(3 * k_B * T / m)
        """
        if temperature_k <= 0 or mass_kg <= 0:
            raise ValueError("Temperature and particle mass must be strictly positive.")

        v_p = math.sqrt(2.0 * K_B * temperature_k / mass_kg)
        v_avg = math.sqrt(8.0 * K_B * temperature_k / (math.pi * mass_kg))
        v_rms = math.sqrt(3.0 * K_B * temperature_k / mass_kg)
        return {
            "v_probable": v_p,
            "v_mean": v_avg,
            "v_rms": v_rms
        }

    @staticmethod
    def maxwell_boltzmann_pdf(v: float, temperature_k: float, mass_kg: float) -> float:
        """
        Probability density function of molecular speed v:
        f(v) = 4 * pi * (m / (2 * pi * k_B * T))^(3/2) * v^2 * exp(- m * v^2 / (2 * k_B * T))
        """
        if v < 0:
            return 0.0
        if temperature_k <= 0 or mass_kg <= 0:
            raise ValueError("Temperature and particle mass must be strictly positive.")

        a = mass_kg / (2.0 * K_B * temperature_k)
        prefactor = 4.0 * math.pi * (a / math.pi) ** 1.5
        return prefactor * (v ** 2) * math.exp(-a * (v ** 2))

    @staticmethod
    def integrate_distribution(
        v_max: float,
        temperature_k: float,
        mass_kg: float,
        steps: int = 2000
    ) -> float:
        """
        Numerically integrates f(v) dv from 0 to v_max using trapezoidal rule.
        For large v_max, this converges to 1.0 (normalization).
        """
        dv = v_max / steps
        total = 0.5 * (BoltzmannStatisticalEngine.maxwell_boltzmann_pdf(0.0, temperature_k, mass_kg) +
                       BoltzmannStatisticalEngine.maxwell_boltzmann_pdf(v_max, temperature_k, mass_kg))

        for i in range(1, steps):
            v = i * dv
            total += BoltzmannStatisticalEngine.maxwell_boltzmann_pdf(v, temperature_k, mass_kg)

        return total * dv

    @staticmethod
    def mean_kinetic_energy(temperature_k: float) -> float:
        """
        Average translational kinetic energy per particle from equipartition:
        <E_k> = 3/2 * k_B * T
        """
        if temperature_k < 0:
            raise ValueError("Absolute temperature cannot be negative.")
        return 1.5 * K_B * temperature_k
