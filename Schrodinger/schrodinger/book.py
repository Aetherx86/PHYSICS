import html
from typing import List
from .wave_mechanics import HBAR, M_ELECTRON, PotentialWellSolver
from .visualizer import SchrodingerVisualizer

class SchrodingerBookGenerator:
    """Generates the interactive readable edition of Erwin Schrödinger's Wave Mechanics."""
    def __init__(self):
        self.visualizer = SchrodingerVisualizer()

    def generate_html(self) -> str:
        well_svg = self.visualizer.render_potential_well_svg()
        harm_svg = self.visualizer.render_harmonic_oscillator_svg()

        solver = PotentialWellSolver(length=1.0e-9)
        e1_ev = solver.energy_eigenvalue(1) / 1.602176634e-19
        e2_ev = solver.energy_eigenvalue(2) / 1.602176634e-19
        e3_ev = solver.energy_eigenvalue(3) / 1.602176634e-19

        return rf"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Erwin Schrödinger: Wave Mechanics &amp; The Wave Equation — Interactive Edition</title>
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
            grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr));
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
        <h1>Erwin Schrödinger: Wave Mechanics</h1>
        <p class="subtitle">Quantisierung als Eigenwertproblem (1926) &amp; The Non-Relativistic Wave Equation</p>
    </header>

    <main>
        <section id="tdse">
            <h2 class="section-title">The Time-Dependent Schrödinger Equation (TDSE)</h2>
            <p>
                In early 1926, Erwin Schrödinger translated Louis de Broglie's matter-wave hypothesis into a partial differential wave equation governing the temporal evolution of quantum states:
            </p>
            <div class="equation-box">
                $$i\hbar \frac{{\partial \psi(\mathbf{{r}}, t)}}{{\partial t}} = \hat{{H}} \psi(\mathbf{{r}}, t) = \left( -\frac{{\hbar^2}}{{2m}} \nabla^2 + V(\mathbf{{r}}, t) \right) \psi(\mathbf{{r}}, t)$$
            </div>
            <p>
                By Born's statistical interpretation, the wavefunction squared $|\psi(\mathbf{{r}}, t)|^2 = \psi^* \psi$ specifies the spatial probability density of locating the particle, obeying local probability conservation:
            </p>
            <div class="equation-box">
                $$\frac{{\partial \rho}}{{\partial t}} + \nabla \cdot \mathbf{{j}} = 0, \quad \mathbf{{j}} = \frac{{\hbar}}{{2mi}} \left( \psi^* \nabla \psi - \psi \nabla \psi^* \right)$$
            </div>
        </section>

        <section id="tise-box">
            <h2 class="section-title">Quantization as an Eigenvalue Problem: Particle in a Box</h2>
            <p>
                For time-independent potentials $V(\mathbf{{r}})$, separation of variables $\psi(x, t) = \phi(x) e^{{-iEt/\hbar}}$ reduces the dynamics to the stationary Time-Independent Schrödinger Equation (TISE):
            </p>
            <div class="equation-box">
                $$\hat{{H}}\psi_n(x) = E_n \psi_n(x), \quad \psi_n(x) = \sqrt{{\frac{{2}}{{L}}}} \sin\left( \frac{{n\pi x}}{{L}} \right)$$
            </div>
            <p>
                Enforcing Dirichlet boundary conditions $\psi(0) = \psi(L) = 0$ at the impenetrable walls eliminates continuous energy spectra, producing exact discrete quantum energy levels:
            </p>
            <div class="figure-box">
                {well_svg}
            </div>
            <div class="metrics-grid">
                <div class="metric-card">
                    <h4>Ground State Energy (n = 1)</h4>
                    <p>$$E_1 = \frac{{\pi^2 \hbar^2}}{{2m L^2}}$$</p>
                    <span class="metric-val">{e1_ev:.3f} eV</span>
                </div>
                <div class="metric-card">
                    <h4>First Excited State (n = 2)</h4>
                    <p>$$E_2 = 4 E_1$$</p>
                    <span class="metric-val">{e2_ev:.3f} eV</span>
                </div>
                <div class="metric-card">
                    <h4>Second Excited State (n = 3)</h4>
                    <p>$$E_3 = 9 E_1$$</p>
                    <span class="metric-val">{e3_ev:.3f} eV</span>
                </div>
            </div>
        </section>

        <section id="harmonic-oscillator">
            <h2 class="section-title">The Quantum Harmonic Oscillator</h2>
            <p>
                Under a parabolic restoring potential $V(x) = \frac{{1}}{{2}}m\omega^2 x^2$, the stationary states are Hermite-Gaussian modes possessing non-zero ground-state vacuum fluctuations:
            </p>
            <div class="equation-box">
                $$E_n = \left( n + \frac{{1}}{{2}} \right) \hbar \omega, \quad \psi_0(x) = \left( \frac{{m\omega}}{{\pi \hbar}} \right)^{{1/4}} \exp\left( -\frac{{m\omega x^2}}{{2\hbar}} \right)$$
            </div>
            <div class="figure-box">
                {harm_svg}
            </div>
        </section>
    </main>
</body>
</html>
"""
