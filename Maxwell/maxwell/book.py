import html
from typing import List
from .electrodynamics import EPSILON_0, MU_0, C_EXACT, ElectrodynamicsEngine, MAXWELL_EQUATIONS
from .visualizer import MaxwellVisualizer

class MaxwellBookGenerator:
    """Generates the interactive readable edition of James Clerk Maxwell's Electromagnetism."""
    def __init__(self):
        self.visualizer = MaxwellVisualizer()

    def generate_html(self) -> str:
        wave_svg = self.visualizer.render_em_wave_svg(wavelength=1.0, e0=1.0)
        disp_svg = self.visualizer.render_displacement_current_svg()

        c_calc = ElectrodynamicsEngine.calculate_wave_speed(EPSILON_0, MU_0)
        s_flux = ElectrodynamicsEngine.poynting_vector_magnitude(e_amplitude=1.0)

        eqs_html = []
        for eq in MAXWELL_EQUATIONS:
            eqs_html.append(f"""
            <div class="eq-card">
                <div class="eq-header">
                    <h3>{html.escape(eq.name)}</h3>
                </div>
                <div class="eq-math-row">
                    <div class="eq-math-col">
                        <span class="math-tag">Differential Form</span>
                        <div class="math-box">$${eq.differential_form}$$</div>
                    </div>
                    <div class="eq-math-col">
                        <span class="math-tag">Integral Form</span>
                        <div class="math-box">$${eq.integral_form}$$</div>
                    </div>
                </div>
                <p class="eq-meaning"><strong>Physical Meaning:</strong> {html.escape(eq.physical_meaning)}</p>
                <p class="eq-context"><em>Historical Context:</em> {html.escape(eq.discovery_context)}</p>
            </div>
            """)

        eqs_joined = "".join(eqs_html)

        return rf"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>James Clerk Maxwell: Classical Electrodynamics &amp; Wave Theory — Interactive Edition</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
    <style>
        :root {{
            --primary: #0f172a;
            --accent: #2563eb;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --muted: #64748b;
            --border: #e2e8f0;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Charter", Georgia, serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            overflow-x: hidden;
        }}
        header {{
            background: var(--primary);
            color: #ffffff;
            padding: 3.5rem 2rem;
            text-align: center;
        }}
        header h1 {{ font-size: 2.6rem; font-weight: 800; }}
        header p.subtitle {{ font-size: 1.25rem; color: #94a3b8; margin-top: 0.5rem; }}
        main {{ max-width: 1050px; margin: -1.5rem auto 4rem; padding: 0 1.5rem; }}
        section {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 2rem;
            margin-bottom: 2.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            overflow: hidden;
        }}
        h2.section-title {{ font-size: 1.7rem; color: var(--primary); margin-bottom: 1.25rem; border-bottom: 2px solid var(--border); padding-bottom: 0.4rem; }}
        .eq-card {{
            border: 1px solid var(--border);
            background: #fafafa;
            border-radius: 6px;
            padding: 1.25rem;
            margin-bottom: 1.5rem;
        }}
        .eq-header h3 {{ color: var(--primary); margin-bottom: 0.75rem; font-size: 1.2rem; }}
        .eq-math-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
            gap: 1rem;
            margin-bottom: 0.75rem;
        }}
        .math-tag {{
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--accent);
            text-transform: uppercase;
            display: block;
            margin-bottom: 0.25rem;
        }}
        .math-box {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 0.85rem;
            overflow-x: auto;
            max-width: 100%;
            box-sizing: border-box;
            text-align: center;
        }}
        .eq-meaning {{ font-size: 0.95rem; margin-top: 0.5rem; }}
        .eq-context {{ font-size: 0.88rem; color: var(--muted); margin-top: 0.25rem; }}
        .equation-box {{
            background: #f1f5f9;
            padding: 1.25rem;
            border-left: 4px solid var(--accent);
            border-radius: 0 6px 6px 0;
            margin: 1.25rem 0;
            overflow-x: auto;
            max-width: 100%;
            box-sizing: border-box;
            text-align: center;
        }}
        .figure-box {{
            margin: 1.5rem 0;
            width: 100%;
            overflow-x: auto;
        }}
        svg {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
            gap: 1.25rem;
            margin-top: 1.25rem;
        }}
        .metric-card {{
            background: #f8fafc;
            border: 1px solid var(--border);
            padding: 1.25rem;
            border-radius: 6px;
        }}
        .metric-card h4 {{ color: var(--primary); margin-bottom: 0.4rem; }}
        .metric-val {{ font-size: 1.25rem; font-weight: bold; color: var(--accent); margin-top: 0.3rem; display: block; }}
        @media print {{
            header {{ display: none; }}
            body {{ background: #ffffff; color: #000000; font-size: 11pt; }}
            section {{ page-break-inside: avoid; border: none; box-shadow: none; margin-bottom: 2rem; }}
            svg {{ max-width: 85%; margin: 0 auto; }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>James Clerk Maxwell: The Electromagnetic Field</h1>
        <p class="subtitle">A Dynamical Theory of the Electromagnetic Field (1865) &amp; Treatise on Electricity and Magnetism</p>
    </header>

    <main>
        <section id="equations">
            <h2 class="section-title">The Four Maxwell Equations</h2>
            <p style="margin-bottom: 1.25rem;">
                In 1865, James Clerk Maxwell unified electricity, magnetism, and optics into a single comprehensive field theory:
            </p>
            {eqs_joined}
        </section>

        <section id="wave-equation">
            <h2 class="section-title">Electromagnetic Wave Equation &amp; The Speed of Light</h2>
            <p>
                Taking the curl of the curl of the electric field in charge-free vacuum ($\rho = 0, \mathbf{{J}} = 0$):
            </p>
            <div class="equation-box">
                $$\nabla \times (\nabla \times \mathbf{{E}}) = \nabla(\nabla \cdot \mathbf{{E}}) - \nabla^2 \mathbf{{E}} = -\frac{{\partial}}{{\partial t}}(\nabla \times \mathbf{{B}}) = -\mu_0 \varepsilon_0 \frac{{\partial^2 \mathbf{{E}}}}{{\partial t^2}}$$
            </div>
            <p>
                Yielding the three-dimensional vector wave equation predicting electromagnetic waves traveling at speed $c$:
            </p>
            <div class="equation-box">
                $$\nabla^2 \mathbf{{E}} - \frac{{1}}{{c^2}} \frac{{\partial^2 \mathbf{{E}}}}{{\partial t^2}} = 0, \quad c = \frac{{1}}{{\sqrt{{\mu_0 \varepsilon_0}}}}$$
            </div>
            <div class="figure-box">
                {wave_svg}
            </div>
            <div class="metrics-grid">
                <div class="metric-card">
                    <h4>Theoretical Light Velocity</h4>
                    <p>$$c = \frac{{1}}{{\sqrt{{\mu_0 \varepsilon_0}}}}$$</p>
                    <span class="metric-val">{c_calc:,.1f} m/s</span>
                </div>
                <div class="metric-card">
                    <h4>Poynting Energy Flux Density</h4>
                    <p>$$\langle S \rangle = \frac{{1}}{{2}} \varepsilon_0 c E_0^2$$</p>
                    <span class="metric-val">{s_flux * 1000.0:.3f} mW/m&#178;</span>
                </div>
            </div>
        </section>

        <section id="displacement-current">
            <h2 class="section-title">Maxwell's Displacement Current</h2>
            <p>
                Amp&egrave;re's original circuital law failed during capacitor charging because no conduction current traverses the dielectric gap.
                Maxwell resolved this asymmetry by introducing the displacement current $I_D = \varepsilon_0 \frac{{d\Phi_E}}{{dt}}$:
            </p>
            <div class="figure-box">
                {disp_svg}
            </div>
        </section>
    </main>
</body>
</html>
"""
