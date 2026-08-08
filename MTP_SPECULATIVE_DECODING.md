# MTP Speculative Decoding

This is an experimental `llama-server` route for practical local API speed. It is not the same benchmark as the direct non-speculative `llama-bench` headline.

Short version: speculative decoding works on Strix Halo with Vulkan/RADV, ROCm/HIP, and current `llama.cpp`/ROCmFPX routes, but it is not automatically faster. It improves server generation on the tested Qwen3.6 35B MTP GGUFs, a matched Gemma 4 26B-A4B QAT assistant-head route, the tuned CHADROCK ACE/SABER ROCmFP4 route, and the new Qwen3-Next 80B MTP route on HIP. The same Qwen3-Next target and sidecar became much slower on Vulkan despite high acceptance, while Gemma 4 31B DFlash was also slower on two synthetic long-prompt shapes. Keep every server/speculative result separate from direct `llama-bench`.

## Current Result

Local rows were measured on the Beelink GTR9 Pro. Historical Qwen3.6 and Gemma rows use Mesa/RADV; CHADROCK rows use the pinned `ciru-ai/ROCmFPX` helper runner at `deaa996`. The 2026-08-09 Qwen3-Next qualification uses the same b10330 main model, MTP sidecar, prompts, and deterministic output checks on both Mesa/RADV and ROCm 7.14. Community rows are kept separate and marked as GMKtec or Nimo reports.

### Qwen3-Next 80B Backend Crossover On b10330

This matched A/B is intentionally shown separately from the historical six-prompt leaderboard. It used two prompt shapes, three repeats each, 128 generated tokens, and normal low-load workstation conditions.

| Backend / policy | Short decode | 3K-prompt decode | Draft acceptance | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Vulkan/RADV direct | 61.33 t/s | 59.16 t/s | n/a | Fastest direct control. |
| Vulkan/RADV MTP `n=4`, `p=0` | 12.37 t/s | 12.58 t/s | 95.8-99.0% | Correct but 78.7-79.8% slower. |
| ROCm/HIP direct | 51.34 t/s | 50.21 t/s | n/a | Slower direct control. |
| ROCm/HIP MTP `n=4`, `p=0` | **83.52 t/s** | **83.60 t/s** | 97.4-99.0% | 62.7-66.5% over matched HIP direct. |

All repeats produced the same observed output hash for a given deterministic prompt. The useful result is therefore a backend crossover, not a universal claim that HIP or MTP is faster. Raw commands, responses, logs, and hashes are in [`data/raw/2026-08-09/qwen3-next-80b-mtp-b10330/`](data/raw/2026-08-09/qwen3-next-80b-mtp-b10330/).

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
| Gemma 4 26B-A4B QAT `UD-Q4_K_XL`, ac4cddeb0 | no MTP | 73.96 t/s | 73.63-74.13 | Direct server baseline for the matched-head Gemma route. |
| Gemma 4 26B-A4B QAT `UD-Q4_K_XL` + matched `Q4_0` MTP head, ac4cddeb0 | MTP `draft-n=2`, `--poll 50`, `-ub 512` | 106.88 t/s | 92.91-119.08 | First local Gemma 4 26B-A4B QAT MTP six-prompt pass; mean acceptance 0.7385. |
| Gemma 4 26B-A4B QAT `UD-Q4_K_XL` + matched `Q4_0` MTP head, ac4cddeb0 | MTP `draft-n=3`, `--poll 50`, `-ub 512` | 109.98 t/s | 93.62-126.39 | Best sweep setting before repeat; mean acceptance 0.6817. |
| Gemma 4 26B-A4B QAT `UD-Q4_K_XL` + matched `Q4_0` MTP head, ac4cddeb0 | MTP `draft-n=3`, `--poll 50`, `-ub 512` repeat | **110.00 t/s** | 93.57-127.33 | Best repeat-confirmed Gemma MTP average; server/speculative result. |
| Gemma 4 26B-A4B QAT `UD-Q4_K_XL` + matched `Q4_0` MTP head, ac4cddeb0 | MTP `draft-n=3`, `--poll 50`, `-ub 512` cold repeat | **102.69 t/s** | 86.76-118.77 | Cold repeat after stopping nonessential docflock/VM workload while leaving T3 and Hermes untouched; confirms useful 100+ t/s-class route but shows cold/warm variability. |
| Gemma 4 26B-A4B QAT `UD-Q4_K_XL` + matched `Q4_0` MTP head, ac4cddeb0 | MTP `draft-n=3`, `--poll 50`, `-ub 512` T3-only repeat | **107.42 t/s** | 91.30-124.71 | Repeat after stopping Hermes/Ollama/RustDesk/docflock/VM/browser-class noise while leaving T3 running; shows the 110 t/s best repeat is mainly host-workload sensitive, not a different route. |
| Gemma 4 31B QAT Q4_0, b10066 | no speculative decoding, 5,471 prompt tokens | 10.30 t/s | 10.26-10.35 | Three-repeat autoregressive server baseline; separate direct row was 11.38 tg128. |
| Gemma 4 31B QAT Q4_0 + matched Q8_0 DFlash, b10066 | DFlash `n_max=8`, 5,471 prompt tokens | 9.73 t/s | 9.12-10.22 | Mean draft acceptance 14.12%; 5.54% slower than matched no-spec. |
| Gemma 4 31B QAT Q4_0, b10066 | no speculative decoding, 21,855 prompt tokens | 9.40 t/s | 9.33-9.46 | Three-repeat autoregressive long-prompt baseline. |
| Gemma 4 31B QAT Q4_0 + matched Q8_0 DFlash, b10066 | DFlash `n_max=8`, 21,855 prompt tokens | 7.48 t/s | 7.40-7.58 | Mean draft acceptance 10.91%; 20.42% slower than matched no-spec. |
| CHADROCK ACE/SABER 35B ROCmFP4, ROCmFPX `deaa996` | MTP `n_max=4`, `p_min=0.25`, exact 3946-token reference profile, gen512 | **141.37 t/s** | 140.84-141.79 | Three-repeat mean with 100% draft acceptance. Fastest repeat-confirmed reference profile; not a universal 4K speed. |
| CHADROCK ACE/SABER 35B ROCmFP4, ROCmFPX `deaa996` | MTP `n_max=4`, `p_min=0.25`, gen2048 check | 127.77 t/s | 127.77 | Same 3946-token prompt with longer generation; 1595/1753 draft tokens accepted. |
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
- **Best current-model Gemma MTP route measured here:** Gemma 4 26B-A4B QAT with a matched MTP head at 102.69 t/s cold repeat, 107.42 t/s T3-only repeat, and 110.00 t/s best repeat across the same six-prompt harness on ac4cddeb0.
- **Fastest repeat-confirmed local MTP server profile:** CHADROCK ACE/SABER 35B ROCmFP4 through `ciru-ai/ROCmFPX` averaged 141.37 t/s over three exact reference-profile repeats, but the 1K and 8K profiles averaged only 78.00 and 83.85 t/s as acceptance fell. This is prompt-shape-specific rather than a broad six-prompt average.
- **Current Qwen3-Next 80B MTP profile:** b10330 ROCm/HIP reached 83.52-83.60 t/s and improved 62.7-66.5% over its matched HIP control. The same sidecar fell to 12.37-12.58 t/s on Vulkan, so this is backend-specific evidence rather than a generic MTP recommendation.
- **Largest first-party MTP agent route:** Step 3.7 Flash ROCmFPX Q3 QualityPlus, a 198B-total / about 11B-active target plus separate Q8 draft, measured 34.50 t/s at 4K and 33.83 t/s at 16K. MTP improved the matched 4K server baseline by 44.68%; 256K allocation and native tool-call smokes passed.
- **Best community MTP average reported so far:** the same exact route reached 93.29 t/s on mottledMantis' GMKtec EVO-X2.
- **Fastest local MTP server prompt:** Qwen3.6 MTP IQ4_XS-Q8nextn with `draft-n=3`, `-t 16`, `--poll 100`, and `-ub 1024` reached 117.53 t/s on the best b9360 prompt.
- **MTP is still not the direct headline category:** the 101.1 t/s MTP result is `llama-server` speculative decoding, not direct non-speculative `llama-bench`.
- **Official 27B MTP Q8_0 is not a speed route here:** the latest rerun reached 14.69 t/s with MTP, so the useful practical path remains the 35B-A3B MoE MTP quant.

## Why This Matters

MTP is valuable because it can improve real `llama-server` generation, not because it automatically raises every direct `llama-bench` number. The speedup depends on draft-token acceptance rate, prompt shape, generation length, quantization, and server flags.

The Qwen3-Next A/B adds backend implementation to that list. High draft acceptance did not rescue the Vulkan route, while the matched HIP route accelerated strongly and preserved the observed deterministic output. Select and benchmark the complete target/draft/backend combination instead of treating the model card or acceptance percentage as sufficient evidence.

The Gemma 4 QAT repeats also show that single-stream server/MTP speed is sensitive to host workload. The same route measured 102.69 t/s with T3 and Hermes left running after stopping docflock/VM noise, 107.42 t/s with only T3 left among the known local services, and 110.00 t/s in the best repeat. CHADROCK has a different sensitivity: the exact 3946-token profile averaged 141.37 t/s at 100% acceptance, while the 984- and 7893-token profiles averaged 78.00 and 83.85 t/s at 41.93% and 51.28% acceptance. For public claims, use the exact profile and acceptance rather than only the highest number.

The official Gemma 4 31B DFlash scout reinforces that rule. The sidecar loaded and both server profiles produced the correct native calculator tool call, but the synthetic 5.5K and 21.9K prompt shapes only accepted about 14% and 11% of drafted tokens. The speculative profile therefore lost speed instead of gaining it. A sidecar being supported is not enough; benchmark the intended workload and publish acceptance with throughput.

Step 3.7 demonstrates the capacity side of MTP. Its 4K uplift was large and acceptance stayed at 99.61-100% through the repeat-confirmed 4K/16K profiles, but absolute decode was lower because the target is a 198B sparse agent model. Use this route to answer whether a frontier-size target, draft, long context, and tools fit together on one box, not to compete with 35B speed profiles.

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

Gemma 4 26B-A4B QAT matched-head route:

- Main source: `unsloth/gemma-4-26b-a4b-it-qat-GGUF`
- Main file: `gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf`
- Draft file: `gemma-4-26B-A4B-it-Q4_0-MTP.gguf`
- Build: `llama.cpp` ac4cddeb0 build 9592
- Status: first-party Beelink `llama-server` route with direct baseline, no-spec server baseline, warm MTP repeat, and cold MTP repeat. This is not an Atomic TurboQuant community row and not direct `llama-bench`.

Gemma 4 31B official QAT and DFlash route:

- Target source: `ggml-org/gemma-4-31B-it-GGUF`, official Google QAT Q4_0 target.
- Draft source: matched `dflash-gemma-4-31B-it-Q8_0.gguf` from the same GGUF repository, derived from `z-lab/gemma-4-31B-it-DFlash`.
- Projector: matched `mmproj-gemma-4-31B-it-Q8_0.gguf`.
- Build: official `llama.cpp` b10066 (`86a9c79f8`) with Vulkan/RADV.
- Status: text, vision, native tool call, direct `llama-bench`, and matched no-spec/DFlash server comparison completed. DFlash is currently a workload-specific negative result, not a recommended speed profile. [`raw evidence`](data/raw/2026-07-18/gemma4-31b-qat-dflash-b10066/)

Step 3.7 Flash capacity/agent route:

- Main source: `jcbtc/Step-3.7-Flash-ROCmFPX-Q3-QualityPlus` at `fa311ca5a82bf82a2338151c4790e3f659abd88d`
- Draft source: `notSnix/Step-3.7-Flash-MTP-Draft-GGUF` at `c7bc8526b2b7004ce045112edebdf13a9eceb7eb`
- Runner: `ciru-ai/ROCmFPX` at `221402af8574faf652b101b6afe225a3f329561f`
- Status: first-party Beelink no-spec/MTP server comparison, 4K/16K/48K profiles, 256K allocation proof, and native tool-call smoke. Advanced server route, not direct `llama-bench`.

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

Best Gemma 4 26B-A4B QAT MTP route found:

```bash
AMD_VULKAN_ICD=RADV \
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json \
~/llama-cpp-latest/build-vulkan-20260611/bin/llama-server \
  -m ~/benchmark-models/gemma-4-26b-a4b-it-qat-unsloth-udq4kxl/gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf \
  --host 127.0.0.1 --port 18081 \
  -ngl 999 -fa on --no-mmap --cache-ram 0 \
  -c 4096 -np 1 -b 2048 -ub 512 --poll 50 \
  --spec-type draft-mtp \
  -md ~/benchmark-models/gemma-4-26b-a4b-it-qat-unsloth-udq4kxl/MTP/gemma-4-26B-A4B-it-Q4_0-MTP.gguf \
  --spec-draft-n-max 3
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
  - [`data/raw/2026-06-11/gemma4-26b-qat-mtp-sixprompt-ac4cddeb/`](data/raw/2026-06-11/gemma4-26b-qat-mtp-sixprompt-ac4cddeb/)
  - [`data/raw/2026-06-12/gemma4-26b-qat-mtp-cold-repeat-ac4cddeb/`](data/raw/2026-06-12/gemma4-26b-qat-mtp-cold-repeat-ac4cddeb/)
  - [`data/raw/2026-06-12/gemma4-26b-qat-mtp-t3-only-repeat-ac4cddeb/`](data/raw/2026-06-12/gemma4-26b-qat-mtp-t3-only-repeat-ac4cddeb/)
  - [`data/raw/2026-06-21/rocmfpx-chadrock-ace-saber-helper-repro/`](data/raw/2026-06-21/rocmfpx-chadrock-ace-saber-helper-repro/)
  - [`data/raw/2026-07-16/step37-rocmfpx-q3-qualityplus/`](data/raw/2026-07-16/step37-rocmfpx-q3-qualityplus/)
- Upstream MTP support: <https://github.com/ggml-org/llama.cpp/pull/22673>

## Interpretation

Use MTP when you want to test speculative decoding on a real local API server. Do not use the 117.53 t/s local Qwen prompt, the 175.97 t/s GMKtec prompt peak, the 127.33 t/s Gemma prompt peak, or the 141.37 t/s CHADROCK reference profile as a general "Strix Halo runs every workload at that speed" claim. The guide can honestly say that the best measured local Qwen3.6 MTP server route reaches about 101.1 t/s across six prompts on b9360, the Gemma 4 26B-A4B QAT route reaches 102.7-110.0 t/s across the same six-prompt harness depending on host workload and repeat condition, and the tuned CHADROCK/ROCmFPX lane reaches 141.37 t/s on one exact repeat-confirmed, 100%-acceptance reference profile. Separately, Step 3.7 proves a 198B sparse agent target plus draft can run at 34.50 t/s at 4K and allocate 256K context on one 128GB box. The official 27B Q8_0 and NVFP4 MTP routes are worth documenting as negative speed results so readers do not chase the wrong route.
