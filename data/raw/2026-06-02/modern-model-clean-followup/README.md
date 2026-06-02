# Modern Model Clean Follow-Up

Short controlled follow-up for the Reddit feedback that the direct 98.51 t/s
Qwen3-Coder 30B row is an older-model speed baseline.

Host state:

- Beelink GTR9 Pro, Ryzen AI MAX+ 395 / Radeon 8060S.
- Kernel `6.19.4-061904-generic`.
- Vulkan/RADV, GPU DPM forced to `high`, CPU EPP `performance`.
- T3 remained active and was preflight-checked.
- Firefox, RustDesk, Ollama, Zoom VM, ffmpeg/docflock, and local dev-server noise were temporarily paused and restored.

## Qwen3-Coder-Next 80B-A3B IQ4_XS

Direct `llama-bench` on llama.cpp `1fd5f4803` / b9467:

```text
llama-bench -m Qwen3-Coder-Next-IQ4_XS.gguf -fa 1 -ngl 999 -mmp 0 -b 2048 -ub 512 -p 512 -n 128 -r 10 -o csv
```

Result:

| Model | Build | pp512 | tg128 | Read |
| --- | --- | ---: | ---: | --- |
| Qwen3-Coder-Next 80B-A3B IQ4_XS | `1fd5f4803` / b9467 | 738.98 +/- 14.96 t/s | 61.91 +/- 0.43 t/s | Modern coding-model row; useful for current-model context, not a replacement for the older 30B speed-first headline. |

## Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn

Repeat of the previous best b9360 MTP server route:

```text
llama-server -m Qwen3.6-35B-A3B-MTP-IQ4_XS-Q8nextn.gguf \
  -ngl 999 -fa on --no-mmap --no-mmproj \
  -c 4096 -np 1 -b 2048 -ub 1024 -t 16 --poll 100 \
  --spec-type draft-mtp --spec-draft-n-max 2 --jinja --no-webui
```

Six-prompt result:

| Metric | t/s |
| --- | ---: |
| Mean | 97.08 |
| Min | 87.35 |
| Max | 106.24 |

Interpretation:

- Code prompts still crossed 100 t/s in this repeat.
- The broad six-prompt average did not reproduce the previous 101.1 t/s run.
- Keep MTP labeled as an experimental server/speculative route, not a simple direct benchmark headline.

## DFlash/PFlash Preflight

Local source trees and cached assets exist for DFlash/PFlash investigation:

- `hec-vllm-awq4-qwen`
- `lucebox-hub`
- cached `z-lab/Qwen3.6-27B-DFlash`
- Docker ROCm development images

This was only a preflight inventory. No DFlash/PFlash performance claim is made here.
