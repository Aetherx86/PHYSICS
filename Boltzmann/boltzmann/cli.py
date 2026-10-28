import argparse
import sys
import os
import http.server
import socketserver
import subprocess
from .book import BoltzmannBookGenerator
from .statistical_mechanics import BoltzmannStatisticalEngine, K_B, M_N2

def main():
    parser = argparse.ArgumentParser(description="Ludwig Boltzmann: Statistical Mechanics Suite")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # serve command
    serve_parser = subparsers.add_parser("serve", help="Serve the interactive readable book locally")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to bind server (default: 8000)")

    # export command
    export_parser = subparsers.add_parser("export", help="Export book to standalone HTML or PDF")
    export_parser.add_argument("--out", type=str, default="Boltzmann_Statistical_Mechanics.html", help="Output file path (.html or .pdf)")

    # speeds command
    speed_parser = subparsers.add_parser("speeds", help="Calculate characteristic speeds (vp, v_mean, v_rms)")
    speed_parser.add_argument("--temp", type=float, default=300.0, help="Temperature in Kelvin (default: 300 K)")
    speed_parser.add_argument("--mass", type=float, default=M_N2, help="Molecular mass in kg (default: N2 mass)")

    # entropy command
    ent_parser = subparsers.add_parser("entropy", help="Calculate Boltzmann entropy S = k_B * ln(Omega)")
    ent_parser.add_argument("--omega", type=float, default=1.0e20, help="Microstates multiplicity Omega")

    args = parser.parse_args()

    if args.command == "speeds":
        speeds = BoltzmannStatisticalEngine.characteristic_speeds(args.temp, args.mass)
        e_kin = BoltzmannStatisticalEngine.mean_kinetic_energy(args.temp)
        print(f"Maxwell-Boltzmann Molecular Speeds at T = {args.temp:.1f} K:")
        print(f"  Molecular Mass:          {args.mass:.4e} kg")
        print(f"  Most Probable Speed v_p: {speeds['v_probable']:.2f} m/s")
        print(f"  Mean Speed <v>:          {speeds['v_mean']:.2f} m/s")
        print(f"  Root-Mean-Square v_rms:  {speeds['v_rms']:.2f} m/s")
        print(f"  Mean Kinetic Energy:     {e_kin:.4e} J ({(e_kin / 1.602176634e-19) * 1000:.2f} meV)")

    elif args.command == "entropy":
        s_val = BoltzmannStatisticalEngine.entropy(args.omega)
        print("Boltzmann Entropy Evaluation:")
        print(f"  Microstates Omega: {args.omega:.4e}")
        print(f"  Entropy S:         {s_val:.6e} J / K")

    elif args.command == "export":
        gen = BoltzmannBookGenerator()
        html_content = gen.generate_html()

        if args.out.endswith(".pdf"):
            temp_html = "/tmp/_boltzmann_temp.html"
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
                print(f"[OK] Exported interactive Boltzmann Statistical Mechanics to PDF: {args.out} ({os.path.getsize(args.out):,} bytes)")
            else:
                print(f"[ERROR] Failed to generate PDF: {res.stderr.decode()}", file=sys.stderr)
                sys.exit(1)
        else:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"[OK] Exported interactive Boltzmann Statistical Mechanics to {args.out} ({os.path.getsize(args.out):,} bytes)")

    elif args.command == "serve":
        gen = BoltzmannBookGenerator()
        html_content = gen.generate_html()
        temp_dir = "/tmp/boltzmann_server"
        os.makedirs(temp_dir, exist_ok=True)
        index_path = os.path.join(temp_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        os.chdir(temp_dir)
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", args.port), handler) as httpd:
            print(f"[OK] Serving Boltzmann Interactive Edition on http://localhost:{args.port} (Ctrl+C to stop)")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n[OK] Server stopped.")

if __name__ == "__main__":
    main()
