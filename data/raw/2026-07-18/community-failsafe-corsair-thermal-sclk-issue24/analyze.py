#!/usr/bin/env python3
"""Validate and summarize the 2026-07-18 strict Strix Halo campaign."""

from __future__ import annotations

import csv
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NODES = ("node-a", "node-b", "node-c")
RUNS = {
    2200: "strict-soak-2200-20260718T185727Z",
    2400: "strict-soak-2400-20260718T192908Z",
    2500: "strict-soak-2500-20260718T200042Z",
    2600: "strict-soak-2600-20260718T203226Z",
}
SWEEP_RUN = "strict-sweep-20260718T184554Z"
STOCK_SHORT_RUNS = {
    "node-a": "strict-stock-stage2-20260718T220900Z",
    "node-b": "strict-stock-stage3-20260718T222000Z",
    "node-c": "strict-stock-stage1-20260718T215500Z",
}
STOCK_LONG_RUNS = {
    "node-a": "strict-stock-30m-node-a-20260718T231000Z",
    "node-b": "strict-stock-30m-node-b-20260719T010100Z",
    "node-c": "strict-stock-30m-node-c-20260718T223000Z",
}
POWER_THRESHOLD_W = 40
STABLE_METADATA_KEYS = (
    "ambient_c",
    "cooling_context",
    "background_condition",
    "background_running_container_count",
    "background_model_process_count",
    "system_vendor",
    "product_name",
    "product_version",
    "board_vendor",
    "board_name",
    "board_version_smbios",
    "physical_pcb_revision",
    "bios_vendor",
    "bios_version",
    "bios_date",
    "ec_firmware_version",
    "os_pretty_name",
    "kernel",
    "kernel_cmdline_relevant",
    "gpu_identity",
    "ec_power_mode",
    "fan1_mode",
    "fan1_rampup_curve",
    "fan1_rampdown_curve",
    "fan2_mode",
    "fan2_rampup_curve",
    "fan2_rampdown_curve",
    "fan3_mode",
    "fan3_rampup_curve",
    "fan3_rampdown_curve",
    "podman_version",
    "container_reference",
    "container_repo_digests",
    "llama_cpp_version",
    "package_mesa_vulkan",
    "package_amd_gpu_firmware",
    "package_linux_firmware",
    "model_file_count",
    "model_01_name",
    "model_01_bytes",
    "model_02_name",
    "model_02_bytes",
    "model_03_name",
    "model_03_bytes",
)
NODE_STABLE_METADATA_KEYS = ("ec_driver_commit",)


def read_kv(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            result[key] = value
    return result


def recompute_soak(path: Path) -> dict[str, float | int]:
    rows: list[tuple[int, float, float, int]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        rows.append(
            (
                int(fields[0]),
                int(fields[2]) / 1_000,
                int(fields[3]) / 1_000_000,
                int(fields[4]),
            )
        )

    loaded = [row for row in rows if row[2] >= POWER_THRESHOLD_W]
    third = max(1, len(loaded) // 3)
    first = loaded[:third]
    last = loaded[-third:]
    first_edge = statistics.fmean(row[1] for row in first)
    last_edge = statistics.fmean(row[1] for row in last)
    xs = [row[0] / 60 for row in last]
    ys = [row[1] for row in last]
    x_bar = statistics.fmean(xs)
    y_bar = statistics.fmean(ys)
    denominator = sum((x - x_bar) ** 2 for x in xs)
    slope_10m = (
        sum((x - x_bar) * (y - y_bar) for x, y in zip(xs, ys))
        / denominator
        * 10
        if denominator
        else 0
    )
    return {
        "samples_total": len(rows),
        "samples_under_load": len(loaded),
        "loaded_duration_s": loaded[-1][0] - loaded[0][0],
        "edge_max_c": max(row[1] for row in loaded),
        "edge_final_c": loaded[-1][1],
        "edge_first_third_avg_c": first_edge,
        "edge_last_third_avg_c": last_edge,
        "edge_first_to_last_delta_c": last_edge - first_edge,
        "edge_late_slope_c_per_10m": slope_10m,
        "power_avg_w": statistics.fmean(row[2] for row in loaded),
        "power_max_w": max(row[2] for row in loaded),
        "sclk_avg_mhz": statistics.fmean(row[3] for row in loaded),
    }


def validate_summary(recorded: dict[str, str], calculated: dict[str, float | int]) -> None:
    for key, expected in calculated.items():
        actual = float(recorded[key])
        if isinstance(expected, int):
            tolerance = 0
        elif key == "sclk_avg_mhz":
            tolerance = 0.051
        else:
            tolerance = 0.0011
        if abs(actual - expected) > tolerance:
            raise ValueError(f"{key}: recorded={actual}, calculated={expected}")


def validate_campaign_metadata() -> None:
    paths: list[tuple[str, Path]] = []
    for cap, run in RUNS.items():
        for node in NODES:
            paths.append((node, ROOT / node / run / f"soak-{cap}MHz" / "metadata.txt"))
    for node in NODES:
        paths.append((node, ROOT / node / SWEEP_RUN / "sweep" / "metadata.txt"))
        for runs in (STOCK_SHORT_RUNS, STOCK_LONG_RUNS):
            paths.append((node, ROOT / node / runs[node] / "soak-stock" / "metadata.txt"))

    baseline = read_kv(paths[0][1])
    node_baselines: dict[str, dict[str, str]] = {}
    for node, path in paths:
        metadata = read_kv(path)
        node_baseline = node_baselines.setdefault(node, metadata)
        if metadata["background_condition"] != "zero-running-containers":
            raise ValueError(f"{path}: wrong background condition")
        if metadata["background_running_container_count"] != "0":
            raise ValueError(f"{path}: background container detected")
        if metadata["background_model_process_count"] != "0":
            raise ValueError(f"{path}: background model process detected")
        for key in STABLE_METADATA_KEYS:
            is_stock_run = any("stock" in part for part in path.parts)
            if key == "ec_firmware_version" and is_stock_run and metadata[key] == "unknown":
                continue
            if metadata[key] != baseline[key]:
                raise ValueError(
                    f"{path}: metadata mismatch for {key}: "
                    f"{metadata[key]!r} != {baseline[key]!r}"
                )
        for key in NODE_STABLE_METADATA_KEYS:
            if metadata[key] != node_baseline[key]:
                raise ValueError(
                    f"{path}: node-local metadata changed for {key}: "
                    f"{metadata[key]!r} != {node_baseline[key]!r}"
                )


def validate_stock_telemetry(path: Path) -> None:
    stock_samples = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        power_w = int(fields[3]) / 1_000_000
        if power_w < POWER_THRESHOLD_W:
            continue
        stock_samples += 1
        if fields[5] != "2900" or fields[6] != "auto":
            raise ValueError(f"{path}: loaded sample was not stock 2900 MHz/auto")
    if stock_samples < 6:
        raise ValueError(f"{path}: insufficient stock samples")


def print_stock_table() -> None:
    print()
    print("## Strict stock controls")
    print()
    print("| Node | Duration | Avg SCLK | Avg W | Max W | Max °C | Final °C | Δ first→last third | Late °C/10m | Verdict |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    module_hashes: set[str] = set()
    for label, runs in (("5 min", STOCK_SHORT_RUNS), ("30 min", STOCK_LONG_RUNS)):
        for node in NODES:
            directory = ROOT / node / runs[node] / "soak-stock"
            summary = read_kv(directory / "summary.txt")
            metadata = read_kv(directory / "metadata.txt")
            config = read_kv(directory / "run-config.txt")
            calculated = recompute_soak(directory / "telemetry.tsv")
            validate_summary(summary, calculated)
            validate_stock_telemetry(directory / "telemetry.tsv")
            if summary["exit_reason"] != "completed":
                raise ValueError(f"{node} {label}: incomplete stock soak")
            if config["target"] != "stock" or config["max_safe_temp_c"] != "95":
                raise ValueError(f"{node} {label}: wrong stock configuration")
            module_hashes.add(metadata["ec_driver_module_sha256"])
            print(
                f"| {node} | {label} | {float(summary['sclk_avg_mhz']):.1f} | "
                f"{float(summary['power_avg_w']):.2f} | {float(summary['power_max_w']):.2f} | "
                f"{float(summary['edge_max_c']):.0f} | {float(summary['edge_final_c']):.0f} | "
                f"{float(summary['edge_first_to_last_delta_c']):+.2f} | "
                f"{float(summary['edge_late_slope_c_per_10m']):+.2f} | {summary['verdict']} |"
            )
    if len(module_hashes) != 1:
        raise ValueError(f"stock runs used differing EC module hashes: {module_hashes}")


def print_soak_table() -> None:
    print("## Strict 30-minute soaks")
    print()
    print("| Node | Cap | Avg SCLK | Avg W | Max W | Max °C | Final °C | Δ first→last third | Late °C/10m | Verdict |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for cap, run in RUNS.items():
        for node in NODES:
            directory = ROOT / node / run / f"soak-{cap}MHz"
            summary = read_kv(directory / "summary.txt")
            metadata = read_kv(directory / "metadata.txt")
            calculated = recompute_soak(directory / "telemetry.tsv")
            validate_summary(summary, calculated)
            if summary["exit_reason"] != "completed":
                raise ValueError(f"{node} {cap}: incomplete soak")
            if metadata["background_condition"] != "zero-running-containers":
                raise ValueError(f"{node} {cap}: wrong background condition")
            if metadata["background_running_container_count"] != "0":
                raise ValueError(f"{node} {cap}: background container detected")
            if metadata["background_model_process_count"] != "0":
                raise ValueError(f"{node} {cap}: background model process detected")
            print(
                f"| {node} | {cap} | {float(summary['sclk_avg_mhz']):.1f} | "
                f"{float(summary['power_avg_w']):.2f} | {float(summary['power_max_w']):.2f} | "
                f"{float(summary['edge_max_c']):.0f} | {float(summary['edge_final_c']):.0f} | "
                f"{float(summary['edge_first_to_last_delta_c']):+.2f} | "
                f"{float(summary['edge_late_slope_c_per_10m']):+.2f} | {summary['verdict']} |"
            )


def print_sweep_table() -> None:
    print()
    print("## Strict 10-repetition throughput sweep")
    print()
    print("| Node | Cap | Prompt tok/s | Gen tok/s | Max °C | Max W | Status |")
    print("|---|---:|---:|---:|---:|---:|---|")
    for node in NODES:
        path = ROOT / node / SWEEP_RUN / "sweep" / "summary.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) != 4:
            raise ValueError(f"{node}: expected four sweep rows, got {len(rows)}")
        for row in rows:
            print(
                f"| {node} | {row['target'].removesuffix('MHz')} | "
                f"{float(row['pp_avg_ts']):.2f} | {float(row['tg_avg_ts']):.2f} | "
                f"{float(row['max_edge_c']):.0f} | {float(row['max_power_w']):.2f} | {row['status']} |"
            )


def print_aggregate_table() -> None:
    print()
    print("## Three-node aggregate")
    print()
    print("| Cap | Prompt tok/s | Gen tok/s | Soak avg W | Worst soak °C | Prompt vs 2200 | Gen vs 2200 |")
    print("|---:|---:|---:|---:|---:|---:|---:|")

    sweep_by_cap: dict[int, list[tuple[float, float]]] = {cap: [] for cap in RUNS}
    for node in NODES:
        path = ROOT / node / SWEEP_RUN / "sweep" / "summary.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                cap = int(row["target"].removesuffix("MHz"))
                sweep_by_cap[cap].append((float(row["pp_avg_ts"]), float(row["tg_avg_ts"])))

    soak_by_cap: dict[int, list[tuple[float, float]]] = {cap: [] for cap in RUNS}
    for cap, run in RUNS.items():
        for node in NODES:
            directory = ROOT / node / run / f"soak-{cap}MHz"
            summary = read_kv(directory / "summary.txt")
            soak_by_cap[cap].append((float(summary["power_avg_w"]), float(summary["edge_max_c"])))

    baseline_pp = statistics.fmean(value[0] for value in sweep_by_cap[2200])
    baseline_tg = statistics.fmean(value[1] for value in sweep_by_cap[2200])
    for cap in RUNS:
        prompt = statistics.fmean(value[0] for value in sweep_by_cap[cap])
        generation = statistics.fmean(value[1] for value in sweep_by_cap[cap])
        power = statistics.fmean(value[0] for value in soak_by_cap[cap])
        worst_temp = max(value[1] for value in soak_by_cap[cap])
        print(
            f"| {cap} | {prompt:.2f} | {generation:.2f} | {power:.2f} | {worst_temp:.0f} | "
            f"{(prompt / baseline_pp - 1) * 100:+.2f}% | {(generation / baseline_tg - 1) * 100:+.2f}% |"
        )


if __name__ == "__main__":
    validate_campaign_metadata()
    print_soak_table()
    print_sweep_table()
    print_aggregate_table()
    print_stock_table()
