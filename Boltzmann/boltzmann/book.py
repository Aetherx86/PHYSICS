import html
from .statistical_mechanics import BoltzmannStatisticalEngine, M_N2, K_B
from .visualizer import BoltzmannVisualizer

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ludwig Boltzmann: Statistical Mechanics, Entropy & Kinetic Gas Theory - Interactive Edition</title>
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
        label { font-weight: 600; min-width: 200px; }
        input[type="range"] { flex: 1; min-width: 200px; }
        input[type="number"], select {
            width: 140px;
            padding: 0.4rem 0.6rem;
            border: 1px solid var(--border);
            border-radius: 4px;
            background: #ffffff;
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
        <h1>Ludwig Boltzmann: Statistical Mechanics</h1>
        <p class="subtitle">Entropy Equation S = k_B ln Ω, Maxwell-Boltzmann Distribution, and H-Theorem (1877)</p>
    </header>

    <main>
        <section id="entropy-section">
            <h2 class="section-title">The Statistical Origin of Thermodynamic Entropy</h2>
            <p>
                In 1877, Ludwig Boltzmann bridged the microscopic realm of atomic motion with the macroscopic laws of thermodynamics by demonstrating that entropy $S$ is a direct statistical measure of microscopic multiplicity $\Omega$:
            </p>
            <div class="equation-box">
                $$S = k_B \ln \Omega$$
            </div>
            <p>
                Here $\Omega$ is the number of distinct microstates consistent with a given macroscopic thermodynamic state $(E, V, N)$. Because thermodynamic entropy is strictly extensive ($S_{A+B} = S_A + S_B$) while microstate configurations multiply ($\Omega_{A+B} = \Omega_A \cdot \Omega_B$), the logarithm is uniquely required.
            </p>
            <div class="figure-box">
                __ENTROPY_SVG__
            </div>
        </section>

        <section id="distribution-section">
            <h2 class="section-title">The Maxwell-Boltzmann Molecular Speed Distribution</h2>
            <p>
                By maximizing the entropy functional under constraints of fixed particle number $N$ and total energy $E$, Boltzmann derived the continuous equilibrium distribution for molecular velocities in three dimensions:
            </p>
            <div class="equation-box">
                $$f(v) \, dv = 4\pi \left(\frac{m}{2\pi k_B T}\right)^{3/2} v^2 \exp\left(-\frac{m v^2}{2 k_B T}\right) dv$$
            </div>
            <p>
                From this probability density function, the three fundamental statistical speeds emerge in rigorous hierarchical order:
            </p>
            <div class="equation-box">
                $$v_p = \sqrt{\frac{2 k_B T}{m}} < \langle v \rangle = \sqrt{\frac{8 k_B T}{\pi m}} < v_{\text{rms}} = \sqrt{\frac{3 k_B T}{m}}$$
            </div>
            <p>
                Each molecule carries an average translational kinetic energy of $\langle E_k \rangle = \frac{1}{2} m v_{\text{rms}}^2 = \frac{3}{2} k_B T$, perfectly proving the classical equipartition theorem of energy.
            </p>
            <div class="figure-box">
                __MAXWELL_SVG__
            </div>
        </section>

        <section id="interactive-tool">
            <h2 class="section-title">Interactive Tool: Gas Speed Distribution & Thermal Energy</h2>
            <div class="interactive-card">
                <div class="interactive-title">Real-Time Characteristic Velocity Calculator</div>
                <div class="control-group">
                    <label for="temp-slider">Temperature $T$ (Kelvin):</label>
                    <input type="range" id="temp-slider" min="50" max="1500" step="10" value="300" oninput="updateTemp()">
                    <input type="number" id="temp-num" min="50" max="1500" step="10" value="300" oninput="syncTemp(this.value)">
                </div>
                <div class="control-group">
                    <label for="gas-select">Molecular Species:</label>
                    <select id="gas-select" onchange="updateTemp()">
                        <option value="0.0280134">Nitrogen (N2, 28.0 g/mol)</option>
                        <option value="0.0040026">Helium (He, 4.00 g/mol)</option>
                        <option value="0.039948">Argon (Ar, 39.9 g/mol)</option>
                        <option value="0.031999">Oxygen (O2, 32.0 g/mol)</option>
                    </select>
                </div>
                <div class="result-panel" id="boltzmann-output">
                    Most Probable Speed $v_p$: 422.0 m/s<br>
                    Mean Speed $\langle v \rangle$: 476.2 m/s<br>
                    Root-Mean-Square Speed $v_{\text{rms}}$: 516.8 m/s<br>
                    Mean Kinetic Energy $\langle E_k \rangle$: 6.213e-21 J (38.78 meV)
                </div>
            </div>
        </section>
    </main>

    <footer>
        <p>Interactive Edition: Ludwig Boltzmann's Kinetic Theory of Gases & Statistical Entropy (1877)</p>
        <p>Mathematical proof engines and visualization generated with pure web-standard vector graphics.</p>
    </footer>

    <script>
        const K_B = 1.380649e-23;
        const N_A = 6.02214076e23;

        function updateTemp() {
            const T = parseFloat(document.getElementById('temp-slider').value);
            document.getElementById('temp-num').value = T;
            calculate(T);
        }
        function syncTemp(val) {
            const T = parseFloat(val);
            if (!isNaN(T)) {
                document.getElementById('temp-slider').value = T;
                calculate(T);
            }
        }
        function calculate(T) {
            const molarMass = parseFloat(document.getElementById('gas-select').value);
            const m = molarMass / N_A;

            const vp = Math.sqrt(2 * K_B * T / m);
            const vavg = Math.sqrt(8 * K_B * T / (Math.PI * m));
            const vrms = Math.sqrt(3 * K_B * T / m);
            const eKin = 1.5 * K_B * T;
            const eKinMev = (eKin / 1.602176634e-19) * 1000;

            document.getElementById('boltzmann-output').innerHTML = 
                'Most Probable Speed $v_p$: ' + vp.toFixed(1) + ' m/s<br>' +
                'Mean Speed $\\langle v \\rangle$: ' + vavg.toFixed(1) + ' m/s<br>' +
                'Root-Mean-Square Speed $v_{\\text{rms}}$: ' + vrms.toFixed(1) + ' m/s<br>' +
                'Mean Kinetic Energy $\\langle E_k \\rangle$: ' + eKin.toExponential(3) + ' J (' + eKinMev.toFixed(2) + ' meV)';
        }
    </script>
</body>
</html>
"""

class BoltzmannBookGenerator:
    """Generates the interactive readable edition of Ludwig Boltzmann's Statistical Mechanics."""
    def __init__(self):
        self.visualizer = BoltzmannVisualizer()

    def generate_html(self) -> str:
        maxwell_svg = self.visualizer.render_maxwell_boltzmann_svg()
        entropy_svg = self.visualizer.render_entropy_microstates_svg()

        html_out = HTML_TEMPLATE.replace("__MAXWELL_SVG__", maxwell_svg).replace("__ENTROPY_SVG__", entropy_svg)
        return html_out
