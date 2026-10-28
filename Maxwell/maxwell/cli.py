import argparse
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from .book import MaxwellBookGenerator
from .electrodynamics import EPSILON_0, MU_0, C_EXACT, ElectrodynamicsEngine, MAXWELL_EQUATIONS

class BookHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        generator = MaxwellBookGenerator()
        html_content = generator.generate_html().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html_content)))
        self.end_headers()
        self.wfile.write(html_content)

    def log_message(self, format, *args):
        pass

def _export_output(content: str, out_file: str, label: str = "book"):
    import os
    import shutil
    import subprocess
    import tempfile

    if out_file.lower().endswith(".pdf"):
        chrome_candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            shutil.which("google-chrome"),
            shutil.which("chromium"),
            shutil.which("chromium-browser"),
        ]
        chrome_bin = next((b for b in chrome_candidates if b and os.path.exists(b)), None)
        if chrome_bin:
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            try:
                cmd = [
                    chrome_bin,
                    "--headless",
                    "--disable-gpu",
                    "--run-all-compositor-stages-before-draw",
                    f"--print-to-pdf={out_file}",
                    tmp_path,
                ]
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                size = os.path.getsize(out_file)
                print(f"[OK] Exported interactive {label} to PDF: {out_file} ({size:,} bytes)")
                return
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        else:
            print("[INFO] Headless Chrome not found for direct PDF rasterization; exporting HTML publication instead.")
            out_file = out_file[:-4] + ".html"

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Exported interactive {label} to {out_file} ({len(content):,} bytes)")

def cmd_serve(args):
    server = HTTPServer(("127.0.0.1", args.port), BookHTTPHandler)
    print("=== James Clerk Maxwell: Electrodynamics Interactive Server ===")
    print(f"Listening on http://localhost:{args.port}/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("\nServer shut down.")

def cmd_export(args):
    gen = MaxwellBookGenerator()
    content = gen.generate_html()
    _export_output(content, args.output, label="Maxwell Electrodynamics")

def cmd_wave_speed(args):
    c = ElectrodynamicsEngine.calculate_wave_speed(EPSILON_0, MU_0)
    print("=== Maxwell Electromagnetic Wave Speed Derivation ===")
    print(f"Vacuum Permittivity eps_0: {EPSILON_0:.10e} F/m")
    print(f"Vacuum Permeability mu_0:  {MU_0:.10e} N/A^2")
    print(f"Calculated c = 1/sqrt(eps_0 * mu_0): {c:,.3f} m/s")
    print(f"SI Defined c:                      {C_EXACT:,.3f} m/s")
    print(f"Relative Difference:               {abs(c - C_EXACT) / C_EXACT:.2e}")

def cmd_equations(args):
    print("=== The Four Maxwell Equations ===")
    for i, eq in enumerate(MAXWELL_EQUATIONS, 1):
        print(f"\n{i}. {eq.name}")
        print(f"   Differential: {eq.differential_form}")
        print(f"   Integral:     {eq.integral_form}")
        print(f"   Concept:      {eq.physical_meaning}")

def main():
    parser = argparse.ArgumentParser(
        prog="maxwell",
        description="James Clerk Maxwell: Classical Electrodynamics & Wave Suite",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_serve = subparsers.add_parser("serve", help="Launch interactive web reader")
    p_serve.add_argument("--port", type=int, default=8080, help="Port to bind (default: 8080)")
    p_serve.set_defaults(func=cmd_serve)

    p_exp = subparsers.add_parser("export", help="Export readable HTML or publication PDF")
    p_exp.add_argument("--out", dest="output", default="maxwell_electrodynamics.html", help="Target output file (.html or .pdf)")
    p_exp.set_defaults(func=cmd_export)

    p_speed = subparsers.add_parser("wave-speed", help="Compute speed of light from vacuum constants")
    p_speed.set_defaults(func=cmd_wave_speed)

    p_eqs = subparsers.add_parser("equations", help="Display differential and integral forms of Maxwell equations")
    p_eqs.set_defaults(func=cmd_equations)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
