import argparse
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from .book import DiracBookGenerator
from .relativistic_qm import E_REST_ELECTRON_EV, RelativisticDiracEngine, get_dirac_gamma_matrices

class BookHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        generator = DiracBookGenerator()
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
    print("=== Paul Dirac: Relativistic Quantum Mechanics Interactive Server ===")
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
    gen = DiracBookGenerator()
    content = gen.generate_html()
    _export_output(content, args.output, label="Dirac Relativistic Quantum Mechanics")

def cmd_clifford(args):
    print("=== Clifford Algebra Anti-Commutation Check: {gamma^mu, gamma^nu} = 2 eta^(mu nu) I_4 ===")
    results = RelativisticDiracEngine.verify_clifford_algebra()
    all_ok = True
    for mu, nu, ok in results:
        status = "PASSED" if ok else "FAILED"
        if not ok:
            all_ok = False
        print(f"  {{gamma^{mu}, gamma^{nu}}} -> {status}")
    print(f"\nOverall Result: {'All 16 Clifford relations verified successfully!' if all_ok else 'Verification failed.'}")

def cmd_dispersion(args):
    p = args.momentum
    ep, em = RelativisticDiracEngine.dispersion_energy(p)
    print(f"=== Dirac Relativistic Dispersion for Electron (Rest Energy: {E_REST_ELECTRON_EV/1000:.2f} keV) ===")
    print(f"Momentum p*c:               {p/1000:.2f} keV")
    print(f"Positive Energy E+ (e-):    +{ep/1000:.2f} keV")
    print(f"Negative Energy E- (e+):    {em/1000:.2f} keV")
    print(f"Total Mass Gap 2*m*c^2:     {(2 * E_REST_ELECTRON_EV)/1000:.2f} keV")

def main():
    parser = argparse.ArgumentParser(
        prog="dirac",
        description="Paul Dirac: Relativistic Quantum Mechanics, Spinors & Antimatter Suite",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_serve = subparsers.add_parser("serve", help="Launch interactive web reader")
    p_serve.add_argument("--port", type=int, default=8080, help="Port to bind (default: 8080)")
    p_serve.set_defaults(func=cmd_serve)

    p_exp = subparsers.add_parser("export", help="Export readable HTML or publication PDF")
    p_exp.add_argument("--out", dest="output", default="dirac_relativistic_qm.html", help="Target output file (.html or .pdf)")
    p_exp.set_defaults(func=cmd_export)

    p_clifford = subparsers.add_parser("clifford", help="Verify all 16 Clifford anticommutator relations")
    p_clifford.set_defaults(func=cmd_clifford)

    p_disp = subparsers.add_parser("dispersion", help="Compute positive and negative energy eigenvalues")
    p_disp.add_argument("--momentum", type=float, default=300000.0, help="Momentum p*c in eV (default: 300,000 eV)")
    p_disp.set_defaults(func=cmd_dispersion)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
