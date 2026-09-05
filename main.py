import argparse
import json
import random
import time
import sys
import os
import traceback
from pathlib import Path
from datetime import datetime

script_dir = Path(__file__).resolve().parent

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--env", dest="env", help="decide whether you are in production or development", required=True,
                        type=str.upper, choices=("PROD", "DEV"))
    parser.add_argument("--intensity", dest="intensity", help="decide how intense the benchmark will be", required=True,
                        type=str.upper, choices=("LOW", "MID", "HIGH"))

    return parser.parse_args()


def run_benchmark(env: str, intensity: str):
    output_path = script_dir / "telemetry.json"
    fake_data = {
        "environment": env,
        "intensity": intensity,
        "status": "succeed",
        "games": {
            "Cyberpunk2077": {
                "average_fps": 100,
                "1% low": 85
            },
            "Black Myth Wukong": {
                "average_fps": 88,
                "1% low": 70
            }
        }
    }

    print(f"Running tests in {env} environment.")

    # If intensity is set to high, there is a 30% chance that the test will crash
    if intensity != "HIGH" or random.random() > 0.30:
        time.sleep(5)
        with open(output_path, 'w', encoding="utf-8") as file:
            json.dump(fake_data, file, indent=4)
            file.flush()
            os.fsync(file.fileno())
    else:
        raise Exception("Simulated GPU crash due to high intensity")


if __name__ == "__main__":
    args = get_args()
    try:
        run_benchmark(args.env, args.intensity)
    except Exception as err:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("error_trace.log", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Benchmark failed: {err}\n")
            f.write(traceback.format_exc())
            f.write("\n" + "=" * 60 + "\n")

        sys.exit(1)
