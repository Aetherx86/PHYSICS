import argparse
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from .book import SchrodingerBookGenerator
from .wave_mechanics import HBAR, M_ELECTRON, PotentialWellSolver, HarmonicOscillatorWavefunctions

class BookHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        generator = SchrodingerBookGenerator()
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
    print("=== Erwin Schrödinger: Wave Mechanics Interactive Server ===")
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
    gen = SchrodingerBookGenerator()
    content = gen.generate_html()
    _export_output(content, args.output, label="Schrodinger Wave Mechanics")

def cmd_spectrum(args):
    solver = PotentialWellSolver(length=args.length * 1.0e-9)
    print(f"=== Infinite Square Well Spectrum (L = {args.length:.2f} nm, Electron Mass) ===")
    print(f"{'State n':<10} {'Energy (Joules)':<22} {'Energy (eV)':<12} {'Ratio E_n / E_1'}")
    print("-" * 60)
    e1 = solver.energy_eigenvalue(1)
    for n in range(1, args.states + 1):
        en = solver.energy_eigenvalue(n)
        ev = en / 1.602176634e-19
        ratio = en / e1
        print(f"n = {n:<6} {en:<22.6e} {ev:<12.3f} {ratio:.1f}")

def main():
    parser = argparse.ArgumentParser(
        prog="schrodinger",
        description="Erwin Schrödinger: Wave Mechanics & Quantized Energy Spectrum Suite",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_serve = subparsers.add_parser("serve", help="Launch interactive web reader")
    p_serve.add_argument("--port", type=int, default=8080, help="Port to bind (default: 8080)")
    p_serve.set_defaults(func=cmd_serve)

    p_exp = subparsers.add_parser("export", help="Export readable HTML or publication PDF")
    p_exp.add_argument("--out", dest="output", default="schrodinger_wave_mechanics.html", help="Target output file (.html or .pdf)")
    p_exp.set_defaults(func=cmd_export)

    p_spec = subparsers.add_parser("well-spectrum", help="Calculate square potential well energy eigenvalues")
    p_spec.add_argument("--length", type=float, default=1.0, help="Well width in nanometers (default: 1.0 nm)")
    p_spec.add_argument("--states", type=int, default=5, help="Number of quantum states to compute (default: 5)")
    p_spec.set_defaults(func=cmd_spectrum)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
