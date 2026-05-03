#!/usr/bin/env python3
"""Sample amdgpu PPT power telemetry as CSV.

This records the kernel-exposed amdgpu power counter, not wall power. Use it
for same-machine relative runs unless validated against an external meter.
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def find_amdgpu_power() -> tuple[Path, str]:
    candidates = []
    for name_file in Path("/sys/class/hwmon").glob("hwmon*/name"):
        try:
            if name_file.read_text(encoding="utf-8").strip() != "amdgpu":
                continue
        except OSError:
            continue
        hwmon = name_file.parent
        for metric in ("power1_average", "power1_input"):
            path = hwmon / metric
            if path.exists():
                label = "PPT"
                label_path = hwmon / "power1_label"
                if label_path.exists():
                    try:
                        label = label_path.read_text(encoding="utf-8").strip()
                    except OSError:
                        pass
                candidates.append((path, label))
    if not candidates:
        raise SystemExit("No amdgpu power1_average/power1_input telemetry found")
    return candidates[0]


def read_watts(path: Path) -> float:
    microwatts = int(path.read_text(encoding="utf-8").strip())
    return microwatts / 1_000_000


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=60.0, help="sample duration")
    parser.add_argument("--interval", type=float, default=1.0, help="seconds between samples")
    args = parser.parse_args()

    path, label = find_amdgpu_power()
    writer = csv.writer(sys.stdout)
    writer.writerow(["timestamp_utc", "seconds_elapsed", "watts", "source", "label", "path"])
    start = time.monotonic()
    while True:
        elapsed = time.monotonic() - start
        if elapsed > args.seconds:
            break
        timestamp = datetime.now(timezone.utc).isoformat()
        writer.writerow([timestamp, f"{elapsed:.3f}", f"{read_watts(path):.3f}", "amdgpu_hwmon", label, str(path)])
        sys.stdout.flush()
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
