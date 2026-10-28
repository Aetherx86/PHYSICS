import math
from typing import List
from .blackbody import PlanckBlackbodyEngine, B_WIEN

class PlanckVisualizer:
    """Generates clean, scalable SVG diagrams of blackbody radiation spectra and quantum discretization."""

    def render_blackbody_curves_svg(self, width: int = 700, height: int = 340) -> str:
        """
        Renders Planck spectral radiance curves against the classical Rayleigh-Jeans divergence.
        """
        margin_left = 70
        margin_right = 50
        margin_top = 40
        margin_bottom = 50

        plot_w = width - margin_left - margin_right
        plot_h = height - margin_top - margin_bottom

        lambda_max_nm = 2000.0 # nm
        # Scale for 5500 K peak:
        peak_5500 = PlanckBlackbodyEngine.planck_spectral_radiance(527e-9, 5500.0)

        svg = [
            f'<svg viewBox="0 0 {width} {height}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; border-radius:6px; font-family:-apple-system, sans-serif;">',
            f'<!-- Visible Spectrum Band (380 nm - 750 nm) -->',
            f'<defs>',
            f'  <linearGradient id="vis-spectrum" x1="0%" y1="0%" x2="100%" y2="0%">',
            f'    <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.25"/>',
            f'    <stop offset="35%" stop-color="#3b82f6" stop-opacity="0.25"/>',
            f'    <stop offset="60%" stop-color="#10b981" stop-opacity="0.25"/>',
            f'    <stop offset="85%" stop-color="#eab308" stop-opacity="0.25"/>',
            f'    <stop offset="100%" stop-color="#ef4444" stop-opacity="0.25"/>',
            f'  </linearGradient>',
            f'</defs>'
        ]

        # Draw visible spectrum background
        vis_x1 = margin_left + (380.0 / lambda_max_nm) * plot_w
        vis_x2 = margin_left + (750.0 / lambda_max_nm) * plot_w
        vis_w = vis_x2 - vis_x1
        svg.append(f'<rect x="{vis_x1:.1f}" y="{margin_top}" width="{vis_w:.1f}" height="{plot_h}" fill="url(#vis-spectrum)" />')
        svg.append(f'<text x="{(vis_x1 + vis_x2) / 2:.1f}" y="{margin_top + 16}" fill="#64748b" font-size="11" font-weight="600" text-anchor="middle">Visible Light</text>')

        # Axes
        svg.append(f'<line x1="{margin_left}" y1="{height - margin_bottom}" x2="{width - margin_right}" y2="{height - margin_bottom}" stroke="#94a3b8" stroke-width="1.5" />')
        svg.append(f'<line x1="{margin_left}" y1="{height - margin_bottom}" x2="{margin_left}" y2="{margin_top}" stroke="#94a3b8" stroke-width="1.5" />')
        svg.append(f'<text x="{width / 2}" y="{height - 15}" fill="#475569" font-size="13" text-anchor="middle">Wavelength λ (nm)</text>')
        svg.append(f'<text x="22" y="{height / 2}" fill="#475569" font-size="13" text-anchor="middle" transform="rotate(-90 22 {height / 2})">Spectral Radiance B_λ</text>')

        # Ticks on X
        for tick_nm in [0, 500, 1000, 1500, 2000]:
            px = margin_left + (tick_nm / lambda_max_nm) * plot_w
            py = height - margin_bottom
            svg.append(f'<line x1="{px}" y1="{py}" x2="{px}" y2="{py + 5}" stroke="#94a3b8" stroke-width="1"/>')
            svg.append(f'<text x="{px}" y="{py + 18}" fill="#64748b" font-size="11" text-anchor="middle">{tick_nm}</text>')

        # Planck Curves
        curves = [
            (5500.0, "#2563eb", "Planck: T = 5500 K (Sun)"),
            (4000.0, "#059669", "Planck: T = 4000 K"),
            (3000.0, "#d97706", "Planck: T = 3000 K")
        ]

        steps = 150
        for temp, color, label in curves:
            pts = []
            for i in range(1, steps + 1):
                lam_nm = (i / steps) * lambda_max_nm
                b_val = PlanckBlackbodyEngine.planck_spectral_radiance(lam_nm * 1.0e-9, temp)
                px = margin_left + (lam_nm / lambda_max_nm) * plot_w
                py = (height - margin_bottom) - (b_val / peak_5500) * plot_h
                py_clamped = max(margin_top, min(py, height - margin_bottom))
                pts.append(f"{px:.1f},{py_clamped:.1f}")
            svg.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2.5" />')

        # Rayleigh-Jeans classical UV catastrophe (at 5500 K)
        rj_pts = []
        for i in range(25, steps + 1):
            lam_nm = (i / steps) * lambda_max_nm
            b_rj = PlanckBlackbodyEngine.rayleigh_jeans_radiance(lam_nm * 1.0e-9, 5500.0)
            px = margin_left + (lam_nm / lambda_max_nm) * plot_w
            py = (height - margin_bottom) - (b_rj / peak_5500) * plot_h
            if py < margin_top:
                py = margin_top
            rj_pts.append(f"{px:.1f},{py:.1f}")
        svg.append(f'<polyline points="{" ".join(rj_pts)}" fill="none" stroke="#dc2626" stroke-width="2.2" stroke-dasharray="4,3" />')

        # Legend
        leg_x = width - margin_right - 230
        leg_y = margin_top + 15
        for idx, (temp, color, label) in enumerate(curves):
            ly = leg_y + idx * 20
            svg.append(f'<line x1="{leg_x}" y1="{ly}" x2="{leg_x + 22}" y2="{ly}" stroke="{color}" stroke-width="2.5" />')
            svg.append(f'<text x="{leg_x + 28}" y="{ly + 4}" fill="#334155" font-size="11" font-weight="600">{label}</text>')

        # RJ legend entry
        ly_rj = leg_y + len(curves) * 20
        svg.append(f'<line x1="{leg_x}" y1="{ly_rj}" x2="{leg_x + 22}" y2="{ly_rj}" stroke="#dc2626" stroke-width="2.2" stroke-dasharray="4,3" />')
        svg.append(f'<text x="{leg_x + 28}" y="{ly_rj + 4}" fill="#dc2626" font-size="11" font-weight="700">Classical UV Catastrophe</text>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_energy_quantization_svg(self, width: int = 700, height: int = 220) -> str:
        """
        Renders the discrete energy ladder E_n = n * h * nu introduced by Planck in 1900.
        """
        svg = [
            f'<svg viewBox="0 0 {width} {height}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; border-radius:6px; font-family:-apple-system, sans-serif;">',
            f'<text x="{width / 2}" y="25" fill="#0f172a" font-size="15" font-weight="700" text-anchor="middle">Max Planck: Discrete Quanta of Action E = n · h · ν</text>',
            f'<g transform="translate(60, 45)">',
            f'  <rect x="0" y="0" width="250" height="135" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>',
            f'  <text x="125" y="24" fill="#dc2626" font-size="13" font-weight="700" text-anchor="middle">Classical Continuous (Equipartition)</text>',
            f'  <defs><linearGradient id="cont-grad" x1="0%" y1="100%" x2="0%" y2="0%"><stop offset="0%" stop-color="#fee2e2"/><stop offset="100%" stop-color="#ef4444"/></linearGradient></defs>',
            f'  <rect x="30" y="40" width="60" height="80" fill="url(#cont-grad)" rx="4"/>',
            f'  <text x="170" y="70" fill="#475569" font-size="11" text-anchor="middle">Continuous energy</text>',
            f'  <text x="170" y="88" fill="#dc2626" font-size="11" font-weight="700" text-anchor="middle">Predicts E_tot → ∞</text>',
            f'  <text x="170" y="106" fill="#64748b" font-size="10" text-anchor="middle">(UV Catastrophe)</text>',
            f'</g>',
            f'<g transform="translate(380, 45)">',
            f'  <rect x="0" y="0" width="260" height="135" rx="6" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>',
            f'  <text x="130" y="24" fill="#059669" font-size="13" font-weight="700" text-anchor="middle">Planck Quantized Oscillators (1900)</text>',
            f'  <!-- Energy rungs -->',
            f'  <line x1="30" y1="115" x2="110" y2="115" stroke="#059669" stroke-width="3"/>',
            f'  <text x="120" y="118" fill="#334155" font-size="10">n = 0 (E = 0)</text>',
            f'  <line x1="30" y1="90" x2="110" y2="90" stroke="#059669" stroke-width="3"/>',
            f'  <text x="120" y="93" fill="#334155" font-size="10">n = 1 (E = hν)</text>',
            f'  <line x1="30" y1="65" x2="110" y2="65" stroke="#059669" stroke-width="3"/>',
            f'  <text x="120" y="68" fill="#334155" font-size="10">n = 2 (E = 2hν)</text>',
            f'  <line x1="30" y1="40" x2="110" y2="40" stroke="#059669" stroke-width="3"/>',
            f'  <text x="120" y="43" fill="#334155" font-size="10">n = 3 (E = 3hν)</text>',
            f'</g>',
            f'</svg>'
        ]
        return "\n".join(svg)
