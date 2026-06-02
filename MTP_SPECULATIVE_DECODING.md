# MTP Speculative Decoding

This is an experimental `llama-server` route for practical local API speed. It is not the same benchmark as the direct non-speculative `llama-bench` headline.

Short version: MTP works on Strix Halo with Vulkan/RADV and current `llama.cpp` master. It improves server generation on the tested Qwen3.6 35B MTP GGUFs. The latest local b9360 run crossed 100 t/s across the six-prompt harness, and the route also has a GMKtec EVO-X2 community reproduction. Keep it separate from direct `llama-bench`: the guide now has a separate Qwen3-30B-A3B-Instruct-2507 IQ4_XS direct 100.04 t/s row, while the Qwen3-Coder direct speed-first row remains 98.51 t/s.

## Current Result

Local rows were measured on the Beelink GTR9 Pro with Mesa/RADV and Qwen3.6 MTP GGUFs. The latest local MTP rerun used `llama.cpp` b9360 / `6b4e4bd58` with Mesa 26.1.1. Community rows are kept separate and marked as GMKtec EVO-X2 reports.

| Model file | Mode | Mean over 6 prompts | Range | Takeaway |
|------------|------|--------------------:|------:|----------|
| Official 35B Q8_0 MTP GGUF | no MTP | 56.20 t/s | 53.35-69.44 | Heavy baseline. |
| Official 35B Q8_0 MTP GGUF | MTP `draft-n=2` | 67.04 t/s | 60.81-75.55 | Best 35B Q8 average; about +19%. |
| Local Q4_K_M requant | no MTP | 74.13 t/s | 72.55-74.56 | Better baseline after reducing model weight. |
| Local Q4_K_M requant | MTP `draft-n=2` | 87.53 t/s | 82.18-95.68 | Best Q4_K_M average; about +18% over Q4_K_M no-MTP. |
| Local Q4_K_M requant | MTP `draft-n=3`, `-t 16`, `--poll 10` | 83.13-84.19 t/s repeats | best prompt 99.86-100.74 | Repeatable single-prompt 100 t/s, but not a broad average claim. |
| `localweights` IQ4_XS-Q8nextn | no MTP | 72.44 t/s | 72.12-72.62 | Published small MTP quant baseline. |
| `localweights` IQ4_XS-Q8nextn | MTP `draft-n=2`, `-t 16`, `--poll 50` | 90.80 t/s | 83.23-100.37 | Previous best broad MTP average before the b9235 rerun. |
| `localweights` IQ4_XS-Q8nextn | MTP `draft-n=3`, `-t 16`, `--poll 10` | 90.27 t/s | 73.81-110.61 | Former single-prompt peak, but less stable. |
| `localweights` IQ4_XS-Q8nextn, b9235 | no MTP | 74.54 t/s | 74.36-74.86 | Latest-stack baseline rerun. |
| `localweights` IQ4_XS-Q8nextn, b9235 | MTP `draft-n=2`, `-t 16`, `--poll 50` | 91.88 t/s | 80.40-100.67 | Latest-stack MTP rerun. |
| `localweights` IQ4_XS-Q8nextn, b9235 | MTP `draft-n=3`, `-t 16`, `--poll 10` | 92.30 t/s | 76.57-109.21 | Former best local Beelink broad MTP average. |
| `localweights` IQ4_XS-Q8nextn, b9334 | no MTP | 74.39 t/s | 70.77-75.14 | Latest no-speculative baseline. |
| `localweights` IQ4_XS-Q8nextn, b9334 | MTP `draft-n=2`, `-t 16`, `--poll 50` | 96.14 t/s | 86.58-107.24 | Clear latest-stack MTP improvement. |
| `localweights` IQ4_XS-Q8nextn, b9334 | MTP `draft-n=3`, `-t 16`, `--poll 100` | **98.57 t/s** | 81.94-116.22 | Former best local Beelink broad MTP average before the b9360 `-ub 1024` rerun. |
| `localweights` IQ4_XS-Q8nextn, b9334 | MTP `draft-n=3`, `-t 16`, `--poll 10` | 98.52 t/s | 82.24-116.75 | Best b9334 single-prompt peak. |
| `localweights` IQ4_XS-Q8nextn, b9334 | MTP `draft-n=4`, `-t 16`, `--poll 50` | 87.89 t/s | 66.66-110.46 | Higher draft depth hurt average stability. |
| `localweights` IQ4_XS-Q8nextn, b9360 | no MTP | 74.88 t/s | 74.82-74.97 | Latest no-speculative baseline. |
| `localweights` IQ4_XS-Q8nextn, b9360 | MTP `draft-n=2`, `-t 16`, `--poll 100`, `-ub 512` | 99.56 t/s | 86.91-108.28 | Very close to 100, but still below it without the ubatch change. |
| `localweights` IQ4_XS-Q8nextn, b9360 | MTP `draft-n=2`, `-t 16`, `--poll 100`, `-ub 1024` | **101.15 t/s** | 88.36-109.87 | First repeated local broad 100+ t/s MTP route; t16 repeats were 101.15 / 101.10 / 101.06. |
| `localweights` IQ4_XS-Q8nextn, b9360 | MTP `draft-n=2`, `-t 12`, `--poll 100`, `-ub 1024` | **101.16 t/s** | 88.29-109.71 | Highest single six-prompt average in the b9360 sweep, essentially tied with t16. |
| `localweights` IQ4_XS-Q8nextn, b9360 | MTP `draft-n=3`, `-t 16`, `--poll 100`, `-ub 1024` | 99.83 t/s | 83.28-117.53 | Higher single-prompt peak, lower broad average than draft-n=2. |
| GMKtec EVO-X2 `localweights` IQ4_XS-Q8nextn, b9235 | no MTP | 74.72 t/s | 65.57-114.89 | Community exact-model baseline from mottledMantis. |
| GMKtec EVO-X2 `localweights` IQ4_XS-Q8nextn, b9235 | MTP `draft-n=2`, `-t 16`, `--poll 50` | **93.29 t/s** | 71.79-161.54 | Best community broad MTP average reported so far. |
| GMKtec EVO-X2 `localweights` IQ4_XS-Q8nextn, b9235 | MTP `draft-n=3`, `-t 16`, `--poll 50` | 93.01 t/s | 68.28-175.97 | Higher single-prompt peak, slightly lower average than `draft-n=2`. |
| Official 27B Q8_0 MTP GGUF, b9235 | no MTP | 7.74 t/s | 7.74-7.75 | Heavy dense route; not a speed candidate. |
| Official 27B Q8_0 MTP GGUF, b9235 | best MTP | 14.59 t/s | 12.70-16.56 | MTP helps, but this stays far slower than the 35B-A3B MoE path. |
| Official 27B Q8_0 MTP GGUF, `de6f727aa` | no MTP | 7.61 t/s | 7.59-7.62 | Latest local build rerun; unchanged practical conclusion. |
| Official 27B Q8_0 MTP GGUF, `de6f727aa` | MTP `draft-n=3`, `--poll 10` | 14.69 t/s | 12.87-16.53 | Slightly faster than the b9235 row, still not a speed route. |

The most honest public summary is:

- **Direct Qwen3-Coder speed row:** Qwen3-Coder Q4_K_S remains 98.51 t/s r50.
- **Separate direct 100 t/s row:** Qwen3-30B-A3B-Instruct-2507 IQ4_XS reached 100.04 t/s r50 direct `llama-bench`; this is a different general-instruct model and quant.
- **Best local MTP server average measured here:** Qwen3.6 MTP IQ4_XS-Q8nextn at about 101.1 t/s across six practical prompts on b9360 with `draft-n=2`, `--poll 100`, and `-ub 1024`.
- **Best community MTP average reported so far:** the same exact route reached 93.29 t/s on mottledMantis' GMKtec EVO-X2.
- **Fastest local MTP server prompt:** Qwen3.6 MTP IQ4_XS-Q8nextn with `draft-n=3`, `-t 16`, `--poll 100`, and `-ub 1024` reached 117.53 t/s on the best b9360 prompt.
- **MTP is still not the direct headline category:** the 101.1 t/s MTP result is `llama-server` speculative decoding, not direct non-speculative `llama-bench`.
- **Official 27B MTP Q8_0 is not a speed route here:** the latest rerun reached 14.69 t/s with MTP, so the useful practical path remains the 35B-A3B MoE MTP quant.

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

Official 27B MTP Q8_0 checked as a negative speed result:

- Source: `ggml-org/Qwen3.6-27B-MTP-GGUF`
- File: `Qwen3.6-27B-MTP-Q8_0.gguf`
- Size: 29,047,083,264 bytes
- SHA256: `9cbd97ae7cf607be58535f5c81600086ce774ae1e10895ab8ca1d8719fe8b74e`

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

Previous best average route with the published IQ4_XS-Q8nextn file:

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

Best current average MTP route found:

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
~/llama-cpp-upstream-2026-05-27-b9360/build-vulkan/bin/llama-server \
  -m ~/benchmark-models/qwen36-mtp-iq4xs-q8nextn/Qwen3.6-35B-A3B-MTP-IQ4_XS-Q8nextn.gguf \
  --host 127.0.0.1 --port 18081 \
  -ngl 999 -fa on --no-mmap --no-mmproj \
  -c 4096 -np 1 -b 2048 -ub 1024 -t 16 --poll 100 \
  --spec-type draft-mtp --spec-draft-n-max 2 \
  --jinja --no-webui
```

## Evidence

- Structured summary: [`data/mtp_speculative.csv`](data/mtp_speculative.csv)
- Raw CSVs, JSONL responses, and server logs:
  - [`data/raw/2026-05-16/mtp-server-qwen36-35b/`](data/raw/2026-05-16/mtp-server-qwen36-35b/)
  - [`data/raw/2026-05-17/mtp-iq4xs-q8nextn/`](data/raw/2026-05-17/mtp-iq4xs-q8nextn/)
  - [`data/raw/2026-05-19/mtp-35b-iq4xs-llamacpp-9235/`](data/raw/2026-05-19/mtp-35b-iq4xs-llamacpp-9235/)
  - [`data/raw/2026-05-19/community-gmktec-mtp-issue18/`](data/raw/2026-05-19/community-gmktec-mtp-issue18/)
  - [`data/raw/2026-05-19/qwen36-27b-mtp-q8-llamacpp-9235/`](data/raw/2026-05-19/qwen36-27b-mtp-q8-llamacpp-9235/)
  - [`data/raw/2026-05-26/latest-llamacpp-b9334/`](data/raw/2026-05-26/latest-llamacpp-b9334/)
  - [`data/raw/2026-05-27/latest-llamacpp-b9360/`](data/raw/2026-05-27/latest-llamacpp-b9360/)
  - [`data/raw/2026-06-01/qwen36-27b-mtp-latest-de6f727/`](data/raw/2026-06-01/qwen36-27b-mtp-latest-de6f727/)
- Upstream MTP support: <https://github.com/ggml-org/llama.cpp/pull/22673>

## Interpretation

Use MTP when you want to test speculative decoding on a real local API server. Do not use the 117.53 t/s local prompt or the 175.97 t/s GMKtec prompt peak as a general "Strix Halo runs every Qwen3.6 workload at 100 t/s" claim. The guide can honestly say that the best measured local Qwen3.6 MTP server route now reaches about 101.1 t/s across six prompts on b9360, while the first GMKtec reproduction reached 93.3 t/s on b9235. The official 27B Q8_0 MTP GGUF is worth documenting as a negative speed result so readers do not chase the wrong route.
