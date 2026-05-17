# MTP Speculative Decoding

This is an experimental `llama-server` route for practical local API speed. It is not the same benchmark as the direct non-speculative `llama-bench` headline.

Short version: MTP works on Strix Halo with Vulkan/RADV and current `llama.cpp` master. It improves server generation on the tested Qwen3.6 35B MTP GGUFs, but the broad average still does not replace the 98.51 t/s direct Qwen3-Coder headline.

## Current Result

Measured on the Beelink GTR9 Pro with `llama.cpp` b9187 / `0253fb21`, Mesa/RADV 26.0.6, and Qwen3.6 35B-A3B MTP GGUFs:

| Model file | Mode | Mean over 6 prompts | Range | Takeaway |
|------------|------|--------------------:|------:|----------|
| Official Q8_0 MTP GGUF | no MTP | 56.20 t/s | 53.35-69.44 | Heavy baseline. |
| Official Q8_0 MTP GGUF | MTP `draft-n=2` | 67.04 t/s | 60.81-75.55 | Best Q8 average; about +19%. |
| Local Q4_K_M requant | no MTP | 74.13 t/s | 72.55-74.56 | Better baseline after reducing model weight. |
| Local Q4_K_M requant | MTP `draft-n=2` | 87.53 t/s | 82.18-95.68 | Best Q4_K_M average; about +18% over Q4_K_M no-MTP. |
| Local Q4_K_M requant | MTP `draft-n=3`, `-t 16`, `--poll 10` | 83.13-84.19 t/s repeats | best prompt 99.86-100.74 | Repeatable single-prompt 100 t/s, but not a broad average claim. |
| `localweights` IQ4_XS-Q8nextn | no MTP | 72.44 t/s | 72.12-72.62 | Published small MTP quant baseline. |
| `localweights` IQ4_XS-Q8nextn | MTP `draft-n=2`, `-t 16`, `--poll 50` | **90.80 t/s** | 83.23-100.37 | Best broad MTP average measured here. |
| `localweights` IQ4_XS-Q8nextn | MTP `draft-n=3`, `-t 16`, `--poll 10` | 90.27 t/s | 73.81-110.61 | Fastest single prompt, but less stable. |

The most honest public summary is:

- **Direct speed headline remains:** Qwen3-Coder Q4_K_S at 98.51 t/s r50.
- **Best MTP server average measured here:** Qwen3.6 MTP IQ4_XS-Q8nextn at about 90.8 t/s across six practical prompts.
- **Fastest local MTP server prompt:** Qwen3.6 MTP IQ4_XS-Q8nextn with `draft-n=3`, `-t 16`, `--poll 10` reached 110.61 t/s on the best prompt, but the same run averaged about 90.3 t/s across the full prompt set.
- **Still not a broad 100 t/s claim:** the best six-prompt average stayed below 100 t/s.

## Why This Matters

MTP is valuable because it can improve real `llama-server` generation, not because it automatically raises every direct `llama-bench` number. The speedup depends on draft-token acceptance rate, prompt shape, generation length, quantization, and server flags.

For beginners: keep using the main README setup first. Treat MTP as an advanced route if you specifically want to experiment with speculative decoding in a local API server.

## Model Provenance

Downloaded model:

- Source: `ggml-org/Qwen3.6-35B-A3B-MTP-GGUF`
- File: `Qwen3.6-35B-A3B-MTP-Q8_0.gguf`
- Size: 37,801,096,544 bytes
- SHA256: `5f24078b0ec9186811834fe229edd71c6cd1e861d6586137d08510ef648126ce`

Local test quant:

- File: `Qwen3.6-35B-A3B-MTP-Q4_K_M.gguf`
- Created with `llama-quantize --allow-requantize` from the official Q8_0 GGUF
- Size: 21,712,409,952 bytes
- SHA256: `be11d472527e5013290b09c1afc12694a326a4184eb97cf58fff579a671dddc3`

Because the Q4_K_M file is a local requant from Q8_0, do not treat it as an upstream-published model file.

Published small MTP quant:

- Source: `localweights/Qwen3.6-35B-A3B-MTP-IQ4_XS-Q8nextn-GGUF`
- File: `Qwen3.6-35B-A3B-MTP-IQ4_XS-Q8nextn.gguf`
- Size: 19,393,459,552 bytes
- SHA256: `4d2349305663bc59bacab26d8eba8ed1218de84b8d1f0456208037e13efa9a98`

## Best Commands Tested

Baseline Q4_K_M server:

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
~/llama-cpp-master-0253/build-vulkan/bin/llama-server \
  -m ~/benchmark-models/qwen36-mtp/Qwen3.6-35B-A3B-MTP-Q4_K_M.gguf \
  --host 127.0.0.1 --port 18081 \
  -ngl 999 -fa on --no-mmap --no-mmproj \
  -c 4096 -np 1 -b 2048 -ub 512 -t 15 --poll 50 \
  --jinja --no-webui
```

Best Q4_K_M MTP server route:

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
~/llama-cpp-master-0253/build-vulkan/bin/llama-server \
  -m ~/benchmark-models/qwen36-mtp/Qwen3.6-35B-A3B-MTP-Q4_K_M.gguf \
  --host 127.0.0.1 --port 18081 \
  -ngl 999 -fa on --no-mmap --no-mmproj \
  -c 4096 -np 1 -b 2048 -ub 512 -t 15 --poll 50 \
  --spec-type draft-mtp --spec-draft-n-max 2 --spec-draft-ngl 999 \
  --jinja --no-webui
```

Best average route with the published IQ4_XS-Q8nextn file:

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
~/llama-cpp-master-0253/build-vulkan/bin/llama-server \
  -m ~/benchmark-models/qwen36-mtp-iq4xs-q8nextn/Qwen3.6-35B-A3B-MTP-IQ4_XS-Q8nextn.gguf \
  --host 127.0.0.1 --port 18081 \
  -ngl 999 -fa on --no-mmap --no-mmproj \
  -c 4096 -np 1 -b 2048 -ub 512 -t 16 --poll 50 \
  --spec-type draft-mtp --spec-draft-n-max 2 \
  --jinja --no-webui
```

Fastest single-prompt MTP route found:

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
~/llama-cpp-master-0253/build-vulkan/bin/llama-server \
  -m ~/benchmark-models/qwen36-mtp-iq4xs-q8nextn/Qwen3.6-35B-A3B-MTP-IQ4_XS-Q8nextn.gguf \
  --host 127.0.0.1 --port 18081 \
  -ngl 999 -fa on --no-mmap --no-mmproj \
  -c 4096 -np 1 -b 2048 -ub 512 -t 16 --poll 10 \
  --spec-type draft-mtp --spec-draft-n-max 3 \
  --jinja --no-webui
```

## Evidence

- Structured summary: [`data/mtp_speculative.csv`](data/mtp_speculative.csv)
- Raw CSVs, JSONL responses, and server logs:
  - [`data/raw/2026-05-16/mtp-server-qwen36-35b/`](data/raw/2026-05-16/mtp-server-qwen36-35b/)
  - [`data/raw/2026-05-17/mtp-iq4xs-q8nextn/`](data/raw/2026-05-17/mtp-iq4xs-q8nextn/)
- Upstream MTP support: <https://github.com/ggml-org/llama.cpp/pull/22673>

## Interpretation

Use MTP when you want to test speculative decoding on a real local API server. Do not use the 110.61 t/s prompt as a general "Strix Halo runs Qwen3.6 at 100 t/s" claim. The guide can honestly say that MTP exceeded 100 t/s on favorable server prompts, while the best measured practical six-prompt average stayed around 90.8 t/s.
