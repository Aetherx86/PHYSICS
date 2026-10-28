import math
from typing import Dict, Tuple

# Fundamental Physical Constants (CODATA 2018 / SI Exact)
H_PLANCK = 6.62607015e-34       # Planck constant in J * s
C_LIGHT = 299792458.0           # Speed of light in vacuum in m / s
K_BOLTZMANN = 1.380649e-23      # Boltzmann constant in J / K
B_WIEN = 2.897771955e-3         # Wien displacement law constant in m * K
SIGMA_SB = (2.0 * (math.pi ** 5) * (K_BOLTZMANN ** 4)) / (15.0 * (C_LIGHT ** 2) * (H_PLANCK ** 3)) # Stefan-Boltzmann constant ~5.670374e-8 W/(m^2*K^4)

class PlanckBlackbodyEngine:
    """
    Implements Max Planck's quantum theory of blackbody radiation (1900):
    - Planck spectral radiance B_lambda(lambda, T)
    - Rayleigh-Jeans classical approximation (UV Catastrophe)
    - Wien's displacement law lambda_max * T = b
    - Stefan-Boltzmann total integrated radiance and radiant exitance j* = sigma * T^4
    """

    @staticmethod
    def planck_spectral_radiance(wavelength_m: float, temperature_k: float) -> float:
        """
        Planck's spectral radiance per unit wavelength:
        B_lambda(lambda, T) = (2 * h * c^2 / lambda^5) / (exp(h * c / (lambda * k_B * T)) - 1)
        Units: W / (m^3 * sr)
        """
        if wavelength_m <= 0 or temperature_k <= 0:
            raise ValueError("Wavelength and temperature must be strictly positive.")

        exponent = (H_PLANCK * C_LIGHT) / (wavelength_m * K_BOLTZMANN * temperature_k)
        if exponent > 700.0:
            # Avoid overflow in exp(x) for tiny wavelengths
            return 0.0

        c1 = 2.0 * H_PLANCK * (C_LIGHT ** 2)
        denom = math.expm1(exponent) # exp(x) - 1 with high precision
        if denom <= 0:
            return 0.0

        return c1 / ((wavelength_m ** 5) * denom)

    @staticmethod
    def rayleigh_jeans_radiance(wavelength_m: float, temperature_k: float) -> float:
        """
        Classical Rayleigh-Jeans formula without quantization:
        B_RJ(lambda, T) = (2 * c * k_B * T) / lambda^4
        Diverges as lambda -> 0 (Ultraviolet Catastrophe).
        """
        if wavelength_m <= 0 or temperature_k <= 0:
            raise ValueError("Wavelength and temperature must be strictly positive.")

        return (2.0 * C_LIGHT * K_BOLTZMANN * temperature_k) / (wavelength_m ** 4)

    @staticmethod
    def wien_peak_wavelength(temperature_k: float) -> float:
        """
        Wien's displacement law:
        lambda_max = b / T
        """
        if temperature_k <= 0:
            raise ValueError("Temperature must be strictly positive.")
        return B_WIEN / temperature_k

    @staticmethod
    def stefan_boltzmann_exitance(temperature_k: float) -> float:
        """
        Stefan-Boltzmann law for total radiant energy exitance:
        j* = sigma * T^4
        Units: W / m^2
        """
        if temperature_k < 0:
            raise ValueError("Absolute temperature cannot be negative.")
        return SIGMA_SB * (temperature_k ** 4)

    @staticmethod
    def integrate_planck_radiance(
        temperature_k: float,
        lambda_min: float = 1.0e-9,
        lambda_max: float = 5.0e-5,
        steps: int = 5000
    ) -> float:
        """
        Numerically integrates B_lambda d_lambda from lambda_min to lambda_max.
        Should converge to (sigma / pi) * T^4.
        """
        d_lambda = (lambda_max - lambda_min) / steps
        total = 0.5 * (PlanckBlackbodyEngine.planck_spectral_radiance(lambda_min, temperature_k) +
                       PlanckBlackbodyEngine.planck_spectral_radiance(lambda_max, temperature_k))

        for i in range(1, steps):
            lam = lambda_min + i * d_lambda
            total += PlanckBlackbodyEngine.planck_spectral_radiance(lam, temperature_k)

        return total * d_lambda
