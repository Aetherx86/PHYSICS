import argparse
import sys
import os
import http.server
import socketserver
import subprocess
from .book import PlanckBookGenerator
from .blackbody import (
    PlanckBlackbodyEngine,
    B_WIEN,
    SIGMA_SB
)

def main():
    parser = argparse.ArgumentParser(description="Max Planck: Blackbody Radiation & Quantum Suite")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # serve command
    serve_parser = subparsers.add_parser("serve", help="Serve the interactive readable book locally")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to bind server (default: 8000)")

    # export command
    export_parser = subparsers.add_parser("export", help="Export book to standalone HTML or PDF")
    export_parser.add_argument("--out", type=str, default="Planck_Blackbody_Radiation.html", help="Output file path (.html or .pdf)")

    # radiance command
    rad_parser = subparsers.add_parser("radiance", help="Calculate Planck spectral radiance")
    rad_parser.add_argument("--temp", type=float, default=5778.0, help="Cavity temperature in Kelvin (default: Sun 5778 K)")
    rad_parser.add_argument("--wavelength", type=float, default=500.0e-9, help="Wavelength in meters (default: 500 nm)")

    # wien command
    wien_parser = subparsers.add_parser("wien", help="Calculate Wien displacement law peak and Stefan-Boltzmann exitance")
    wien_parser.add_argument("--temp", type=float, default=5778.0, help="Cavity temperature in Kelvin (default: Sun 5778 K)")

    args = parser.parse_args()

    if args.command == "radiance":
        b_planck = PlanckBlackbodyEngine.planck_spectral_radiance(args.wavelength, args.temp)
        b_rj = PlanckBlackbodyEngine.rayleigh_jeans_radiance(args.wavelength, args.temp)
        print(f"Blackbody Spectral Radiance at T = {args.temp:.1f} K, λ = {args.wavelength * 1e9:.1f} nm:")
        print(f"  Planck Quantum Radiance:     {b_planck:.4e} W / (m^3 * sr)")
        print(f"  Rayleigh-Jeans Classical:    {b_rj:.4e} W / (m^3 * sr)")
        ratio = (b_rj / b_planck) if b_planck > 0 else float('inf')
        print(f"  Classical Overprediction:    {ratio:.3f}x")

    elif args.command == "wien":
        peak_lambda = PlanckBlackbodyEngine.wien_peak_wavelength(args.temp)
        j_star = PlanckBlackbodyEngine.stefan_boltzmann_exitance(args.temp)
        print(f"Thermal Radiation Properties at T = {args.temp:.1f} K:")
        print(f"  Wien Peak Wavelength λ_max:  {peak_lambda * 1e9:.2f} nm")
        print(f"  Stefan-Boltzmann Exitance:   {j_star:.4e} W / m^2")

    elif args.command == "export":
        gen = PlanckBookGenerator()
        html_content = gen.generate_html()

        if args.out.endswith(".pdf"):
            temp_html = "/tmp/_planck_temp.html"
            with open(temp_html, "w", encoding="utf-8") as f:
                f.write(html_content)

            chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            if not os.path.exists(chrome_path):
                print(f"[ERROR] Chrome binary not found at {chrome_path}", file=sys.stderr)
                sys.exit(1)

            cmd = [
                chrome_path,
                "--headless",
                "--disable-gpu",
                f"--print-to-pdf={os.path.abspath(args.out)}",
                temp_html
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode == 0:
                print(f"[OK] Exported interactive Planck Blackbody Radiation to PDF: {args.out} ({os.path.getsize(args.out):,} bytes)")
            else:
                print(f"[ERROR] Failed to generate PDF: {res.stderr.decode()}", file=sys.stderr)
                sys.exit(1)
        else:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"[OK] Exported interactive Planck Blackbody Radiation to {args.out} ({os.path.getsize(args.out):,} bytes)")

    elif args.command == "serve":
        gen = PlanckBookGenerator()
        html_content = gen.generate_html()
        temp_dir = "/tmp/planck_server"
        os.makedirs(temp_dir, exist_ok=True)
        index_path = os.path.join(temp_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        os.chdir(temp_dir)
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", args.port), handler) as httpd:
            print(f"[OK] Serving Planck Interactive Edition on http://localhost:{args.port} (Ctrl+C to stop)")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n[OK] Server stopped.")

if __name__ == "__main__":
    main()
