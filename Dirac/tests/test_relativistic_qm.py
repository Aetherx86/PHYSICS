import unittest
from dirac.relativistic_qm import (
    E_REST_ELECTRON_EV,
    Matrix4x4,
    get_dirac_gamma_matrices,
    RelativisticDiracEngine,
)
from dirac.visualizer import DiracVisualizer
from dirac.book import DiracBookGenerator

class TestDiracRelativisticQM(unittest.TestCase):
    def test_gamma_matrix_traces(self):
        gammas = get_dirac_gamma_matrices()
        self.assertEqual(len(gammas), 4)
        for idx, g in enumerate(gammas):
            self.assertAlmostEqual(g.trace(), 0.0 + 0.0j, msg=f"gamma^{idx} trace must be 0")

    def test_clifford_anticommutation(self):
        results = RelativisticDiracEngine.verify_clifford_algebra()
        self.assertEqual(len(results), 16)
        for mu, nu, ok in results:
            self.assertTrue(ok, msg=f"Clifford relation failed for mu={mu}, nu={nu}")

    def test_relativistic_dispersion(self):
        # At p=0, E = +/- mc^2 = +/- 511 keV
        ep0, em0 = RelativisticDiracEngine.dispersion_energy(0.0)
        self.assertAlmostEqual(ep0, E_REST_ELECTRON_EV, places=2)
        self.assertAlmostEqual(em0, -E_REST_ELECTRON_EV, places=2)

        # At p=300 keV, E = sqrt(300^2 + 511^2) ~ 592.5 keV
        ep, em = RelativisticDiracEngine.dispersion_energy(300000.0)
        self.assertGreater(ep, 590000.0)
        self.assertLess(ep, 595000.0)
        self.assertEqual(ep, -em)

    def test_svg_rendering(self):
        vis = DiracVisualizer()
        svg_sea = vis.render_dirac_sea_svg()
        svg_gamma = vis.render_gamma_matrices_svg()
        self.assertIn("<svg", svg_sea)
        self.assertIn("Dirac Sea", svg_sea)
        self.assertIn("<svg", svg_gamma)
        self.assertIn("Gamma Matrices", svg_gamma)

    def test_book_generation(self):
        gen = DiracBookGenerator()
        html_doc = gen.generate_html()
        self.assertIn("<!DOCTYPE html>", html_doc)
        self.assertIn("Paul Dirac", html_doc)
        self.assertIn("katex", html_doc)

if __name__ == "__main__":
    unittest.main()
