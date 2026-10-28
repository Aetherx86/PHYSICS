import unittest
import math
from boltzmann.statistical_mechanics import BoltzmannStatisticalEngine, K_B, M_N2
from boltzmann.book import BoltzmannBookGenerator

class TestBoltzmannStatisticalMechanics(unittest.TestCase):
    def test_entropy_calculation(self):
        omega = 1.0e20
        expected = K_B * math.log(omega)
        s_val = BoltzmannStatisticalEngine.entropy(omega)
        self.assertAlmostEqual(s_val, expected, places=15)

    def test_characteristic_speeds_ratios(self):
        t = 300.0
        m = M_N2
        speeds = BoltzmannStatisticalEngine.characteristic_speeds(t, m)
        vp = speeds["v_probable"]
        vavg = speeds["v_mean"]
        vrms = speeds["v_rms"]

        # Ratios must strictly satisfy:
        # vavg / vp == sqrt(4 / pi)
        # vrms / vp == sqrt(1.5)
        self.assertAlmostEqual(vavg / vp, math.sqrt(4.0 / math.pi), places=6)
        self.assertAlmostEqual(vrms / vp, math.sqrt(1.5), places=6)
        self.assertLess(vp, vavg)
        self.assertLess(vavg, vrms)

    def test_distribution_normalization(self):
        t = 300.0
        m = M_N2
        # For N2 at 300 K, v_rms ~ 516 m/s, so integrating up to 2500 m/s captures > 99.999%
        integral = BoltzmannStatisticalEngine.integrate_distribution(
            v_max=2500.0,
            temperature_k=t,
            mass_kg=m,
            steps=3000
        )
        self.assertAlmostEqual(integral, 1.0, places=3)

    def test_equipartition_kinetic_energy(self):
        t = 300.0
        e_kin = BoltzmannStatisticalEngine.mean_kinetic_energy(t)
        self.assertAlmostEqual(e_kin, 1.5 * K_B * t, places=15)

    def test_html_generator(self):
        gen = BoltzmannBookGenerator()
        html = gen.generate_html()
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Ludwig Boltzmann", html)
        self.assertIn("renderMathInElement", html)
        self.assertIn("<svg", html)

if __name__ == "__main__":
    unittest.main()
