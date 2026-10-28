import unittest
from schrodinger.wave_mechanics import HBAR, M_ELECTRON, PotentialWellSolver, HarmonicOscillatorWavefunctions
from schrodinger.visualizer import SchrodingerVisualizer
from schrodinger.book import SchrodingerBookGenerator

class TestSchrodingerWaveMechanics(unittest.TestCase):
    def setUp(self):
        self.solver = PotentialWellSolver(length=1.0e-9)

    def test_energy_scaling(self):
        e1 = self.solver.energy_eigenvalue(1)
        e2 = self.solver.energy_eigenvalue(2)
        e3 = self.solver.energy_eigenvalue(3)
        self.assertAlmostEqual(e2 / e1, 4.0, places=5)
        self.assertAlmostEqual(e3 / e1, 9.0, places=5)

    def test_wavefunction_boundary_conditions(self):
        for n in [1, 2, 3]:
            self.assertAlmostEqual(self.solver.wavefunction(n, 0.0), 0.0)
            self.assertAlmostEqual(self.solver.wavefunction(n, 1.0e-9), 0.0)

    def test_orthonormality(self):
        # Self-normalization = 1.0
        norm1 = self.solver.integrate_overlap(1, 1)
        self.assertAlmostEqual(norm1, 1.0, places=3)
        # Orthogonality = 0.0
        overlap12 = self.solver.integrate_overlap(1, 2)
        self.assertAlmostEqual(overlap12, 0.0, places=3)

    def test_harmonic_oscillator(self):
        sho = HarmonicOscillatorWavefunctions(omega=1.0e15)
        e0 = sho.energy_level(0)
        e1 = sho.energy_level(1)
        self.assertAlmostEqual(e1 - e0, HBAR * 1.0e15, places=5)
        # Ground state maximum at origin x=0
        psi0_0 = sho.ground_state(0.0)
        psi0_1 = sho.ground_state(1.0e-10)
        self.assertGreater(psi0_0, psi0_1)

    def test_svg_rendering(self):
        vis = SchrodingerVisualizer()
        svg_well = vis.render_potential_well_svg()
        svg_harm = vis.render_harmonic_oscillator_svg()
        self.assertIn("<svg", svg_well)
        self.assertIn("Infinite Square Well", svg_well)
        self.assertIn("<svg", svg_harm)
        self.assertIn("Harmonic Oscillator", svg_harm)

    def test_book_generation(self):
        gen = SchrodingerBookGenerator()
        html_doc = gen.generate_html()
        self.assertIn("<!DOCTYPE html>", html_doc)
        self.assertIn("Erwin Schrödinger", html_doc)
        self.assertIn("katex", html_doc)

if __name__ == "__main__":
    unittest.main()
