import argparse
import sys
import os
import http.server
import socketserver
import subprocess
from .book import FeynmanBookGenerator
from .path_integral import PathIntegralEngine, HBAR, M_ELECTRON

def main():
    parser = argparse.ArgumentParser(description="Richard Feynman: Path Integrals & Quantum Action Suite")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # serve command
    serve_parser = subparsers.add_parser("serve", help="Serve the interactive readable book locally")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to bind server (default: 8000)")

    # export command
    export_parser = subparsers.add_parser("export", help="Export book to standalone HTML or PDF")
    export_parser.add_argument("--out", type=str, default="Feynman_Path_Integrals.html", help="Output file path (.html or .pdf)")

    # action command
    action_parser = subparsers.add_parser("action", help="Calculate classical action for a free particle")
    action_parser.add_argument("--mass", type=float, default=M_ELECTRON, help="Mass in kg")
    action_parser.add_argument("--xa", type=float, default=0.0, help="Start position in meters")
    action_parser.add_argument("--xb", type=float, default=1.0e-9, help="End position in meters")
    action_parser.add_argument("--time", type=float, default=1.0e-15, help="Time duration in seconds")

    # propagate command
    prop_parser = subparsers.add_parser("propagate", help="Calculate analytical free propagator")
    prop_parser.add_argument("--mass", type=float, default=M_ELECTRON, help="Mass in kg")
    prop_parser.add_argument("--xa", type=float, default=0.0, help="Start position in meters")
    prop_parser.add_argument("--xb", type=float, default=1.0e-9, help="End position in meters")
    prop_parser.add_argument("--time", type=float, default=1.0e-15, help="Time duration in seconds")

    args = parser.parse_args()

    if args.command == "action":
        action = PathIntegralEngine.classical_action_free_particle(args.mass, args.xa, args.xb, args.time)
        print("Classical Action Evaluation:")
        print(f"  Mass:       {args.mass:.6e} kg")
        print(f"  Interval:   [{args.xa:.3e}, {args.xb:.3e}] m")
        print(f"  Duration:   {args.time:.3e} s")
        print(f"  Action S:   {action:.6e} J*s")
        print(f"  S / hbar:   {action / HBAR:.4f} rad")

    elif args.command == "propagate":
        k_val = PathIntegralEngine.free_particle_propagator_analytical(args.mass, args.xa, args.xb, args.time)
        print("Free Particle Propagator K(x_b, T; x_a, 0):")
        print(f"  Complex Amplitude: {k_val.real:.4e} + {k_val.imag:.4e}j")
        print(f"  Modulus |K|:       {abs(k_val):.4e}")

    elif args.command == "export":
        gen = FeynmanBookGenerator()
        html_content = gen.generate_html()

        if args.out.endswith(".pdf"):
            temp_html = "/tmp/_feynman_temp.html"
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
                print(f"[OK] Exported interactive Feynman Path Integrals to PDF: {args.out} ({os.path.getsize(args.out):,} bytes)")
            else:
                print(f"[ERROR] Failed to generate PDF: {res.stderr.decode()}", file=sys.stderr)
                sys.exit(1)
        else:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"[OK] Exported interactive Feynman Path Integrals to {args.out} ({os.path.getsize(args.out):,} bytes)")

    elif args.command == "serve":
        gen = FeynmanBookGenerator()
        html_content = gen.generate_html()
        temp_dir = "/tmp/feynman_server"
        os.makedirs(temp_dir, exist_ok=True)
        index_path = os.path.join(temp_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        os.chdir(temp_dir)
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", args.port), handler) as httpd:
            print(f"[OK] Serving Feynman Interactive Edition on http://localhost:{args.port} (Ctrl+C to stop)")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n[OK] Server stopped.")

if __name__ == "__main__":
    main()
