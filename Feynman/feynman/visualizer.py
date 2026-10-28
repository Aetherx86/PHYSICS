import math
from typing import List
from .path_integral import PathIntegralEngine

class FeynmanVisualizer:
    """Generates clean, scalable SVG diagrams illustrating Feynman's Path Integral formulation."""

    def render_path_bundle_svg(self, width: int = 700, height: int = 340) -> str:
        """
        Renders a spacetime bundle of trajectories connecting an initial state A to final state B.
        The classical trajectory (stationary action) is highlighted.
        """
        margin_left = 60
        margin_right = 60
        margin_top = 40
        margin_bottom = 50

        plot_w = width - margin_left - margin_right
        plot_h = height - margin_top - margin_bottom

        t_steps = 50
        times = [i / (t_steps - 1) for i in range(t_steps)]
        x_a = 0.2
        x_b = 0.8

        svg = [
            f'<svg viewBox="0 0 {width} {height}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; border-radius:6px; font-family:-apple-system, sans-serif;">',
            f'<!-- Axes -->',
            f'<line x1="{margin_left}" y1="{height - margin_bottom}" x2="{width - margin_right}" y2="{height - margin_bottom}" stroke="#94a3b8" stroke-width="1.5" />',
            f'<line x1="{margin_left}" y1="{height - margin_bottom}" x2="{margin_left}" y2="{margin_top}" stroke="#94a3b8" stroke-width="1.5" />',
            f'<text x="{width / 2}" y="{height - 15}" fill="#475569" font-size="13" text-anchor="middle">Time Coordinate t</text>',
            f'<text x="25" y="{height / 2}" fill="#475569" font-size="13" text-anchor="middle" transform="rotate(-90 25 {height / 2})">Position x(t)</text>',
            f'<text x="{margin_left}" y="{height - margin_bottom + 20}" fill="#64748b" font-size="12" text-anchor="middle">t_a</text>',
            f'<text x="{width - margin_right}" y="{height - margin_bottom + 20}" fill="#64748b" font-size="12" text-anchor="middle">t_b</text>'
        ]

        # Perturbation variations
        amplitudes = [-0.35, -0.22, -0.10, 0.10, 0.22, 0.35]
        for amp in amplitudes:
            path_pts = []
            for t in times:
                x_val = x_a + (x_b - x_a) * t + amp * math.sin(math.pi * t)
                px = margin_left + t * plot_w
                py = (height - margin_bottom) - x_val * plot_h
                path_pts.append(f"{px:.1f},{py:.1f}")
            svg.append(f'<polyline points="{" ".join(path_pts)}" fill="none" stroke="#93c5fd" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.8"/>')

        # Classical stationary trajectory (delta S = 0)
        cl_pts = []
        for t in times:
            x_val = x_a + (x_b - x_a) * t
            px = margin_left + t * plot_w
            py = (height - margin_bottom) - x_val * plot_h
            cl_pts.append(f"{px:.1f},{py:.1f}")
        svg.append(f'<polyline points="{" ".join(cl_pts)}" fill="none" stroke="#2563eb" stroke-width="3.5" />')

        # Endpoint Markers
        pa_x = margin_left
        pa_y = (height - margin_bottom) - x_a * plot_h
        pb_x = width - margin_right
        pb_y = (height - margin_bottom) - x_b * plot_h

        svg.append(f'<circle cx="{pa_x}" cy="{pa_y}" r="6" fill="#1e293b" />')
        svg.append(f'<text x="{pa_x - 12}" y="{pa_y + 4}" fill="#1e293b" font-size="13" font-weight="700" text-anchor="end">Source A (x_a, t_a)</text>')

        svg.append(f'<circle cx="{pb_x}" cy="{pb_y}" r="6" fill="#1e293b" />')
        svg.append(f'<text x="{pb_x + 12}" y="{pb_y + 4}" fill="#1e293b" font-size="13" font-weight="700" text-anchor="start">Detector B (x_b, t_b)</text>')

        # Labels
        svg.append(f'<text x="{width / 2}" y="{margin_top + 30}" fill="#2563eb" font-size="13" font-weight="700" text-anchor="middle">Classical Trajectory (Stationary Phase: δS = 0)</text>')
        svg.append(f'<text x="{width / 2}" y="{margin_top + 50}" fill="#64748b" font-size="11" text-anchor="middle">Fluctuating Quantum Histories (Destructive Interference)</text>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_phasor_interference_svg(self, width: int = 700, height: int = 240) -> str:
        """
        Renders complex amplitude phasors showing constructive phase addition along stationary path
        and destructive cancellation for fluctuating paths.
        """
        svg = [
            f'<svg viewBox="0 0 {width} {height}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; border-radius:6px; font-family:-apple-system, sans-serif;">',
            f'<text x="{width / 2}" y="28" fill="#0f172a" font-size="15" font-weight="700" text-anchor="middle">Quantum Phasor Summation: Constructive vs Destructive Interference</text>',
            f'<g transform="translate(40, 50)">',
            f'  <text x="120" y="25" fill="#2563eb" font-size="13" font-weight="700" text-anchor="middle">Stationary Phase Region (δS ≈ 0)</text>',
            f'  <text x="120" y="45" fill="#64748b" font-size="11" text-anchor="middle">Phasors align: Constructive reinforcement</text>',
            f'  <!-- Aligned vectors -->',
            f'  <line x1="20" y1="110" x2="65" y2="105" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arrow-blue)"/>',
            f'  <line x1="65" y1="105" x2="115" y2="102" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arrow-blue)"/>',
            f'  <line x1="115" y1="102" x2="165" y2="100" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arrow-blue)"/>',
            f'  <line x1="165" y1="100" x2="215" y2="100" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arrow-blue)"/>',
            f'  <line x1="20" y1="140" x2="215" y2="140" stroke="#059669" stroke-width="3" stroke-dasharray="4,2"/>',
            f'  <text x="115" y="160" fill="#059669" font-size="11" font-weight="700" text-anchor="middle">Large Resultant Probability Amplitude</text>',
            f'</g>',
            f'<g transform="translate(380, 50)">',
            f'  <text x="130" y="25" fill="#dc2626" font-size="13" font-weight="700" text-anchor="middle">Rapidly Oscillating Region (δS >> ħ)</text>',
            f'  <text x="130" y="45" fill="#64748b" font-size="11" text-anchor="middle">Random phases: Complete destructive cancellation</text>',
            f'  <!-- Curled spiral vectors -->',
            f'  <path d="M 80,110 L 110,95 L 125,120 L 105,135 L 85,125 L 95,105 L 105,115" fill="none" stroke="#dc2626" stroke-width="2.2" />',
            f'  <circle cx="105" cy="115" r="3" fill="#dc2626"/>',
            f'  <text x="130" y="160" fill="#dc2626" font-size="11" font-weight="700" text-anchor="middle">Net Amplitude ≈ 0</text>',
            f'</g>',
            f'</svg>'
        ]
        return "\n".join(svg)
