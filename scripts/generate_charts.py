#!/usr/bin/env python3
"""Generate SVG benchmark charts from data/*.csv.

The charts are intentionally dependency-free so contributors can regenerate
them with the system Python that ships on Ubuntu/Fedora.
"""

from __future__ import annotations

import csv
import html
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CHARTS = ROOT / "charts"

COLORS = [
    "#1f77b4",
    "#d62728",
    "#2ca02c",
    "#9467bd",
    "#ff7f0e",
    "#17becf",
    "#7f7f7f",
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(row: dict[str, str], key: str) -> float:
    value = row.get(key, "").strip()
    return float(value) if value else math.nan


def nice_max(value: float) -> float:
    if value <= 0:
        return 1.0
    exp = math.floor(math.log10(value))
    step = 10**exp
    for multiplier in (1, 2, 2.5, 5, 10):
        candidate = multiplier * step
        if candidate >= value:
            return candidate
    return 10 * step


def write_svg(filename: str, body: list[str], width: int, height: int) -> None:
    CHARTS.mkdir(exist_ok=True)
    content = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
        "<style>",
        "text{font-family:Inter,Segoe UI,Arial,sans-serif;fill:#17202a}",
        ".title{font-size:26px;font-weight:700}",
        ".subtitle{font-size:14px;fill:#52616f}",
        ".axis{font-size:12px;fill:#52616f}",
        ".tick{font-size:11px;fill:#52616f}",
        ".legend{font-size:13px;fill:#17202a}",
        ".note{font-size:12px;fill:#52616f}",
        ".grid{stroke:#dce3ea;stroke-width:1}",
        ".axis-line{stroke:#6b7a89;stroke-width:1.2}",
        "</style>",
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        *body,
        "</svg>",
        "",
    ]
    (CHARTS / filename).write_text("\n".join(content), encoding="utf-8")


def line_chart(
    filename: str,
    title: str,
    subtitle: str,
    x_labels: list[str],
    series: list[dict[str, object]],
    y_label: str,
    y_max: float | None = None,
    note: str | None = None,
) -> None:
    width, height = 980, 560
    left, right, top, bottom = 82, 42, 92, 92
    plot_w, plot_h = width - left - right, height - top - bottom
    values = [v for item in series for v in item["values"] if v is not None and math.isfinite(v)]
    ymax = nice_max(max(values) * 1.08 if y_max is None else y_max)
    ticks = 5

    def x_pos(index: int) -> float:
        if len(x_labels) == 1:
            return left + plot_w / 2
        return left + (plot_w * index / (len(x_labels) - 1))

    def y_pos(value: float) -> float:
        return top + plot_h - (value / ymax) * plot_h

    body = [
        f'<text x="{left}" y="40" class="title">{esc(title)}</text>',
        f'<text x="{left}" y="64" class="subtitle">{esc(subtitle)}</text>',
    ]

    for i in range(ticks + 1):
        value = ymax * i / ticks
        y = y_pos(value)
        body.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" class="grid"/>')
        body.append(f'<text x="{left - 10}" y="{y + 4:.1f}" text-anchor="end" class="tick">{value:.0f}</text>')

    body.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" class="axis-line"/>')
    body.append(f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" class="axis-line"/>')
    body.append(
        f'<text x="20" y="{top + plot_h / 2:.1f}" class="axis" transform="rotate(-90 20 {top + plot_h / 2:.1f})">{esc(y_label)}</text>'
    )

    for i, label in enumerate(x_labels):
        x = x_pos(i)
        body.append(f'<text x="{x:.1f}" y="{top + plot_h + 26}" text-anchor="middle" class="tick">{esc(label)}</text>')

    legend_x = left
    legend_y = height - 36
    for index, item in enumerate(series):
        color = COLORS[index % len(COLORS)]
        values_for_item = item["values"]
        points = []
        for i, value in enumerate(values_for_item):
            if value is None or not math.isfinite(value):
                continue
            points.append(f"{x_pos(i):.1f},{y_pos(value):.1f}")
        if len(points) >= 2:
            body.append(f'<polyline fill="none" stroke="{color}" stroke-width="3" points="{" ".join(points)}"/>')
        for i, value in enumerate(values_for_item):
            if value is None or not math.isfinite(value):
                continue
            x, y = x_pos(i), y_pos(value)
            body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{color}"/>')
            body.append(f'<text x="{x:.1f}" y="{y - 9:.1f}" text-anchor="middle" class="tick">{value:.1f}</text>')
        body.append(f'<rect x="{legend_x}" y="{legend_y - 10}" width="18" height="4" fill="{color}"/>')
        body.append(f'<text x="{legend_x + 26}" y="{legend_y - 4}" class="legend">{esc(item["name"])}</text>')
        legend_x += max(220, len(str(item["name"])) * 8 + 60)

    if note:
        body.append(f'<text x="{left}" y="{height - 12}" class="note">{esc(note)}</text>')

    write_svg(filename, body, width, height)


def grouped_bar_chart(
    filename: str,
    title: str,
    subtitle: str,
    groups: list[str],
    bars: list[dict[str, object]],
    y_label: str,
    y_max: float | None = None,
    note: str | None = None,
) -> None:
    width, height = 1060, 590
    left, right, top, bottom = 88, 42, 92, 122
    plot_w, plot_h = width - left - right, height - top - bottom
    values = [v for bar in bars for v in bar["values"] if v is not None and math.isfinite(v)]
    ymax = nice_max(max(values) * 1.12 if y_max is None else y_max)
    ticks = 5
    group_w = plot_w / len(groups)
    bar_gap = 8
    bar_w = max(8, min(42, (group_w - 28) / len(bars) - bar_gap))

    def y_pos(value: float) -> float:
        return top + plot_h - (value / ymax) * plot_h

    body = [
        f'<text x="{left}" y="40" class="title">{esc(title)}</text>',
        f'<text x="{left}" y="64" class="subtitle">{esc(subtitle)}</text>',
    ]
    for i in range(ticks + 1):
        value = ymax * i / ticks
        y = y_pos(value)
        body.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" class="grid"/>')
        body.append(f'<text x="{left - 10}" y="{y + 4:.1f}" text-anchor="end" class="tick">{value:.0f}</text>')

    body.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" class="axis-line"/>')
    body.append(f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" class="axis-line"/>')
    body.append(
        f'<text x="22" y="{top + plot_h / 2:.1f}" class="axis" transform="rotate(-90 22 {top + plot_h / 2:.1f})">{esc(y_label)}</text>'
    )

    for group_index, group in enumerate(groups):
        center = left + group_w * group_index + group_w / 2
        body.append(f'<text x="{center:.1f}" y="{top + plot_h + 28}" text-anchor="middle" class="tick">{esc(group)}</text>')
        start = center - ((len(bars) * bar_w) + ((len(bars) - 1) * bar_gap)) / 2
        for bar_index, bar in enumerate(bars):
            value = bar["values"][group_index]
            if value is None or not math.isfinite(value):
                continue
            color = COLORS[bar_index % len(COLORS)]
            x = start + bar_index * (bar_w + bar_gap)
            y = y_pos(value)
            h = top + plot_h - y
            body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="{color}"/>')
            body.append(f'<text x="{x + bar_w / 2:.1f}" y="{y - 7:.1f}" text-anchor="middle" class="tick">{value:.0f}</text>')

    legend_x = left
    legend_y = height - 44
    for index, bar in enumerate(bars):
        color = COLORS[index % len(COLORS)]
        body.append(f'<rect x="{legend_x}" y="{legend_y - 12}" width="14" height="14" fill="{color}"/>')
        body.append(f'<text x="{legend_x + 22}" y="{legend_y}" class="legend">{esc(bar["name"])}</text>')
        legend_x += max(190, len(str(bar["name"])) * 8 + 54)

    if note:
        body.append(f'<text x="{left}" y="{height - 14}" class="note">{esc(note)}</text>')

    write_svg(filename, body, width, height)


def chart_multi_user() -> None:
    rows = [r for r in read_csv("multi_user.csv") if r["status"] == "measured-local"]
    slots = sorted({int(r["parallel_slots"]) for r in rows})
    by_model: dict[str, dict[int, float]] = defaultdict(dict)
    for row in rows:
        by_model[row["model"]][int(row["parallel_slots"])] = as_float(row, "aggregate_tps_mean")
    series = [
        {"name": model, "values": [by_model[model].get(slot) for slot in slots]}
        for model in sorted(by_model)
    ]
    line_chart(
        "multi_user_aggregate.svg",
        "llama-server multi-user aggregate throughput",
        "Vulkan RADV, llama.cpp b9010, continuous batching, 128 generated tokens/request",
        [f"-np {slot}" for slot in slots],
        series,
        "aggregate generation tokens/s",
        note="Source: data/multi_user.csv",
    )


def chart_long_context_prompt() -> None:
    rows = [
        r
        for r in read_csv("long_context.csv")
        if r["status"] == "measured-local" and r["metric"] == "pp" and int(r["context_tokens"]) > 0
    ]
    contexts = sorted({int(r["context_tokens"]) for r in rows})
    by_model: dict[str, dict[int, float]] = defaultdict(dict)
    for row in rows:
        by_model[row["model"]][int(row["context_tokens"])] = as_float(row, "tps")
    series = [
        {"name": model, "values": [by_model[model].get(ctx) for ctx in contexts]}
        for model in sorted(by_model)
    ]
    line_chart(
        "long_context_prompt.svg",
        "Long-context prompt processing",
        "Vulkan RADV llama-bench prompt processing; not decode after a filled KV cache",
        [f"{ctx // 1024}K" for ctx in contexts],
        series,
        "prompt eval tokens/s",
        note="Source: data/long_context.csv",
    )


def chart_filled_kv_decode() -> None:
    rows = [
        r
        for r in read_csv("filled_kv_decode.csv")
        if r["status"] == "measured-local"
        and r["cache_type_k"] == "f16"
        and "synthetic" in r["notes"]
    ]
    contexts = sorted({int(r["target_prompt_tokens"]) for r in rows})
    by_model: dict[str, dict[int, float]] = defaultdict(dict)
    for row in rows:
        by_model[row["model"]][int(row["target_prompt_tokens"])] = as_float(row, "eval_tps_mean")
    series = [
        {"name": model, "values": [by_model[model].get(ctx) for ctx in contexts]}
        for model in sorted(by_model)
    ]
    line_chart(
        "filled_kv_decode.svg",
        "Decode speed after 32K-128K filled KV cache",
        "llama-server full request, f16 KV, synthetic prompt, prompt cache disabled",
        [f"{ctx // 1024}K" for ctx in contexts],
        series,
        "decode tokens/s after fill",
        note="Source: data/filled_kv_decode.csv",
    )


def chart_kv_cache_tradeoff() -> None:
    rows = [
        r
        for r in read_csv("filled_kv_decode.csv")
        if r["model"] == "Qwen3.6 35B-A3B" and "synthetic" in r["notes"] and int(r["target_prompt_tokens"]) in (32768, 65536)
    ]
    baseline: dict[int, dict[str, float]] = {}
    for row in rows:
        ctx = int(row["target_prompt_tokens"])
        if row["cache_type_k"] == "f16":
            baseline[ctx] = {
                "prompt": as_float(row, "prompt_eval_tps_mean"),
                "decode": as_float(row, "eval_tps_mean"),
                "wall": as_float(row, "request_wall_s_mean"),
            }

    groups: list[str] = []
    prompt_values: list[float] = []
    decode_values: list[float] = []
    wall_values: list[float] = []
    for ctx in (32768, 65536):
        for cache in ("q8_0", "q4_0"):
            row = next((r for r in rows if int(r["target_prompt_tokens"]) == ctx and r["cache_type_k"] == cache), None)
            if not row:
                continue
            base = baseline[ctx]
            groups.append(f"{ctx // 1024}K {cache}")
            prompt_values.append(as_float(row, "prompt_eval_tps_mean") / base["prompt"] * 100)
            decode_values.append(as_float(row, "eval_tps_mean") / base["decode"] * 100)
            wall_values.append(as_float(row, "request_wall_s_mean") / base["wall"] * 100)

    grouped_bar_chart(
        "kv_cache_tradeoff.svg",
        "Qwen3.6 KV-cache quantization tradeoff",
        "Relative to f16 KV at the same context. Higher prompt/decode is faster; higher wall time is worse.",
        groups,
        [
            {"name": "prompt eval % of f16", "values": prompt_values},
            {"name": "decode % of f16", "values": decode_values},
            {"name": "wall time % of f16", "values": wall_values},
        ],
        "relative to f16 (%)",
        y_max=140,
        note="Source: data/filled_kv_decode.csv",
    )


def chart_real_vs_synthetic() -> None:
    rows = [r for r in read_csv("filled_kv_decode.csv") if int(r["target_prompt_tokens"]) == 65536]
    groups = []
    prompt_values = []
    decode_values = []
    for model in ("Qwen3.6 35B-A3B", "Qwen3-Next 80B-A3B"):
        synthetic = next(
            (
                r
                for r in rows
                if r["model"] == model
                and r["cache_type_k"] == "f16"
                and "synthetic" in r["notes"]
                and int(r["target_prompt_tokens"]) == 65536
            ),
            None,
        )
        real = next(
            (
                r
                for r in rows
                if r["model"] == model
                and r["cache_type_k"] == "f16"
                and "real guide" in r["notes"]
            ),
            None,
        )
        if not synthetic or not real:
            continue
        groups.append(model.replace(" 35B-A3B", "").replace(" 80B-A3B", ""))
        prompt_values.append(as_float(real, "prompt_eval_tps_mean") / as_float(synthetic, "prompt_eval_tps_mean") * 100)
        decode_values.append(as_float(real, "eval_tps_mean") / as_float(synthetic, "eval_tps_mean") * 100)

    grouped_bar_chart(
        "real_vs_synthetic.svg",
        "Real 64K documents vs synthetic prompts",
        "Real guide/documentation corpus relative to synthetic repeated-token prompt at similar length",
        groups,
        [
            {"name": "prompt eval % of synthetic", "values": prompt_values},
            {"name": "decode % of synthetic", "values": decode_values},
        ],
        "relative throughput (%)",
        y_max=120,
        note="Source: data/filled_kv_decode.csv",
    )


def chart_backend_spot_check() -> None:
    rows = [r for r in read_csv("benchmarks.csv") if r["date"] == "2026-05-03" and r["status"] == "measured-local"]
    models = ["Qwen3.6 35B-A3B", "Qwen3-Coder 30B-A3B"]
    vulkan_values = []
    rocm_values = []
    for model in models:
        vulkan = next((r for r in rows if r["model"] == model and r["backend"] == "Vulkan"), None)
        rocm = next((r for r in rows if r["model"] == model and r["backend"] == "ROCm"), None)
        vulkan_values.append(as_float(vulkan, "tg_tps") if vulkan else None)
        rocm_values.append(as_float(rocm, "tg_tps") if rocm else None)

    grouped_bar_chart(
        "backend_spot_check.svg",
        "Vulkan RADV vs ROCm HIP short-context spot check",
        "Same measured models where both backends have local May 2026 rows",
        [m.replace(" 35B-A3B", "").replace(" 30B-A3B", "") for m in models],
        [
            {"name": "Vulkan RADV tg128", "values": vulkan_values},
            {"name": "ROCm HIP tg128", "values": rocm_values},
        ],
        "generation tokens/s",
        note="Source: data/benchmarks.csv",
    )


def chart_backend_crossover() -> None:
    rows = [
        r
        for r in read_csv("backend_crossover.csv")
        if r["status"] == "measured-local"
        and r["model"] in ("Qwen3.6 35B-A3B", "Qwen3-Coder 30B-A3B")
    ]
    models = ("Qwen3.6 35B-A3B", "Qwen3-Coder 30B-A3B")
    groups = [m.replace(" 35B-A3B", "").replace(" 30B-A3B", "") for m in models]

    def value(model: str, backend: str, workload: str) -> float | None:
        row = next(
            (
                r
                for r in rows
                if r["model"] == model
                and r["backend"] == backend
                and r["workload"] == workload
            ),
            None,
        )
        return as_float(row, "tps") if row else None

    grouped_bar_chart(
        "backend_crossover_prefill.svg",
        "HIP vs Vulkan prompt processing",
        "Local existing-build spot check at pp16384. Treat as direction, not a same-build fairness claim.",
        groups,
        [
            {"name": "Vulkan RADV pp16384", "values": [value(model, "Vulkan", "pp16384") for model in models]},
            {"name": "ROCm HIP pp16384", "values": [value(model, "ROCm HIP", "pp16384") for model in models]},
        ],
        "prompt tokens/s",
        note="Source: data/backend_crossover.csv",
    )
    grouped_bar_chart(
        "backend_crossover_generation.svg",
        "HIP vs Vulkan token generation",
        "Local existing-build spot check at tg128. Vulkan remains the faster generation path here.",
        groups,
        [
            {"name": "Vulkan RADV tg128", "values": [value(model, "Vulkan", "tg128") for model in models]},
            {"name": "ROCm HIP tg128", "values": [value(model, "ROCm HIP", "tg128") for model in models]},
        ],
        "generation tokens/s",
        note="Source: data/backend_crossover.csv",
    )


def main() -> None:
    chart_multi_user()
    chart_long_context_prompt()
    chart_filled_kv_decode()
    chart_kv_cache_tradeoff()
    chart_real_vs_synthetic()
    chart_backend_spot_check()
    chart_backend_crossover()


if __name__ == "__main__":
    main()
