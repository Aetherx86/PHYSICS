import html
from .blackbody import PlanckBlackbodyEngine, H_PLANCK, C_LIGHT, K_BOLTZMANN, B_WIEN, SIGMA_SB
from .visualizer import PlanckVisualizer

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Max Planck: The Quantum of Action & Blackbody Radiation Law - Interactive Edition</title>
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
        <h1>Max Planck: The Quantum of Action</h1>
        <p class="subtitle">Blackbody Radiation Law, Ultraviolet Catastrophe Resolution, and Quanta E = hν (1900)</p>
    </header>

    <main>
        <section id="planck-law">
            <h2 class="section-title">The Blackbody Radiation Law & Spectral Radiance</h2>
            <p>
                In December 1900, Max Planck presented his landmark solution to the cavity radiation puzzle. Classical electrodynamics and the equipartition theorem predicted that a blackbody cavity would emit infinite power at short wavelengths - a catastrophic breakdown known as the <em>Ultraviolet Catastrophe</em>:
            </p>
            <div class="equation-box">
                $$B_{\lambda, \text{RJ}}(\lambda, T) = \frac{2 c k_B T}{\lambda^4} \xrightarrow{\lambda \to 0} \infty \quad \text{(Rayleigh-Jeans Divergence)}$$
            </div>
            <p>
                Planck realized that continuous energy exchange must be replaced by discrete packets - <strong>quanta of action</strong> $E = n h \nu$. This quantum postulate leads to the exact, finite blackbody spectral radiance formula:
            </p>
            <div class="equation-box">
                $$B_\lambda(\lambda, T) = \frac{2 h c^2}{\lambda^5} \frac{1}{\exp\left(\frac{h c}{\lambda k_B T}\right) - 1}$$
            </div>
            <p>
                At short wavelengths ($h c / \lambda \gg k_B T$), the exponential denominator dominates and suppresses radiation to zero, preventing the UV catastrophe while matching precision cavity measurements.
            </p>
            <div class="figure-box">
                __CURVES_SVG__
            </div>
        </section>

        <section id="quantization-section">
            <h2 class="section-title">Energy Quantization and Limiting Laws</h2>
            <p>
                Planck's law reconciles both empirical radiation regimes and reproduces the foundational thermodynamic laws as exact mathematical limits:
            </p>
            <div class="equation-box">
                $$\lambda_{\max} \cdot T = b \approx 2.89777 \times 10^{-3} \text{ m}\cdot\text{K} \quad \text{(Wien's Displacement Law)}$$
            </div>
            <p>
                Integrating over the entire electromagnetic spectrum yields the Stefan-Boltzmann law for total radiant exitance $j^*$:
            </p>
            <div class="equation-box">
                $$j^* = \int_0^\infty \pi B_\lambda(\lambda, T) \, d\lambda = \frac{2 \pi^5 k_B^4}{15 c^2 h^3} T^4 = \sigma T^4$$
            </div>
            <div class="figure-box">
                __QUANTUM_SVG__
            </div>
        </section>

        <section id="interactive-tool">
            <h2 class="section-title">Interactive Tool: Blackbody Spectrum & Thermal Radiance</h2>
            <div class="interactive-card">
                <div class="interactive-title">Radiation Parameter Calculator</div>
                <div class="control-group">
                    <label for="temp-slider">Cavity Temperature $T$ (Kelvin):</label>
                    <input type="range" id="temp-slider" min="1000" max="8000" step="50" value="5778" oninput="updateTemp()">
                    <input type="number" id="temp-num" min="1000" max="8000" step="50" value="5778" oninput="syncTemp(this.value)">
                </div>
                <div class="result-panel" id="planck-output">
                    Wien Peak Wavelength $\lambda_{\max}$: 501.5 nm (Visible Green)<br>
                    Peak Spectral Radiance $B_{\lambda,\max}$: 2.632e+13 W/(m³·sr)<br>
                    Rayleigh-Jeans at Peak: 3.864e+13 W/(m³·sr) (Classical overprediction)<br>
                    Stefan-Boltzmann Total Exitance $j^*$: 6.316e+07 W/m²
                </div>
            </div>
        </section>
    </main>

    <footer>
        <p>Interactive Edition: Max Planck's Quantum Theory of Blackbody Radiation (1900)</p>
        <p>Mathematical proof engines and visualization generated with pure web-standard vector graphics.</p>
    </footer>

    <script>
        const H = 6.62607015e-34;
        const C = 299792458;
        const K_B = 1.380649e-23;
        const B = 2.897771955e-3;
        const SIGMA = 5.670374e-8;

        function updateTemp() {
            const T = parseFloat(document.getElementById('temp-slider').value);
            document.getElementById('temp-num').value = T;
            calc(T);
        }
        function syncTemp(val) {
            const T = parseFloat(val);
            if (!isNaN(T)) {
                document.getElementById('temp-slider').value = T;
                calc(T);
            }
        }
        function calc(T) {
            const lambdaMaxM = B / T;
            const lambdaMaxNm = lambdaMaxM * 1e9;

            // Spectral color descriptor
            let colorDesc = "";
            if (lambdaMaxNm < 380) colorDesc = " (Ultraviolet)";
            else if (lambdaMaxNm <= 450) colorDesc = " (Violet/Blue)";
            else if (lambdaMaxNm <= 495) colorDesc = " (Cyan)";
            else if (lambdaMaxNm <= 570) colorDesc = " (Visible Green)";
            else if (lambdaMaxNm <= 590) colorDesc = " (Yellow)";
            else if (lambdaMaxNm <= 750) colorDesc = " (Red)";
            else colorDesc = " (Infrared)";

            // Radiance at peak
            const exponent = (H * C) / (lambdaMaxM * K_B * T);
            const planckPeak = (2 * H * C * C / Math.pow(lambdaMaxM, 5)) / (Math.exp(exponent) - 1);
            const rjPeak = (2 * C * K_B * T) / Math.pow(lambdaMaxM, 4);
            const jStar = SIGMA * Math.pow(T, 4);

            document.getElementById('planck-output').innerHTML = 
                'Wien Peak Wavelength $\\lambda_{\\max}$: ' + lambdaMaxNm.toFixed(1) + ' nm' + colorDesc + '<br>' +
                'Peak Spectral Radiance $B_{\\lambda,\\max}$: ' + planckPeak.toExponential(3) + ' W/(m³·sr)<br>' +
                'Rayleigh-Jeans at Peak: ' + rjPeak.toExponential(3) + ' W/(m³·sr) (Classical overprediction)<br>' +
                'Stefan-Boltzmann Total Exitance $j^*$: ' + jStar.toExponential(3) + ' W/m²';
        }
    </script>
</body>
</html>
"""

class PlanckBookGenerator:
    """Generates the interactive readable edition of Max Planck's Quantum of Action & Blackbody Radiation."""
    def __init__(self):
        self.visualizer = PlanckVisualizer()

    def generate_html(self) -> str:
        curves_svg = self.visualizer.render_blackbody_curves_svg()
        quantum_svg = self.visualizer.render_energy_quantization_svg()

        html_out = HTML_TEMPLATE.replace("__CURVES_SVG__", curves_svg).replace("__QUANTUM_SVG__", quantum_svg)
        return html_out
