import math
from typing import List
from .wave_mechanics import PotentialWellSolver

class SchrodingerVisualizer:
    """Renders vector diagrams of quantum wavefunctions and probability distributions in SVG."""
    def __init__(self, width: int = 650, height: int = 400):
        self.width = width
        self.height = height

    def render_potential_well_svg(self) -> str:
        """
        Renders the infinite square potential well with stationary wavefunctions
        psi_1(x), psi_2(x), psi_3(x) offset at their corresponding energy levels E_n.
        """
        x_left = 110.0
        x_right = 530.0
        well_width = x_right - x_left
        y_bottom = 350.0

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="100%" height="{self.height}">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1"/>',
            '<text x="20" y="30" font-family="sans-serif" font-weight="bold" font-size="15" fill="#0f172a">Infinite Square Well: Stationary Wavefunctions &psi;&#8345;(x)</text>',
            '<text x="20" y="50" font-family="sans-serif" font-size="12" fill="#64748b">Quantized energies E_n &prop; n&#178; with boundary conditions &psi;(0) = &psi;(L) = 0</text>',
            # Infinite potential barriers (shaded hatching)
            f'<rect x="20" y="70" width="{x_left - 20}" height="{y_bottom - 70}" fill="#f1f5f9" stroke="#94a3b8" stroke-dasharray="4,4"/>',
            f'<text x="35" y="210" font-family="sans-serif" font-weight="bold" font-size="14" fill="#64748b">V = &infin;</text>',
            f'<rect x="{x_right}" y="70" width="{self.width - 20 - x_right}" height="{y_bottom - 70}" fill="#f1f5f9" stroke="#94a3b8" stroke-dasharray="4,4"/>',
            f'<text x="{x_right + 25}" y="210" font-family="sans-serif" font-weight="bold" font-size="14" fill="#64748b">V = &infin;</text>',
            # Well boundary lines
            f'<line x1="{x_left}" y1="70" x2="{x_left}" y2="{y_bottom}" stroke="#0f172a" stroke-width="3"/>',
            f'<line x1="{x_right}" y1="70" x2="{x_right}" y2="{y_bottom}" stroke="#0f172a" stroke-width="3"/>',
            f'<line x1="{x_left}" y1="{y_bottom}" x2="{x_right}" y2="{y_bottom}" stroke="#0f172a" stroke-width="3"/>',
            f'<text x="{x_left - 5}" y="{y_bottom + 20}" font-family="serif" font-weight="bold" font-size="13">x = 0</text>',
            f'<text x="{x_right - 5}" y="{y_bottom + 20}" font-family="serif" font-weight="bold" font-size="13">x = L</text>',
        ]

        # Wavefunction levels: n=1, n=2, n=3
        levels = [
            (1, y_bottom - 60, "#2563eb", 28.0),
            (2, y_bottom - 150, "#16a34a", 28.0),
            (3, y_bottom - 240, "#dc2626", 28.0),
        ]

        steps = 50
        for n, base_y, color, amplitude in levels:
            # Baseline dashed line
            svg.append(f'<line x1="{x_left}" y1="{base_y}" x2="{x_right}" y2="{base_y}" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="3,3"/>')
            svg.append(f'<text x="{x_left + 10}" y="{base_y - 8}" font-family="sans-serif" font-weight="bold" font-size="12" fill="{color}">n = {n} (E_{n} = {n*n} E&#8321;)</text>')

            pts = []
            for s in range(steps + 1):
                frac = s / steps
                x = x_left + frac * well_width
                psi = math.sin(n * math.pi * frac) * amplitude
                y = base_y - psi
                pts.append(f"{x:.1f},{y:.1f}")

            svg.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2.2"/>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_harmonic_oscillator_svg(self) -> str:
        """Renders the parabolic potential V(x) = 1/2 m omega^2 x^2 with ground and first excited states."""
        cx = 325.0
        cy_base = 340.0
        k_scale = 0.0035

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="100%" height="{self.height}">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1"/>',
            '<text x="20" y="30" font-family="sans-serif" font-weight="bold" font-size="15" fill="#0f172a">Quantum Harmonic Oscillator: Parabolic Potential &amp; States</text>',
            '<text x="20" y="50" font-family="sans-serif" font-size="12" fill="#64748b">V(x) = &frac12; m &omega;&#178; x&#178; with non-zero vacuum zero-point energy E&#8320; = &frac12; &#8463;&omega;</text>',
        ]

        # Parabola points
        para_pts = []
        for x_step in range(-190, 191, 5):
            x = cx + x_step
            v = cy_base - (k_scale * (x_step ** 2))
            para_pts.append(f"{x:.1f},{v:.1f}")

        svg.append(f'<polyline points="{" ".join(para_pts)}" fill="none" stroke="#475569" stroke-width="2.5"/>')

        # Energy levels E_0 and E_1
        # E0 = 60px above base
        e0_y = cy_base - 55
        svg.append(f'<line x1="{cx - 120}" y1="{e0_y}" x2="{cx + 120}" y2="{e0_y}" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{cx + 130}" y="{e0_y + 4}" font-family="sans-serif" font-weight="bold" font-size="12" fill="#2563eb">E&#8320; = &frac12; &#8463;&omega;</text>')

        # Ground state Gaussian envelope
        g_pts = []
        for s in range(-100, 101, 4):
            x = cx + s
            gauss = math.exp(-0.5 * (s / 32.0)**2) * 35.0
            g_pts.append(f"{x:.1f},{e0_y - gauss:.1f}")
        svg.append(f'<polyline points="{" ".join(g_pts)}" fill="none" stroke="#2563eb" stroke-width="2.2"/>')

        # E1 = 165px above base
        e1_y = cy_base - 145
        svg.append(f'<line x1="{cx - 160}" y1="{e1_y}" x2="{cx + 160}" y2="{e1_y}" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{cx + 170}" y="{e1_y + 4}" font-family="sans-serif" font-weight="bold" font-size="12" fill="#dc2626">E&#8321; = 3/2 &#8463;&omega;</text>')

        # First excited state (odd parity)
        e1_pts = []
        for s in range(-130, 131, 4):
            x = cx + s
            val = (s / 30.0) * math.exp(-0.5 * (s / 35.0)**2) * 30.0
            e1_pts.append(f"{x:.1f},{e1_y - val:.1f}")
        svg.append(f'<polyline points="{" ".join(e1_pts)}" fill="none" stroke="#dc2626" stroke-width="2.2"/>')

        svg.append('</svg>')
        return "\n".join(svg)
