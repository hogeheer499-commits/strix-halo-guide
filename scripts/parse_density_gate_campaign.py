#!/usr/bin/env python3
"""Build machine-readable AMD density-gate data from committed raw logs."""

from __future__ import annotations

import csv
import argparse
import glob
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/2026-07-13/llamacpp-b9979-amd-density-gate"
DETAIL = ROOT / "data/moe_density_gate.csv"
SUMMARY = ROOT / "data/moe_density_gate_summary.csv"

MODELS = {
    "30b": ("Qwen3-Coder 30B-A3B", "UD-Q4_K_XL", 128, 8),
    "80b": ("Qwen3-Next 80B-A3B", "UD-Q4_K_XL", 512, 10),
}


def parse_output(path: Path) -> list[dict[str, float | int]]:
    rows: list[dict[str, float | int]] = []
    for line in path.read_text(errors="replace").splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "pl" in item:
            rows.append(
                {
                    "concurrency": int(item["pl"]),
                    "prompt_tps": float(item["speed_pp"]),
                    "aggregate_decode_tps": float(item["speed_tg"]),
                    "total_seconds": float(item["t"]),
                    "combined_tps": float(item["speed"]),
                }
            )
    if rows:
        return rows

    for line in path.read_text(errors="replace").splitlines():
        if not line.startswith("|") or line.startswith("|    PP") or line.startswith("|-------"):
            continue
        columns = [column.strip() for column in line.strip().strip("|").split("|")]
        try:
            rows.append(
                {
                    "concurrency": int(columns[2]),
                    "prompt_tps": float(columns[5]),
                    "aggregate_decode_tps": float(columns[7]),
                    "total_seconds": float(columns[8]),
                    "combined_tps": float(columns[9]),
                }
            )
        except (ValueError, IndexError):
            continue
    return rows


def run_metadata(path: Path) -> tuple[str, str, int, str]:
    name = path.name.removesuffix(".stdout.log")
    model_key = name[:3]
    if "-rocm-" in name:
        route = "lemonade-rocm-b1259"
    elif "-dense16-" in name:
        route = "vulkan-b9979-density-dense16"
    elif "-gate-" in name:
        route = "vulkan-b9979-density"
    else:
        route = "vulkan-b9979-stock"
    match = re.search(r"-r(\d+)$", name)
    repeat = int(match.group(1)) if match else 0
    group = path.parent.name
    return model_key, route, repeat, group


def thermal_metadata(path: Path) -> dict[str, str]:
    summary_path = path.with_name(path.name.replace(".stdout.log", ".summary.csv"))
    if not summary_path.exists():
        return {"max_temp_c": "", "avg_ppt_w": "", "max_ppt_w": ""}
    with summary_path.open(newline="") as handle:
        row = next(csv.DictReader(handle))
    if row["status"] != "0" or row["monitor_status"] != "0":
        return {}
    return {
        "max_temp_c": f"{int(row['max_temp_mC']) / 1000:.1f}",
        "avg_ppt_w": f"{float(row['avg_ppt_uW']) / 1_000_000:.3f}",
        "max_ppt_w": f"{float(row['max_ppt_uW']) / 1_000_000:.3f}",
    }


def collect() -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    seen_discovery: set[tuple[str, str, int]] = set()
    for filename in sorted(glob.glob(str(RAW / "**/*.stdout.log"), recursive=True)):
        path = Path(filename)
        model_key, route, repeat, group = run_metadata(path)
        if model_key not in MODELS:
            continue
        thermal = thermal_metadata(path)
        if not thermal:
            continue
        model, quant, experts, used = MODELS[model_key]
        for measured in parse_output(path):
            key = (model_key, route, int(measured["concurrency"]))
            if group == "discovery":
                if key in seen_discovery:
                    continue
                seen_discovery.add(key)
            build = "b1259 e77056f" if "rocm" in route else "b9979 4114ba18 + opt-in patch"
            result.append(
                {
                    "date": "2026-07-13",
                    "status": "measured-local",
                    "source": str(path.parent.relative_to(ROOT)),
                    "run_group": group,
                    "run_id": path.name.removesuffix(".stdout.log"),
                    "repeat": str(repeat),
                    "system": "Beelink GTR9 Pro",
                    "backend": "ROCm/HIP" if "rocm" in route else "Vulkan/RADV",
                    "tool_route": route,
                    "build": build,
                    "model": model,
                    "quant": quant,
                    "experts": str(experts),
                    "experts_used": str(used),
                    "context_tokens": "65536",
                    "prompt_tokens_per_sequence": "512",
                    "generation_tokens_per_sequence": "128",
                    "concurrency": str(measured["concurrency"]),
                    "prompt_tps": f"{measured['prompt_tps']:.6f}",
                    "aggregate_decode_tps": f"{measured['aggregate_decode_tps']:.6f}",
                    "total_seconds": f"{measured['total_seconds']:.6f}",
                    "combined_tps": f"{measured['combined_tps']:.6f}",
                    **thermal,
                    "notes": "PPT is amdgpu sysfs APU/GPU telemetry, not wall power; each controlled run cooled below 50 C before high-DPM measurement",
                }
            )
    return result


def write_detail(rows: list[dict[str, str]], destination: Path = DETAIL) -> None:
    with destination.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_summary(rows: list[dict[str, str]], destination: Path = SUMMARY, retained_source: Path = SUMMARY) -> None:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["model"], row["tool_route"], row["concurrency"])].append(row)

    output: list[dict[str, str]] = []
    for (model, route, concurrency), candidates in sorted(grouped.items(), key=lambda item: (item[0][0], item[0][1], int(item[0][2]))):
        repeated = [row for row in candidates if row["run_group"].startswith("repeats")]
        selected = repeated or candidates
        values = [float(row["aggregate_decode_tps"]) for row in selected]
        temperatures = [float(row["max_temp_c"]) for row in selected]
        powers = [float(row["avg_ppt_w"]) for row in selected]
        output.append(
            {
                "date": "2026-07-13",
                "system": "Beelink GTR9 Pro",
                "model": model,
                "tool_route": route,
                "concurrency": concurrency,
                "n": str(len(values)),
                "mean_aggregate_decode_tps": f"{statistics.mean(values):.3f}",
                "stddev_aggregate_decode_tps": f"{statistics.stdev(values):.3f}" if len(values) > 1 else "n/a",
                "min_aggregate_decode_tps": f"{min(values):.3f}",
                "max_aggregate_decode_tps": f"{max(values):.3f}",
                "max_temp_c": f"{max(temperatures):.1f}",
                "mean_avg_ppt_w": f"{statistics.mean(powers):.3f}",
                "source": "data/raw/2026-07-13/llamacpp-b9979-amd-density-gate",
            }
        )

    # This parser owns only the July 13 campaign. Later curated campaign rows
    # are independent inputs, not disposable output of this parser. Preserve
    # every field and reject collisions using the complete campaign identity.
    with retained_source.open(newline="") as handle:
        retained = list(csv.DictReader(handle))
    owned_source = str(RAW.relative_to(ROOT))
    output.extend(row for row in retained if not (row["date"] == "2026-07-13" and row["source"] == owned_source))
    identity_fields = ("date", "system", "model", "tool_route", "concurrency", "source")
    identities = [tuple(row[key] for key in identity_fields) for row in output]
    if len(identities) != len(set(identities)):
        raise ValueError("duplicate full campaign identity; refusing summary rewrite")
    with destination.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path,
                        help="Explicit scratch destination; compare before replacing canonical data")
    args = parser.parse_args()
    if args.output_dir.resolve() == DETAIL.parent.resolve():
        parser.error("use a scratch output directory and review the diff before replacing canonical data")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = collect()
    if not rows:
        raise SystemExit("no valid benchmark rows found")
    write_detail(rows, args.output_dir / DETAIL.name)
    write_summary(rows, args.output_dir / SUMMARY.name)
    print(f"wrote {len(rows)} July 13 detail rows; shared summary retains independent campaign rows from {SUMMARY.name}")


if __name__ == "__main__":
    main()
