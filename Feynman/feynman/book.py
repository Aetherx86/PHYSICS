import html
from .path_integral import PathIntegralEngine, HBAR, M_ELECTRON
from .visualizer import FeynmanVisualizer

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Richard Feynman: The Path Integral Formulation of Quantum Mechanics - Interactive Edition</title>
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
        header h1 { font-size: 2.5rem; font-weight: 800; letter-spacing: -0.02em; }
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
        label { font-weight: 600; min-width: 220px; }
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
        <h1>Richard Feynman: Space-Time Approach to Non-Relativistic Quantum Mechanics</h1>
        <p class="subtitle">Path Integrals, Sum Over Histories, and Classical Least Action Principle (1948)</p>
    </header>

    <main>
        <section id="path-integral-foundations">
            <h2 class="section-title">The Sum Over Histories & Quantum Propagator</h2>
            <p>
                In 1948, Richard P. Feynman introduced an intuitive and comprehensive formulation of quantum mechanics: rather than following a single deterministic path or solving differential wave equations, a quantum particle traverses <em>all possible geometric histories</em> simultaneously.
            </p>
            <p>
                The probability amplitude $K(b, a) \equiv \langle x_b, t_b \mid x_a, t_a \rangle$ to transition from space-time point $(x_a, t_a)$ to $(x_b, t_b)$ is the functional integral over all unconstrained trajectories $x(t)$:
            </p>
            <div class="equation-box">
                $$K(x_b, t_b; x_a, t_a) = \int \mathcal{D}[x(t)] \exp\left( \frac{i}{\hbar} S[x(t)] \right)$$
            </div>
            <p>
                where $S[x(t)]$ is the classical action functional:
            </p>
            <div class="equation-box">
                $$S[x(t)] = \int_{t_a}^{t_b} L(x, \dot{x}, t) \, dt = \int_{t_a}^{t_b} \left( \frac{1}{2}m \dot{x}^2 - V(x) \right) dt$$
            </div>
            <div class="figure-box">
                __BUNDLE_SVG__
            </div>
        </section>

        <section id="stationary-phase">
            <h2 class="section-title">Principle of Least Action as a Stationary Phase Limit</h2>
            <p>
                Why does classical mechanics follow the principle of least action $\delta S = 0$? In Feynman's formulation, all paths have equal magnitude amplitude $|e^{i S/\hbar}| = 1$. However:
            </p>
            <p>
                When the action $S \gg \hbar$, neighboring non-classical paths differ in action by amounts much larger than $\hbar$. Their quantum phases $\theta = S / \hbar$ rotate violently, causing destructive cancellation when summed over all histories.
            </p>
            <p>
                Only in the immediate infinitesimal neighborhood of the classical stationary path $x_{\text{cl}}(t)$, where the first-order variation vanishes:
            </p>
            <div class="equation-box">
                $$\delta S[x_{\text{cl}}(t)] = 0 \implies \frac{\partial L}{\partial x} - \frac{d}{dt}\left(\frac{\partial L}{\partial \dot{x}}\right) = 0$$
            </div>
            <p>
                do the phase vectors align coherently and add constructively, reproducing the classical trajectory of Hamilton and Newton.
            </p>
            <div class="figure-box">
                __PHASOR_SVG__
            </div>
        </section>

        <section id="interactive-tool">
            <h2 class="section-title">Interactive Tool: Variational Path Action & Phase Phasor</h2>
            <div class="interactive-card">
                <div class="interactive-title">Evaluate Action Deviation and Phase Angle</div>
                <p style="font-size: 0.95rem; color: var(--muted);">
                    Explore how variational sinusoidal deviations $\delta x(t) = A \sin(\pi t / T)$ alter the classical action for an electron ($m_e = 9.109 \times 10^{-31}\text{ kg}$, $x_a = 0$, $x_b = 1\text{ nm}$, $T = 1\text{ fs}$).
                </p>
                <div class="control-group">
                    <label for="amp-slider">Deviation Amplitude $A$ (nm):</label>
                    <input type="range" id="amp-slider" min="-2.0" max="2.0" step="0.05" value="0.0" oninput="updateAction()">
                    <input type="number" id="amp-num" min="-2.0" max="2.0" step="0.05" value="0.0" oninput="syncAmp(this.value)">
                </div>
                <div class="result-panel" id="action-output">
                    Classical Action $S_{\text{cl}}$: 4.5547e-25 J·s<br>
                    Path Action $S[x(t)]$: 4.5547e-25 J·s<br>
                    Excess Action $\Delta S = S - S_{\text{cl}}$: +0.0000e-25 J·s<br>
                    Phase Deviation $\Delta S / \hbar$: 0.0000 rad (Stationary extremum)
                </div>
            </div>
        </section>
    </main>

    <footer>
        <p>Interactive Edition: Richard Feynman's Space-Time Formulation of Quantum Theory (1948)</p>
        <p>Mathematical proof engines and visualization generated with pure web-standard vector graphics.</p>
    </footer>

    <script>
        const M_E = 9.1093837e-31;
        const HBAR = 1.0545718e-34;
        const T_TOTAL = 1.0e-15; // 1 fs
        const DELTA_X = 1.0e-9;   // 1 nm
        const S_CL = 0.5 * M_E * Math.pow(DELTA_X / T_TOTAL, 2) * T_TOTAL;

        function updateAction() {
            const ampNm = parseFloat(document.getElementById('amp-slider').value);
            document.getElementById('amp-num').value = ampNm;
            calc(ampNm);
        }
        function syncAmp(val) {
            const amp = parseFloat(val);
            if (!isNaN(amp)) {
                document.getElementById('amp-slider').value = amp;
                calc(amp);
            }
        }
        function calc(ampNm) {
            const A = ampNm * 1.0e-9;
            // Delta S for sinusoidal deviation A*sin(pi*t/T):
            // v(t) = v_cl + A*(pi/T)*cos(pi*t/T)
            // Delta S = int 1/2 m (2*v_cl*A*pi/T*cos(...) + A^2*pi^2/T^2*cos^2(...)) dt
            // First term integrates to 0 over [0, T].
            // Second term integrates to 1/2 * m * A^2 * pi^2 / (2 * T).
            const deltaS = 0.25 * M_E * Math.pow(A * Math.PI, 2) / T_TOTAL;
            const totalS = S_CL + deltaS;
            const phaseDev = deltaS / HBAR;

            document.getElementById('action-output').innerHTML =
                'Classical Action $S_{\\text{cl}}$: ' + S_CL.toExponential(4) + ' J·s<br>' +
                'Path Action $S[x(t)]$: ' + totalS.toExponential(4) + ' J·s<br>' +
                'Excess Action $\\Delta S = S - S_{\\text{cl}}$: +' + deltaS.toExponential(4) + ' J·s<br>' +
                'Phase Deviation $\\Delta S / \\hbar$: ' + phaseDev.toFixed(4) + ' rad' + (Math.abs(phaseDev) < 1e-4 ? ' (Stationary extremum)' : '');
        }
    </script>
</body>
</html>
"""

class FeynmanBookGenerator:
    """Generates the interactive readable edition of Richard Feynman's Path Integral Formulation."""
    def __init__(self):
        self.visualizer = FeynmanVisualizer()

    def generate_html(self) -> str:
        bundle_svg = self.visualizer.render_path_bundle_svg()
        phasor_svg = self.visualizer.render_phasor_interference_svg()

        html_out = HTML_TEMPLATE.replace("__BUNDLE_SVG__", bundle_svg).replace("__PHASOR_SVG__", phasor_svg)
        return html_out
