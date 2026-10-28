import html
from typing import List
from .relativistic_qm import E_REST_ELECTRON_EV, RelativisticDiracEngine
from .visualizer import DiracVisualizer

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Paul Dirac: Relativistic Quantum Mechanics & The Dirac Equation - Interactive Edition</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}]});"></script>
    <style>
        :root {
            --primary: #0f172a;
            --accent: #2563eb;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --muted: #64748b;
            --border: #e2e8f0;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Charter", Georgia, serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            overflow-x: hidden;
        }
        header {
            background: var(--primary);
            color: #ffffff;
            padding: 3.5rem 2rem;
            text-align: center;
        }
        header h1 { font-size: 2.6rem; font-weight: 800; letter-spacing: -0.02em; }
        header .subtitle { font-size: 1.25rem; color: #94a3b8; margin-top: 0.5rem; }
        main {
            max-width: 960px;
            margin: 2rem auto;
            padding: 0 1.5rem;
        }
        section {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 2.5rem;
            margin-bottom: 2.5rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }
        h2.section-title {
            font-size: 1.75rem;
            color: var(--primary);
            margin-bottom: 1.25rem;
            border-bottom: 2px solid var(--border);
            padding-bottom: 0.5rem;
        }
        p { margin-bottom: 1.2rem; font-size: 1.05rem; }
        .equation-box {
            background: #f1f5f9;
            border-left: 4px solid var(--accent);
            padding: 1.25rem;
            margin: 1.5rem 0;
            border-radius: 0 6px 6px 0;
            overflow-x: auto;
        }
        .figure-box {
            text-align: center;
            margin: 2rem 0;
            padding: 1rem;
            background: #fafafa;
            border: 1px solid var(--border);
            border-radius: 6px;
            overflow-x: auto;
        }
        .interactive-card {
            background: #f8fafc;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1.5rem 0;
        }
        .interactive-title {
            font-weight: 700;
            font-size: 1.2rem;
            color: var(--primary);
            margin-bottom: 1rem;
        }
        .control-group {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }
        label { font-weight: 600; min-width: 180px; }
        input[type="range"] { flex: 1; min-width: 200px; }
        input[type="number"] {
            width: 120px;
            padding: 0.4rem 0.6rem;
            border: 1px solid var(--border);
            border-radius: 4px;
        }
        .result-panel {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 1rem;
            font-family: monospace;
            font-size: 0.95rem;
        }
        footer {
            text-align: center;
            padding: 3rem 1rem;
            color: var(--muted);
            border-top: 1px solid var(--border);
        }
        @media print {
            body { background: #fff; color: #000; }
            section { box-shadow: none; border: 1px solid #ccc; page-break-inside: avoid; }
            .interactive-card { border: 1px dashed #999; }
        }
    </style>
</head>
<body>
    <header>
        <h1>Paul Dirac: Relativistic Quantum Mechanics</h1>
        <p class="subtitle">The Dirac Equation (1928), Gamma Matrices, and Antimatter Prediction</p>
    </header>

    <main>
        <section id="dirac-equation">
            <h2 class="section-title">The Relativistic Wave Equation for the Electron</h2>
            <p>
                In 1928, Paul Adrien Maurice Dirac sought a relativistic wave equation linear in both time and spatial derivatives, overcoming the second-order temporal derivative problem of the Klein-Gordon equation:
            </p>
            <div class="equation-box">
                $$(i\hbar \gamma^\mu \partial_\mu - mc)\psi = 0 \iff i\hbar \frac{\partial \psi}{\partial t} = \left( c \boldsymbol{\alpha} \cdot \mathbf{p} + \beta m c^2 \right)\psi$$
            </div>
            <p>
                To reconcile this linearity with the relativistic mass-shell invariant $E^2 = p^2 c^2 + m^2 c^4$, the coefficients $\gamma^\mu$ must satisfy the Clifford algebra anti-commutation relations:
            </p>
            <div class="equation-box">
                $$\{\gamma^\mu, \gamma^\nu\} \equiv \gamma^\mu \gamma^\nu + \gamma^\nu \gamma^\mu = 2 \eta^{\mu\nu} I_4, \quad \eta = \text{diag}(+1, -1, -1, -1)$$
            </div>
            <p>
                This demands that $\psi$ be a four-component complex spinor, naturally predicting the intrinsic spin-$\frac{1}{2}$ of the electron and its exact gyromagnetic ratio $g = 2$.
            </p>
            <div class="figure-box">
                __GAMMA_SVG__
            </div>
        </section>

        <section id="dirac-sea-antimatter">
            <h2 class="section-title">Negative Energy Solutions and the Dirac Sea</h2>
            <p>
                The relativistic dispersion relation yields two symmetric energy branches:
            </p>
            <div class="equation-box">
                $$E = \pm \sqrt{p^2 c^2 + m^2 c^4}$$
            </div>
            <p>
                Dirac resolved the instability of electrons cascading endlessly into negative energy states by postulating the <em>Dirac Sea</em>: all negative energy states ($E \le -mc^2$) in the vacuum are completely filled according to Pauli's Exclusion Principle.
            </p>
            <p>
                An energetic gamma photon with $h\nu \ge 2mc^2 \approx 1.022\text{ MeV}$ can promote an electron from the negative energy continuum into a positive state, leaving behind a "hole" that behaves as an oppositely charged particle of equal mass - the <strong>positron</strong> ($e^+$), confirmed experimentally by Carl Anderson in 1932.
            </p>
            <div class="figure-box">
                __SEA_SVG__
            </div>
        </section>

        <section id="interactive-dispersion">
            <h2 class="section-title">Interactive Tool: Relativistic Dispersion & Pair Production</h2>
            <div class="interactive-card">
                <div class="interactive-title">Energy Spectrum as a Function of Momentum</div>
                <div class="control-group">
                    <label for="momentum-slider">Momentum $p$ (keV/c):</label>
                    <input type="range" id="momentum-slider" min="0" max="2000" step="10" value="300" oninput="updateDispersion()">
                    <input type="number" id="momentum-num" min="0" max="2000" step="10" value="300" oninput="syncMomentum(this.value)">
                </div>
                <div class="result-panel" id="dispersion-output">
                    Electron Rest Mass $m_e c^2$: 510.998950 keV<br>
                    Positive Branch Energy $E_+$: +592.536 keV<br>
                    Negative Branch Energy $E_-$: -592.536 keV<br>
                    Mass Gap $\Delta E = 2 m_e c^2$: 1021.998 keV (Threshold for Pair Production)
                </div>
            </div>
        </section>
    </main>

    <footer>
        <p>Interactive Edition: The Foundations of Relativistic Quantum Mechanics (1928-1930)</p>
        <p>Mathematical proof engines and visualization generated with pure web-standard vector graphics.</p>
    </footer>

    <script>
        const M_E_KEV = 510.998950;
        function updateDispersion() {
            const p = parseFloat(document.getElementById('momentum-slider').value);
            document.getElementById('momentum-num').value = p;
            calculate(p);
        }
        function syncMomentum(val) {
            const p = parseFloat(val);
            if (!isNaN(p)) {
                document.getElementById('momentum-slider').value = p;
                calculate(p);
            }
        }
        function calculate(p) {
            const energy = Math.sqrt(p * p + M_E_KEV * M_E_KEV);
            const gap = 2 * M_E_KEV;
            document.getElementById('dispersion-output').innerHTML = 
                'Electron Rest Mass $m_e c^2$: ' + M_E_KEV.toFixed(6) + ' keV<br>' +
                'Positive Branch Energy $E_+$: +' + energy.toFixed(3) + ' keV<br>' +
                'Negative Branch Energy $E_-$: -' + energy.toFixed(3) + ' keV<br>' +
                'Mass Gap $\Delta E = 2 m_e c^2$: ' + gap.toFixed(3) + ' keV (Threshold for Pair Production)';
        }
    </script>
</body>
</html>
"""

class DiracBookGenerator:
    """Generates the interactive readable edition of Paul Dirac's Relativistic Quantum Mechanics."""
    def __init__(self):
        self.visualizer = DiracVisualizer()

    def generate_html(self) -> str:
        sea_svg = self.visualizer.render_dirac_sea_svg()
        gamma_svg = self.visualizer.render_gamma_matrices_svg()

        html_out = HTML_TEMPLATE.replace("__GAMMA_SVG__", gamma_svg).replace("__SEA_SVG__", sea_svg)
        return html_out
