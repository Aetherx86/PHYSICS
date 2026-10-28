import unittest
import math
from planck.blackbody import (
    PlanckBlackbodyEngine,
    B_WIEN,
    SIGMA_SB
)
from planck.book import PlanckBookGenerator

class TestPlanckBlackbody(unittest.TestCase):
    def test_wien_peak_maximum(self):
        t = 5000.0
        lam_peak = PlanckBlackbodyEngine.wien_peak_wavelength(t)
        b_peak = PlanckBlackbodyEngine.planck_spectral_radiance(lam_peak, t)

        # Perturb wavelength slightly to left and right
        b_left = PlanckBlackbodyEngine.planck_spectral_radiance(lam_peak * 0.98, t)
        b_right = PlanckBlackbodyEngine.planck_spectral_radiance(lam_peak * 1.02, t)

        # Must be a strict local maximum
        self.assertGreater(b_peak, b_left)
        self.assertGreater(b_peak, b_right)

    def test_rayleigh_jeans_long_wavelength_asymptote(self):
        t = 3000.0
        # For very long radio wavelengths (e.g. 10 cm = 0.1 m), Planck matches Rayleigh-Jeans
        lam_long = 0.1
        b_planck = PlanckBlackbodyEngine.planck_spectral_radiance(lam_long, t)
        b_rj = PlanckBlackbodyEngine.rayleigh_jeans_radiance(lam_long, t)

        ratio = b_planck / b_rj
        self.assertAlmostEqual(ratio, 1.0, places=4)

    def test_stefan_boltzmann_exitance(self):
        t = 1000.0
        expected = SIGMA_SB * (t ** 4)
        j_star = PlanckBlackbodyEngine.stefan_boltzmann_exitance(t)
        self.assertAlmostEqual(j_star, expected, places=7)

    def test_stefan_boltzmann_integral(self):
        t = 1500.0
        # Integrate pi * B_lambda d_lambda over wide spectrum
        integral_radiance = PlanckBlackbodyEngine.integrate_planck_radiance(
            temperature_k=t,
            lambda_min=1e-8,
            lambda_max=1e-4,
            steps=5000
        )
        integral_exitance = math.pi * integral_radiance
        expected_exitance = SIGMA_SB * (t ** 4)

        # Within numerical integration discretization margin (~1%)
        self.assertAlmostEqual(integral_exitance, expected_exitance, delta=expected_exitance * 0.02)

    def test_html_generator(self):
        gen = PlanckBookGenerator()
        html = gen.generate_html()
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Max Planck", html)
        self.assertIn("renderMathInElement", html)
        self.assertIn("<svg", html)

if __name__ == "__main__":
    unittest.main()
