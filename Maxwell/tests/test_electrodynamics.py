import unittest
from maxwell.electrodynamics import EPSILON_0, MU_0, C_EXACT, ElectrodynamicsEngine, MAXWELL_EQUATIONS
from maxwell.visualizer import MaxwellVisualizer
from maxwell.book import MaxwellBookGenerator

class TestMaxwellElectrodynamics(unittest.TestCase):
    def test_wave_speed_accuracy(self):
        c_calc = ElectrodynamicsEngine.calculate_wave_speed(EPSILON_0, MU_0)
        self.assertAlmostEqual(c_calc, C_EXACT, places=-2) # within 100 m/s

    def test_poynting_vector(self):
        flux = ElectrodynamicsEngine.poynting_vector_magnitude(e_amplitude=1.0)
        self.assertGreater(flux, 0.001)
        self.assertLess(flux, 0.002)

    def test_plane_wave_sampling(self):
        samples = ElectrodynamicsEngine.sample_plane_wave(wavelength=1.0, e0=2.0, num_points=20)
        self.assertEqual(len(samples), 21)
        # Verify first point
        z, ex, by, sz = samples[0]
        self.assertAlmostEqual(z, 0.0)
        self.assertAlmostEqual(ex, 2.0)
        self.assertGreater(sz, 0.0)

    def test_maxwell_equations_metadata(self):
        self.assertEqual(len(MAXWELL_EQUATIONS), 4)
        names = [eq.name for eq in MAXWELL_EQUATIONS]
        self.assertTrue(any("Gauss" in n for n in names))
        self.assertTrue(any("Faraday" in n for n in names))
        self.assertTrue(any("Ampère" in n or "Ampere" in n for n in names))

    def test_svg_generation(self):
        vis = MaxwellVisualizer()
        svg_wave = vis.render_em_wave_svg()
        svg_disp = vis.render_displacement_current_svg()
        self.assertIn("<svg", svg_wave)
        self.assertIn("Electric Field", svg_wave)
        self.assertIn("<svg", svg_disp)
        self.assertIn("Displacement Current", svg_disp)

    def test_book_generation(self):
        gen = MaxwellBookGenerator()
        html_doc = gen.generate_html()
        self.assertIn("<!DOCTYPE html>", html_doc)
        self.assertIn("James Clerk Maxwell", html_doc)
        self.assertIn("katex", html_doc)

if __name__ == "__main__":
    unittest.main()
