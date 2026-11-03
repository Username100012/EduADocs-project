"""Run the pilot; simulation is default, --live enables real selected providers."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from experiment.pilot_runner import run_pilot


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=ROOT / "experiments/pilot_config.json")
    parser.add_argument("--generator", choices=("gemini", "qwen3"),
                        help="Execute somente este gerador, preservando a configuração original.")
    args = parser.parse_args()
    key = None
    if args.live and args.generator != "qwen3":
        from google_credentials import read_google_key
        key, _ = read_google_key()
        if not key:
            raise SystemExit("Credencial Google ausente; nenhuma chamada realizada.")
    report = run_pilot(args.config, args.output,
                       simulated=not args.live, connection_configs={"gemini": {"api_key": key}},
                       generator_ids=[args.generator] if args.generator else None)
    print(json.dumps(report, indent=2))
