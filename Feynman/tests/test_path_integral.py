import unittest
import math
from feynman.path_integral import PathIntegralEngine, HBAR, M_ELECTRON
from feynman.book import FeynmanBookGenerator

class TestPathIntegral(unittest.TestCase):
    def test_classical_action_analytical(self):
        mass = 1.0
        x_a = 0.0
        x_b = 2.0
        t_total = 4.0
        # S_cl = m * (x_b - x_a)^2 / (2 * t_total) = 1.0 * 4 / (2 * 4) = 0.5
        action = PathIntegralEngine.classical_action_free_particle(mass, x_a, x_b, t_total)
        self.assertAlmostEqual(action, 0.5, places=6)

    def test_discretized_action_matches_analytical(self):
        mass = M_ELECTRON
        x_a = 0.0
        x_b = 1.0e-9
        t_total = 1.0e-15
        steps = 100
        times = [i * t_total / (steps - 1) for i in range(steps)]
        positions = [x_a + (x_b - x_a) * (t / t_total) for t in times]

        s_num = PathIntegralEngine.compute_path_action(times, positions, mass)
        s_exact = PathIntegralEngine.classical_action_free_particle(mass, x_a, x_b, t_total)

        self.assertAlmostEqual(s_num, s_exact, delta=s_exact * 1e-4)

    def test_stationary_least_action_principle(self):
        mass = M_ELECTRON
        x_a = 0.0
        x_b = 1.0e-9
        t_total = 1.0e-15
        steps = 200
        times = [i * t_total / (steps - 1) for i in range(steps)]

        # Classical path
        pos_cl = PathIntegralEngine.generate_variational_path(times, x_a, x_b, perturbation_amplitude=0.0)
        s_cl = PathIntegralEngine.compute_path_action(times, pos_cl, mass)

        # Variational paths with positive and negative deviations
        for amp in [-0.5e-9, -0.2e-9, 0.2e-9, 0.5e-9]:
            pos_var = PathIntegralEngine.generate_variational_path(times, x_a, x_b, perturbation_amplitude=amp)
            s_var = PathIntegralEngine.compute_path_action(times, pos_var, mass)
            # Action must be strictly greater than classical action
            self.assertGreater(s_var, s_cl)

    def test_analytical_propagator(self):
        mass = M_ELECTRON
        x_a = 0.0
        x_b = 1.0e-9
        t_total = 1.0e-15
        k_val = PathIntegralEngine.free_particle_propagator_analytical(mass, x_a, x_b, t_total)
        self.assertNotEqual(k_val, 0j)
        self.assertFalse(math.isnan(k_val.real))
        self.assertFalse(math.isnan(k_val.imag))

    def test_html_generator(self):
        gen = FeynmanBookGenerator()
        html = gen.generate_html()
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Richard Feynman", html)
        self.assertIn("renderMathInElement", html)
        self.assertIn("<svg", html)

if __name__ == "__main__":
    unittest.main()
