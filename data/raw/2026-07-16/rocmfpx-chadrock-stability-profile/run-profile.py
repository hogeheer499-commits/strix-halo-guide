#!/usr/bin/env python3
import json
import pathlib
import statistics
import time
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parent
BASE_URL = "http://127.0.0.1:18001"
REFERENCE = (ROOT / "prompt_3946_reference.txt").read_text(encoding="utf-8")

prompts = {
    "approx1k": REFERENCE[:4700],
    "reference4k": REFERENCE,
    "approx8k": REFERENCE + "\n\n" + REFERENCE,
    "approx16k": "\n\n".join([REFERENCE] * 4),
}


def post(path, payload):
    request = urllib.request.Request(
        BASE_URL + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    started = time.monotonic()
    with urllib.request.urlopen(request, timeout=900) as response:
        data = json.load(response)
    return data, time.monotonic() - started


rows = []
for repeat in range(1, 4):
    for profile, prompt in prompts.items():
        payload = {
            "prompt": prompt,
            "n_predict": 512,
            "temperature": 0,
            "ignore_eos": True,
            "cache_prompt": False,
            "speculative.n_max": 4,
            "speculative.n_min": 0,
            "speculative.p_min": 0.25,
        }
        stem = f"{profile}-r{repeat}"
        (ROOT / f"{stem}.request.json").write_text(
            json.dumps(payload, indent=2), encoding="utf-8"
        )
        response, wall_seconds = post("/completion", payload)
        (ROOT / f"{stem}.response.json").write_text(
            json.dumps(response, indent=2), encoding="utf-8"
        )
        timings = response["timings"]
        row = {
            "profile": profile,
            "repeat": repeat,
            "prompt_tokens": timings["prompt_n"],
            "generated_tokens": timings["predicted_n"],
            "prompt_tps": timings["prompt_per_second"],
            "decode_tps": timings["predicted_per_second"],
            "draft_generated": timings["draft_n"],
            "draft_accepted": timings["draft_n_accepted"],
            "draft_acceptance": (
                timings["draft_n_accepted"] / timings["draft_n"]
                if timings["draft_n"]
                else 0.0
            ),
            "wall_seconds": wall_seconds,
        }
        rows.append(row)
        print(json.dumps(row), flush=True)
        time.sleep(3)

(ROOT / "profile-rows.json").write_text(
    json.dumps(rows, indent=2), encoding="utf-8"
)

summary = []
for profile in prompts:
    selected = [row for row in rows if row["profile"] == profile]
    summary.append(
        {
            "profile": profile,
            "prompt_tokens": selected[0]["prompt_tokens"],
            "repeats": len(selected),
            "decode_tps_mean": statistics.mean(row["decode_tps"] for row in selected),
            "decode_tps_min": min(row["decode_tps"] for row in selected),
            "decode_tps_max": max(row["decode_tps"] for row in selected),
            "prompt_tps_mean": statistics.mean(row["prompt_tps"] for row in selected),
            "draft_acceptance_mean": statistics.mean(
                row["draft_acceptance"] for row in selected
            ),
        }
    )

(ROOT / "profile-summary.json").write_text(
    json.dumps(summary, indent=2), encoding="utf-8"
)
print(json.dumps({"summary": summary}, indent=2))
