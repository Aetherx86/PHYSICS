import math
from typing import List
from .statistical_mechanics import BoltzmannStatisticalEngine, M_N2, K_B

class BoltzmannVisualizer:
    """Generates clean, scalable SVG visualizations of statistical distributions and entropy."""

    def render_maxwell_boltzmann_svg(self, width: int = 700, height: int = 340) -> str:
        """
        Renders Maxwell-Boltzmann speed distributions for N2 gas at T = 100 K, 300 K, and 1000 K.
        """
        margin_left = 65
        margin_right = 45
        margin_top = 40
        margin_bottom = 50

        plot_w = width - margin_left - margin_right
        plot_h = height - margin_top - margin_bottom

        v_max = 1800.0  # m/s
        pdf_max = 0.0035 # max probability density for 100 K peak

        temperatures = [
            (100.0, "#2563eb", "T = 100 K (Cold)"),
            (300.0, "#059669", "T = 300 K (Room Temp)"),
            (1000.0, "#dc2626", "T = 1000 K (Hot)")
        ]

        svg = [
            f'<svg viewBox="0 0 {width} {height}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; border-radius:6px; font-family:-apple-system, sans-serif;">',
            f'<!-- Axes -->',
            f'<line x1="{margin_left}" y1="{height - margin_bottom}" x2="{width - margin_right}" y2="{height - margin_bottom}" stroke="#94a3b8" stroke-width="1.5" />',
            f'<line x1="{margin_left}" y1="{height - margin_bottom}" x2="{margin_left}" y2="{margin_top}" stroke="#94a3b8" stroke-width="1.5" />',
            f'<text x="{width / 2}" y="{height - 15}" fill="#475569" font-size="13" text-anchor="middle">Molecular Speed v (m/s) [Nitrogen N2]</text>',
            f'<text x="20" y="{height / 2}" fill="#475569" font-size="13" text-anchor="middle" transform="rotate(-90 20 {height / 2})">Probability Density f(v)</text>'
        ]

        # X-ticks
        for speed_tick in [0, 400, 800, 1200, 1600]:
            px = margin_left + (speed_tick / v_max) * plot_w
            py = height - margin_bottom
            svg.append(f'<line x1="{px}" y1="{py}" x2="{px}" y2="{py + 5}" stroke="#94a3b8" stroke-width="1"/>')
            svg.append(f'<text x="{px}" y="{py + 18}" fill="#64748b" font-size="11" text-anchor="middle">{speed_tick}</text>')

        # Plot curves
        steps = 150
        for temp, color, label in temperatures:
            pts = []
            for i in range(steps + 1):
                v = (i / steps) * v_max
                f_val = BoltzmannStatisticalEngine.maxwell_boltzmann_pdf(v, temp, M_N2)
                px = margin_left + (v / v_max) * plot_w
                py = (height - margin_bottom) - (min(f_val, pdf_max) / pdf_max) * plot_h
                pts.append(f"{px:.1f},{py:.1f}")

            svg.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2.5" />')

        # Legend
        legend_x = width - margin_right - 180
        legend_y = margin_top + 10
        for idx, (temp, color, label) in enumerate(temperatures):
            ly = legend_y + idx * 22
            svg.append(f'<line x1="{legend_x}" y1="{ly}" x2="{legend_x + 25}" y2="{ly}" stroke="{color}" stroke-width="2.5" />')
            svg.append(f'<text x="{legend_x + 32}" y="{ly + 4}" fill="#334155" font-size="12" font-weight="600">{label}</text>')

        # Characteristic speed marks for 300 K
        speeds_300 = BoltzmannStatisticalEngine.characteristic_speeds(300.0, M_N2)
        vp = speeds_300["v_probable"]
        px_vp = margin_left + (vp / v_max) * plot_w
        svg.append(f'<line x1="{px_vp}" y1="{height - margin_bottom}" x2="{px_vp}" y2="{margin_top + 45}" stroke="#059669" stroke-width="1.5" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{px_vp}" y="{margin_top + 38}" fill="#059669" font-size="10" font-weight="700" text-anchor="middle">v_p ({vp:.0f} m/s)</text>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_entropy_microstates_svg(self, width: int = 700, height: int = 220) -> str:
        """
        Renders the microscopic configuration spaces and the logarithmic growth of thermodynamic entropy.
        """
        svg = [
            f'<svg viewBox="0 0 {width} {height}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; border-radius:6px; font-family:-apple-system, sans-serif;">',
            f'<text x="{width / 2}" y="25" fill="#0f172a" font-size="15" font-weight="700" text-anchor="middle">Boltzmann Entropy: Microscopic Multiplicity to Macroscopic State</text>',
            f'<g transform="translate(60, 45)">',
            f'  <rect x="0" y="0" width="240" height="130" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>',
            f'  <text x="120" y="24" fill="#1e293b" font-size="13" font-weight="700" text-anchor="middle">Microstate Lattice Multiplicity (Ω)</text>',
            f'  <circle cx="40" cy="55" r="4" fill="#3b82f6"/>',
            f'  <circle cx="80" cy="70" r="4" fill="#ef4444"/>',
            f'  <circle cx="130" cy="50" r="4" fill="#10b981"/>',
            f'  <circle cx="170" cy="85" r="4" fill="#8b5cf6"/>',
            f'  <circle cx="200" cy="60" r="4" fill="#f59e0b"/>',
            f'  <text x="120" y="115" fill="#64748b" font-size="11" text-anchor="middle">Ω = W: Total Accessible Microstates</text>',
            f'</g>',
            f'<g transform="translate(380, 45)">',
            f'  <rect x="0" y="0" width="260" height="130" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>',
            f'  <text x="130" y="24" fill="#0f172a" font-size="13" font-weight="700" text-anchor="middle">Logarithmic Invariant: S = k_B ln Ω</text>',
            f'  <text x="130" y="60" fill="#2563eb" font-size="20" font-weight="800" text-anchor="middle">S = k · log W</text>',
            f'  <text x="130" y="85" fill="#475569" font-size="11" text-anchor="middle">k_B = 1.380649 × 10^-23 J / K</text>',
            f'  <text x="130" y="112" fill="#059669" font-size="11" font-weight="600" text-anchor="middle">Extensive: S(A + B) = S(A) + S(B)</text>',
            f'</g>',
            f'</svg>'
        ]
        return "\n".join(svg)
