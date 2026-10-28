import math
from typing import List, Tuple
from .electrodynamics import ElectrodynamicsEngine

class MaxwellVisualizer:
    """Renders vector diagrams of electromagnetic wave propagation and field relations in SVG."""
    def __init__(self, width: int = 650, height: int = 380):
        self.width = width
        self.height = height

    def render_em_wave_svg(self, wavelength: float = 1.0, e0: float = 1.0) -> str:
        """
        Renders an isometric 3D-projected vector field diagram of an electromagnetic plane wave.
        E-field (blue) oscillates vertically in the xz-plane.
        B-field (red) oscillates horizontally in the yz-plane.
        Poynting vector S (green) points in the direction of wave propagation +z.
        """
        origin_x = 70.0
        origin_y = 190.0
        z_length = 490.0
        amp = 75.0

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="100%" height="{self.height}">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1"/>',
            '<text x="20" y="30" font-family="sans-serif" font-weight="bold" font-size="15" fill="#0f172a">Transverse Electromagnetic Wave Propagation (c = 1 / &radic;(&mu;&#8320; &epsilon;&#8320;))</text>',
            '<text x="20" y="50" font-family="sans-serif" font-size="12" fill="#64748b">Mutually perpendicular E (vertical blue) and B (transverse red) fields with Poynting flux S = (E &times; B)/&mu;&#8320;</text>',
            # Propagation axis z
            f'<line x1="{origin_x}" y1="{origin_y}" x2="{origin_x + z_length}" y2="{origin_y}" stroke="#475569" stroke-width="2"/>',
            f'<polygon points="{origin_x + z_length + 10},{origin_y} {origin_x + z_length},{origin_y - 4} {origin_x + z_length},{origin_y + 4}" fill="#475569"/>',
            f'<text x="{origin_x + z_length + 15}" y="{origin_y + 4}" font-family="serif" font-weight="bold" font-size="14" fill="#475569">+z (k)</text>',
        ]

        # Wave curve and field vectors
        steps = 32
        e_points = []
        b_points = []
        for i in range(steps + 1):
            fraction = i / steps
            z = origin_x + fraction * z_length
            phase = 2.0 * math.pi * fraction * 1.5  # 1.5 cycles
            e_val = math.sin(phase) * amp
            b_val = math.sin(phase) * (amp * 0.55) # projected at isometric angle 30 deg

            # Isometric projection for B: dx = b_val * cos(30), dy = b_val * sin(30)
            iso_dx = b_val * 0.866
            iso_dy = b_val * 0.5

            e_y = origin_y - e_val
            b_x = z + iso_dx
            b_y = origin_y + iso_dy

            e_points.append(f"{z:.1f},{e_y:.1f}")
            b_points.append(f"{b_x:.1f},{b_y:.1f}")

            # Draw discrete vector arrows at periodic nodes
            if i % 2 == 0 and abs(math.sin(phase)) > 0.1:
                # E vector (Blue)
                svg.append(f'<line x1="{z:.1f}" y1="{origin_y}" x2="{z:.1f}" y2="{e_y:.1f}" stroke="#2563eb" stroke-width="1.8"/>')
                # B vector (Red)
                svg.append(f'<line x1="{z:.1f}" y1="{origin_y}" x2="{b_x:.1f}" y2="{b_y:.1f}" stroke="#dc2626" stroke-width="1.8"/>')

        # Continuous wave envelopes
        svg.append(f'<polyline points="{" ".join(e_points)}" fill="none" stroke="#2563eb" stroke-width="2.5"/>')
        svg.append(f'<polyline points="{" ".join(b_points)}" fill="none" stroke="#dc2626" stroke-width="2.5"/>')

        # Legend badges
        svg.append('<rect x="25" y="325" width="130" height="24" fill="#eff6ff" rx="4" stroke="#bfdbfe"/>')
        svg.append('<text x="35" y="341" font-family="sans-serif" font-weight="bold" font-size="12" fill="#1d4ed8">Electric Field E (V/m)</text>')

        svg.append('<rect x="175" y="325" width="130" height="24" fill="#fef2f2" rx="4" stroke="#fecaca"/>')
        svg.append('<text x="185" y="341" font-family="sans-serif" font-weight="bold" font-size="12" fill="#b91c1c">Magnetic Field B (T)</text>')

        svg.append('<rect x="325" y="325" width="160" height="24" fill="#f0fdf4" rx="4" stroke="#bbf7d0"/>')
        svg.append('<text x="335" y="341" font-family="sans-serif" font-weight="bold" font-size="12" fill="#15803d">Poynting Flux S (W/m&#178;)</text>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_displacement_current_svg(self) -> str:
        """Renders Maxwell's capacitor circuit illustrating the displacement current I_D = eps_0 d(Phi_E)/dt."""
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="100%" height="{self.height}">',
            '<rect width="100%" height="100%" fill="#ffffff" rx="8" stroke="#e2e8f0" stroke-width="1"/>',
            '<text x="20" y="30" font-family="sans-serif" font-weight="bold" font-size="15" fill="#0f172a">Maxwell\'s Displacement Current: Conduction &amp; Vacuum Continuity</text>',
            '<text x="20" y="50" font-family="sans-serif" font-size="12" fill="#64748b">I_C = I_D = &epsilon;&#8320; (d&Phi;_E / dt) guarantees Amp&egrave;re loop invariance</text>',
            # Left wire
            '<line x1="80" y1="180" x2="230" y2="180" stroke="#0f172a" stroke-width="3"/>',
            '<text x="130" y="160" font-family="sans-serif" font-weight="bold" font-size="13" fill="#2563eb">I_conduction &rarr;</text>',
            # Left plate (+ charge)
            '<rect x="230" y="90" width="16" height="180" fill="#2563eb" rx="2"/>',
            '<text x="235" y="80" font-family="sans-serif" font-weight="bold" font-size="13" fill="#2563eb">+Q</text>',
            # Right plate (- charge)
            '<rect x="400" y="90" width="16" height="180" fill="#dc2626" rx="2"/>',
            '<text x="405" y="80" font-family="sans-serif" font-weight="bold" font-size="13" fill="#dc2626">-Q</text>',
            # Right wire
            '<line x1="416" y1="180" x2="560" y2="180" stroke="#0f172a" stroke-width="3"/>',
            '<text x="470" y="160" font-family="sans-serif" font-weight="bold" font-size="13" fill="#2563eb">&rarr; I_conduction</text>',
        ]

        # Electric field lines between plates
        for y in range(110, 270, 30):
            svg.append(f'<line x1="246" y1="{y}" x2="396" y2="{y}" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4,3"/>')
            svg.append(f'<polygon points="398,{y} 392,{y-3} 392,{y+3}" fill="#f59e0b"/>')

        svg.append('<rect x="260" y="280" width="130" height="26" fill="#fef3c7" rx="4" stroke="#fde68a"/>')
        svg.append('<text x="270" y="297" font-family="sans-serif" font-weight="bold" font-size="12" fill="#b45309">I_D = &epsilon;&#8320; (d&Phi;_E / dt)</text>')

        svg.append('</svg>')
        return "\n".join(svg)
