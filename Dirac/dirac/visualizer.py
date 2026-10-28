import math
from typing import List
from .relativistic_qm import E_REST_ELECTRON_EV, get_dirac_gamma_matrices

class DiracVisualizer:
    """Renders vector diagrams of the Dirac Sea, antimatter pair production, and Gamma matrices in SVG."""
    def __init__(self, width: int = 650, height: int = 400):
        self.width = width
        self.height = height

    def render_dirac_sea_svg(self) -> str:
        """
        Renders the Dirac energy spectrum:
        Positive continuum (E >= +mc^2), the forbidden mass gap (2mc^2 = 1.022 MeV),
        and the completely filled negative energy Dirac Sea (E <= -mc^2), with a hole positron.
        """
        cx = 320.0
        gap_half = 55.0
        cy_center = 200.0

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="100%" height="{self.height}">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1"/>',
            '<text x="20" y="30" font-family="sans-serif" font-weight="bold" font-size="15" fill="#0f172a">The Dirac Sea, Relativistic Mass Gap &amp; Antimatter Positron</text>',
            '<text x="20" y="50" font-family="sans-serif" font-size="12" fill="#64748b">E = &plusmn;&radic;(p&#178;c&#178; + m&#178;c&#8308;) with forbidden gap 2mc&#178; = 1.022 MeV</text>',
            # Vertical energy axis
            '<line x1="120" y1="360" x2="120" y2="70" stroke="#0f172a" stroke-width="2"/>',
            '<polygon points="120,60 116,72 124,72" fill="#0f172a"/>',
            '<text x="95" y="75" font-family="serif" font-weight="bold" font-size="14" fill="#0f172a">+E</text>',
            '<text x="95" y="365" font-family="serif" font-weight="bold" font-size="14" fill="#0f172a">-E</text>',
            # Positive energy continuum (E >= +mc^2)
            f'<rect x="150" y="70" width="460" height="{cy_center - gap_half - 70}" fill="rgba(37, 99, 235, 0.12)" stroke="#2563eb" stroke-dasharray="3,3"/>',
            f'<text x="170" y="105" font-family="sans-serif" font-weight="bold" font-size="13" fill="#1d4ed8">Positive Energy Continuum (E &ge; +m_e c&#178;)</text>',
            f'<line x1="120" y1="{cy_center - gap_half}" x2="610" y2="{cy_center - gap_half}" stroke="#2563eb" stroke-width="2"/>',
            f'<text x="35" y="{cy_center - gap_half + 4}" font-family="serif" font-weight="bold" font-size="12" fill="#1d4ed8">+mc&#178; (+511 keV)</text>',
            # Forbidden energy gap (2mc^2)
            f'<rect x="150" y="{cy_center - gap_half}" width="460" height="{2 * gap_half}" fill="#f8fafc" stroke="#cbd5e1"/>',
            f'<text x="250" y="{cy_center + 5}" font-family="sans-serif" font-weight="bold" font-size="13" fill="#64748b">Forbidden Mass Gap: 2m_e c&#178; = 1.022 MeV</text>',
            # Negative energy Dirac sea (E <= -mc^2)
            f'<rect x="150" y="{cy_center + gap_half}" width="460" height="85" fill="rgba(220, 38, 38, 0.12)" stroke="#dc2626" stroke-dasharray="3,3"/>',
            f'<line x1="120" y1="{cy_center + gap_half}" x2="610" y2="{cy_center + gap_half}" stroke="#dc2626" stroke-width="2"/>',
            f'<text x="35" y="{cy_center + gap_half + 4}" font-family="serif" font-weight="bold" font-size="12" fill="#b91c1c">-mc&#178; (-511 keV)</text>',
            f'<text x="170" y="325" font-family="sans-serif" font-weight="bold" font-size="13" fill="#b91c1c">Dirac Sea (Negative Energy Vacuum Saturated with Electrons)</text>',
        ]

        # Draw sea electrons (dots) in negative energy
        for x in range(180, 580, 45):
            for y in [cy_center + gap_half + 25, cy_center + gap_half + 55]:
                if x == 450 and y == cy_center + gap_half + 25:
                    # The hole (Positron)
                    svg.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#ffffff" stroke="#dc2626" stroke-width="2.5"/>')
                    svg.append(f'<text x="{x - 4}" y="{y + 4}" font-family="sans-serif" font-weight="bold" font-size="11" fill="#dc2626">+</text>')
                    svg.append(f'<text x="{x + 12}" y="{y + 4}" font-family="sans-serif" font-weight="bold" font-size="12" fill="#b91c1c">Hole = Positron (e+)</text>')
                else:
                    svg.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#dc2626"/>')

        # Pair creation electron in positive continuum
        svg.append(f'<circle cx="450" cy="{cy_center - gap_half - 30}" r="6" fill="#2563eb" stroke="#ffffff" stroke-width="1.5"/>')
        svg.append(f'<text x="465" y="{cy_center - gap_half - 26}" font-family="sans-serif" font-weight="bold" font-size="12" fill="#1d4ed8">Produced Electron (e-)</text>')

        # Photon excitation arrow
        svg.append(f'<path d="M 450 {cy_center + gap_half + 15} Q 420 {cy_center} 450 {cy_center - gap_half - 20}" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-dasharray="4,3"/>')
        svg.append(f'<text x="360" y="{cy_center + 4}" font-family="sans-serif" font-weight="bold" font-size="12" fill="#d97706">&gamma; &ge; 2mc&#178;</text>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_gamma_matrices_svg(self) -> str:
        """Renders the 4x4 Dirac Gamma matrix block-structure representation."""
        gammas = get_dirac_gamma_matrices()
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} 180" width="100%" height="180">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1"/>',
            '<text x="20" y="25" font-family="sans-serif" font-weight="bold" font-size="14" fill="#0f172a">Dirac 4&times;4 Gamma Matrices &gamma;&#751; in Dirac-Pauli Representation</text>',
        ]

        labels = ["&gamma;&#8304; = diag(I, -I)", "&gamma;&#185; = [[0, &sigma;&#8339;], [-&sigma;&#8339;, 0]]", "&gamma;&#178; = [[0, &sigma;&#7522;], [-&sigma;&#7522;, 0]]", "&gamma;&#179; = [[0, &sigma;&#7523;], [-&sigma;&#7523;, 0]]"]
        block_w = 120.0
        start_x = 35.0

        for idx, (g, lbl) in enumerate(zip(gammas, labels)):
            bx = start_x + idx * (block_w + 25)
            by = 45.0
            svg.append(f'<text x="{bx}" y="{by + 12}" font-family="sans-serif" font-weight="bold" font-size="11" fill="#475569">{lbl}</text>')
            cell_size = 22.0
            for r in range(4):
                for c in range(4):
                    val = g.data[r][c]
                    cx_pos = bx + c * cell_size
                    cy_pos = by + 22.0 + r * cell_size
                    if val.real > 0.5:
                        fill = "#dbeafe"
                        text_val = "+1"
                    elif val.real < -0.5:
                        fill = "#fee2e2"
                        text_val = "-1"
                    elif val.imag > 0.5:
                        fill = "#fef3c7"
                        text_val = "+i"
                    elif val.imag < -0.5:
                        fill = "#fef3c7"
                        text_val = "-i"
                    else:
                        fill = "#f8fafc"
                        text_val = "0"

                    svg.append(f'<rect x="{cx_pos}" y="{cy_pos}" width="{cell_size}" height="{cell_size}" fill="{fill}" stroke="#e2e8f0"/>')
                    svg.append(f'<text x="{cx_pos + 4}" y="{cy_pos + 15}" font-family="monospace" font-size="10" fill="#0f172a">{text_val}</text>')

        svg.append('</svg>')
        return "\n".join(svg)
