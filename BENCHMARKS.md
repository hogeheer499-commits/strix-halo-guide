# Benchmark Results - Current Snapshot

This file is the compact benchmark source-of-truth for numbers already published in the README. It reconciles historical and current measurements so old ROCm, driver, serving, and long-context notes do not contradict the current guide.

## Current System Snapshot

Latest live audit on 2026-06-01:

| Component | Current State |
|-----------|---------------|
| System | Beelink GTR9 Pro |
| CPU | AMD Ryzen AI MAX+ 395, 16C/32T |
| GPU | Radeon 8060S, gfx1151, RADV STRIX_HALO |
| RAM | 124GiB OS-visible unified memory |
| Kernel | 6.19.4-061904-generic |
| Mesa RADV | 26.1.1, kisak-mesa PPA |
| Ollama | 0.23.1 |
| AMDVLK | Removed |
| linux-firmware | 20240318.git3b128b60-0ubuntu2.27 |
| GPU clock | 2900 MHz selected |
| tuned | `accelerator-performance` active |

Historical benchmark runs below were measured on 2026-03-20, 2026-03-21, and 2026-04-26 with `tuned accelerator-performance` active. The 2026-05-07 latest-stack rerun confirms `tuned accelerator-performance` active, Mesa RADV 26.0.6, AMDVLK absent, linux-firmware safe, GPU clock at 2900 MHz, llama.cpp b9049, and Ollama 0.23.1. The 2026-05-16 spot check tested llama.cpp b9172 and an isolated Ollama 0.24.0 binary without changing the installed Ollama service. The 2026-05-26 spot check used Mesa RADV 26.1.1 and llama.cpp b9334. The 2026-05-27 spot check used the same Mesa/RADV stack and llama.cpp b9360. The 2026-05-31 spot check tested latest llama.cpp b9442 for the direct Qwen3-Coder speed-first path and found no new headline. The 2026-06-01 spot check updated the same latest-stack worktree to `de6f727aa` and again found no new direct headline.

## Top-Line Model Results

| Model | Backend / Build | Quant | pp512 | tg128 | Notes |
|-------|-----------------|-------|-------|-------|-------|
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9179 | Q4_K_S | 1396 | **98.51** | 2026-05-16 strict-clean r50 speed-first quant confirmation |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9453-7 | Q4_K_S | 1384 | 95.55 | Latest direct rerun; no new headline versus b9179 |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9442 | Q4_K_S | 1376 | 93.85 | Latest direct rerun; no new headline versus b9179 |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9360 | Q4_K_S | 1409 | 97.23 | Latest direct rerun; better than b9334 but no new direct headline |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9334 | Q4_K_S | 1401 | 96.27 | Latest direct rerun; no new headline versus b9179 |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9049 | UD-Q4_K_XL | 1321 | **96.76** | Max-performance guide-flags r20 confirmation; balanced UD default |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9360 | UD-Q4_K_XL | 1399 | 92.60 | Latest direct balanced-UD rerun; no new headline |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9334 | UD-Q4_K_XL | 1402 | 94.15 | Latest direct balanced-UD rerun; no new headline |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9179 | Q4_K_S | 1387 | **97.22** | Earlier 2026-05-16 speed-first quant sweep before strict host-state fix |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b9010 | UD-Q4_K_XL | 1346 | **97.24** | Previous May peak |
| Qwen3-Coder 30B-A3B | Vulkan RADV, llama.cpp b8460 | UD-Q4_K_XL | 1342 | **87.11** | Previous coding MoE headline |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b9049 | Q4_0 | 1244 | **81.30** | Fastest measured speed-first quant; lower-quality tradeoff |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b9049 | Q4_K_M | 1106 | **76.94** | Fast balanced Strix quant candidate |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b9049 | UD-Q4_K_M | 1059 | **62.56** | Clean latest-stack rerun |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b9010 | UD-Q4_K_M | 1109 | **63.06** | Previous May UD rerun |
| Qwen3.6 35B-A3B | Vulkan RADV, llama.cpp b8460 | Q4_K_M | 1064 | **63.76** | Recommended all-rounder |
| Qwen3.5 35B-A3B | Vulkan RADV, llama.cpp b8460 | Q4_K_M | 1080 | **64.85** | Used for backend/build comparison |
| gpt-oss-120b | Vulkan RADV, llama.cpp b9049 | MXFP4 MoE | 727 | **55.57** | 117B-parameter open-weight MoE loaded from split GGUF |
| Qwen3-Next 80B-A3B | Vulkan RADV, llama.cpp b9172 | UD-Q4_K_XL | 752 | **59.06** | Latest-stack r20 confirmation; best current 80B Qwen-family path |
| Qwen3-Next 80B-A3B | Vulkan RADV, llama.cpp b8933 | UD-Q4_K_XL | 657 | **54.92** | 80B MoE, 256K context capable |
| Gemma 4 26B-A4B | Vulkan RADV, llama.cpp b8933 | UD-Q4_K_M | 1142 | **48.46** | Slower than Qwen MoE at similar active params |
| Llama 4 Scout 109B | Vulkan RADV, llama.cpp b8933 | Q4_K_M | 331 | **18.32** | 109B params on one mini PC |
| Llama 3.1 70B | Ollama Vulkan RADV | Q4_K_M | 22-80 | **4.7-4.9** | Dense 70B, bandwidth-bound |
| Qwen3 0.6B | Vulkan RADV, llama.cpp | Q8_0 | 13112 | **266** | Small-model speed ceiling |

## 2026-06-01 Latest de6f727 Direct Spot Check

Measured on the same Beelink GTR9 Pro after a clean pass that left T3 running and stopped RustDesk, DocFlock/ffmpeg, Ollama, and the Zoom VM. Raw data lives under [`data/raw/2026-06-01/latest-llamacpp-de6f727-safe-clean/`](data/raw/2026-06-01/latest-llamacpp-de6f727-safe-clean/).

| Route | Result | Read |
|-------|--------|------|
| llama.cpp `de6f727aa` (`b9453-7`), Qwen3-Coder 30B Q4_K_S direct `llama-bench`, `mmap=0` | 95.55 tg128, 1384.30 pp512 | Latest upstream did not beat the existing b9179 98.51 t/s speed-first headline. |
| Same run with default `mmap=1` | 94.20 tg128, 1371.77 pp512 | Slightly slower in this check; kept as raw evidence only. |

Takeaway: latest `de6f727aa` did not create a new direct Qwen3-Coder headline. The direct speed-first headline remains the older strict-clean b9179 r50 row at 98.51 t/s.

## 2026-05-31 Latest b9442 Direct Spot Check

Measured on the same Beelink GTR9 Pro after a safe-clean pass that left T3 running. Raw data lives under [`data/raw/2026-05-31/`](data/raw/2026-05-31/).

| Route | Result | Read |
|-------|--------|------|
| llama.cpp b9442, Qwen3-Coder 30B Q4_K_S direct `llama-bench` | 93.85 tg128, 1376.37 pp512 | Latest upstream did not beat the existing b9179 98.51 t/s speed-first headline. |
| Same-state b9360 Qwen3-Coder 30B Q4_K_S control | 95.35 tg128, 1384.21 pp512 | Same host state also stayed below the earlier b9360 97.23 t/s r20 row, so do not promote this as a regression claim without more repeats. |
| Same-state b9187 Qwen3-Coder 30B Q4_K_S `-t 15` control | 95.09 tg128, 1388.21 pp512 | Older near-99 scout route did not reproduce a higher result in this short control run. |

Takeaway: latest b9442 did not create a new direct Qwen3-Coder headline. These are useful negative/control rows only; the direct speed-first headline remains the older strict-clean b9179 r50 row at 98.51 t/s.

## 2026-05-27 Latest b9360 Spot Check

Measured on the same Beelink GTR9 Pro after pausing benchmark noise while leaving the normal workspace dependency running. Raw data lives under [`data/raw/2026-05-27/latest-llamacpp-b9360/`](data/raw/2026-05-27/latest-llamacpp-b9360/).

| Route | Result | Read |
|-------|--------|------|
| llama.cpp b9360, Qwen3-Coder 30B Q4_K_S direct `llama-bench` | 97.23 tg128, 1408.59 pp512 | Better than b9334 direct, but still below the b9179 98.51 t/s strict-clean row. |
| llama.cpp b9360, Qwen3-Coder 30B UD-Q4_K_XL direct `llama-bench` | 92.60 tg128, 1398.69 pp512 | No new balanced headline; below the b9049/b9010 96-97 t/s rows. |
| llama.cpp b9360, Qwen3.6 35B MTP IQ4_XS-Q8nextn, no MTP | 74.88 t/s average over six prompts | Current no-speculative server baseline. |
| llama.cpp b9360, Qwen3.6 35B MTP IQ4_XS-Q8nextn, `draft-n=2`, `-ub 512` | 99.56 t/s best default-ubatch average; best prompt 108.28 t/s | Very close to 100 t/s, but still below it without the ubatch change. |
| llama.cpp b9360, Qwen3.6 35B MTP IQ4_XS-Q8nextn, `draft-n=2`, `-ub 1024` | **101.16 t/s** best six-prompt average; t16 repeats **101.15 / 101.10 / 101.06 t/s** | First repeated local broad 100+ t/s MTP server route. |
| llama.cpp b9360, Qwen3.6 35B MTP IQ4_XS-Q8nextn, `draft-n=3`, `-ub 1024` | 99.83 t/s average; best prompt 117.53 t/s | Higher single-prompt peak, lower broad average than draft-n=2. |

Takeaway: latest b9360 did not improve the direct Qwen3-Coder headline, but it did create the first repeat-confirmed local MTP server route above 100 t/s across the six-prompt harness. Keep these categories separate: direct `llama-bench` remains 98.51 t/s speed-first / 96-97 t/s balanced, while MTP is now about 101.1 t/s as an advanced server/speculative route.

## 2026-05-26 Latest b9334 Spot Check

Measured on the same Beelink GTR9 Pro after pausing benchmark noise while leaving the normal workspace dependency running. Raw data lives under [`data/raw/2026-05-26/latest-llamacpp-b9334/`](data/raw/2026-05-26/latest-llamacpp-b9334/).

| Route | Result | Read |
|-------|--------|------|
| llama.cpp b9334, Qwen3-Coder 30B Q4_K_S direct `llama-bench` | 96.27 tg128, 1401.20 pp512 | No new direct headline; slower than the b9179 98.51 t/s strict-clean row. |
| llama.cpp b9334, Qwen3-Coder 30B UD-Q4_K_XL direct `llama-bench` | 94.15 tg128, 1402.17 pp512 | No new balanced headline; below the b9049/b9010 96-97 t/s rows. |
| Same-state b9179 Qwen3-Coder Q4_K_S control | 97.61 tg128, 1409.36 pp512 | Confirms b9334 itself did not improve direct generation in this check. |
| llama.cpp b9334, Qwen3.6 35B MTP IQ4_XS-Q8nextn, no MTP | 74.39 t/s average over six prompts | Current no-speculative server baseline. |
| llama.cpp b9334, Qwen3.6 35B MTP IQ4_XS-Q8nextn, `draft-n=2` | 96.14 t/s average; best prompt 107.24 t/s | Strong improvement over b9235 draft-n=2. |
| llama.cpp b9334, Qwen3.6 35B MTP IQ4_XS-Q8nextn, `draft-n=3` | **98.57 t/s** best six-prompt average; best prompt **116.75 t/s** | Former best local MTP route before the b9360 `-ub 1024` rerun. |
| llama.cpp b9334, Qwen3.6 35B MTP IQ4_XS-Q8nextn, `draft-n=4` | 87.89 t/s average | Higher draft depth hurt average stability. |
| llama.cpp b9334, synthetic512/ignore-EOS MTP variant | 93.93 t/s average | Synthetic prompt variant did not improve the broad average. |

Takeaway: latest b9334 did not improve the direct Qwen3-Coder headline, but it materially improved the experimental MTP server path. It was later superseded by the b9360 MTP rerun at about 101.1 t/s. Keep these categories separate: direct `llama-bench` remains 98.51 t/s speed-first / 96-97 t/s balanced.

## 2026-05-16 Latest-Stack Spot Check

Measured on the same Beelink GTR9 Pro after pausing non-essential GUI/noise processes while leaving the normal workspace session active. Raw data lives under [`data/raw/2026-05-16/`](data/raw/2026-05-16/).

| Route | Result | Read |
|-------|--------|------|
| llama.cpp b9172, Qwen3-Coder 30B UD-Q4_K_XL | 94.43-95.05 tg128 depending on batch flags | No new balanced-UD headline; b9049/b9010 remain faster at about 96-97 t/s. |
| llama.cpp b9172, Qwen3.6 UD-Q4_K_M | 61.52 tg128 | No new headline; current b9049/b9010 rows remain stronger. |
| llama.cpp b9172, Qwen3.6 Q4_0 | 79.14 tg128 | No new headline; current b9049 Q4_0 row remains 81.30 t/s. |
| llama.cpp b9172, Qwen3-Next 80B UD-Q4_K_XL | **59.06 tg128**, 751.70 pp512 | New best 80B Qwen-family row; replaces the old 54.92 t/s b8933 headline for this model. |
| llama.cpp b9172, gpt-oss-120b MXFP4 | 54.69 tg128, 718.61 pp512 | No new headline; b9049 remains slightly better at 55.57 t/s. |
| Ollama 0.24.0 isolated binary, Qwen3.6 API | 49.05 t/s warm generation average | No speedup versus the same-prompt Ollama 0.23.1 control at 49.09 t/s. |
| llama.cpp b9179, Qwen3-Coder 30B Q4_K_S/Q4_0/IQ4_NL/Q4_K_M sweep | Initial best row: Q4_K_S at **97.22 tg128**, 1387.22 pp512 | Useful negative result: current master plus smaller Qwen3-Coder quants did not produce a stable 100 t/s path. Raw data: [`qwen3-coder-break100-master`](data/raw/2026-05-16/qwen3-coder-break100-master/). |
| llama.cpp b9179, Qwen3-Coder 30B Q4_K_S strict-clean confirmation | **98.51 tg128 r50**, 1396.11 pp512 | New speed-first peak after fixing `tuned`/`power-profiles-daemon` conflict and pausing RustDesk/Firefox/Zoom/ffmpeg noise. Raw data: [`break-97-24-strict-noise-settings`](data/raw/2026-05-16/break-97-24-strict-noise-settings/). |
| llama.cpp b8275, Qwen3-Coder-Next 80B-A3B IQ4_XS | 61.68 tg128, 735.72 pp512 | Modern Qwen coding-model row added after Reddit feedback. It is useful current-model evidence but not a replacement for the Qwen3-Coder 30B speed-first headline. Raw data: [`qwen3-coder-next-iq4xs`](data/raw/2026-06-02/qwen3-coder-next-iq4xs/). |
| llama.cpp b9187, Qwen3.6 35B MTP IQ4_XS-Q8nextn server route | **90.80 t/s average** over six prompts with `draft-n=2`; best prompt **110.61 t/s** with `draft-n=3`, `-t 16`, `--poll 10` | Previous MTP route and former single-prompt peak, but not a replacement for the direct non-speculative headline or a broad 100 t/s average. Raw data: [`mtp-iq4xs-q8nextn`](data/raw/2026-05-17/mtp-iq4xs-q8nextn/), summary: [`MTP_SPECULATIVE_DECODING.md`](MTP_SPECULATIVE_DECODING.md). |
| llama.cpp b9235, Qwen3.6 35B MTP IQ4_XS-Q8nextn server route | **92.30 t/s average** over six prompts with `draft-n=3`; best prompt **109.21 t/s** | Former local MTP best, later superseded by b9334 at 98.57 t/s and b9360 at about 101.1 t/s. Raw data: [`mtp-35b-iq4xs-llamacpp-9235`](data/raw/2026-05-19/mtp-35b-iq4xs-llamacpp-9235/). |
| Community GMKtec EVO-X2, llama.cpp b9235, Qwen3-Coder 30B UD-Q4_K_XL | 92.11 tg128 generation-only; 1157.29 pp512 / 91.40 tg128 in the full follow-up | Useful portability evidence for the GMKtec/latest-stack path. Not an apples-to-apples replacement for the Beelink headline because the full follow-up used `-b 512 -ub 512`, `flash_attn=0`, and `use_mmap=1`. Raw data: [`community-gmktec-qwen-coder-issue17`](data/raw/2026-05-19/community-gmktec-qwen-coder-issue17/). |
| Community GMKtec EVO-X2, llama.cpp b9235, Qwen3.6 35B MTP IQ4_XS-Q8nextn | **93.29 t/s average** over six prompts with `draft-n=2`; `draft-n=3` reached 93.01 t/s average and 175.97 t/s best prompt | First independent exact-model MTP reproduction. It slightly exceeds the local Beelink b9235 average, but still does not create a broad 100 t/s average claim. Raw data: [`community-gmktec-mtp-issue18`](data/raw/2026-05-19/community-gmktec-mtp-issue18/). |
| llama.cpp b9235, official Qwen3.6 27B MTP Q8_0 | 7.74 t/s baseline; **14.59 t/s** best MTP average | Useful negative result: MTP nearly doubled the official 27B Q8_0 route, but this dense/heavy path is much slower than the 35B-A3B MoE routes and is not a speed candidate. Raw data: [`qwen36-27b-mtp-q8-llamacpp-9235`](data/raw/2026-05-19/qwen36-27b-mtp-q8-llamacpp-9235/). |

Takeaway: upgrading blindly is not always faster. b9172 is worthwhile for Qwen3-Next 80B on this machine. Current master b9179 plus the Qwen3-Coder Q4_K_S speed-first quant can beat the old 97.24 t/s peak under a strict benchmark host state, but still did not produce a reliable direct non-speculative 100 t/s result. The GMKtec Qwen3-Coder follow-up reinforces that command flags such as batch size, flash attention, and mmap must be preserved when comparing rows. MTP on b9187/b9235/b9334/b9360 can exceed 100 t/s on favorable server prompts, and b9360 plus `-ub 1024` now gives a repeat-confirmed local six-prompt average around 101.1 t/s. Keep direct `llama-bench`, server batching, and speculative decoding claims separate.

## MTP Speculative Decoding

Measured with `llama-server` Vulkan/RADV, six `/completion` prompts, `n_predict=192`, `temperature=0`, `top_k=1`, and prompt cache disabled per request. Structured data: [`data/mtp_speculative.csv`](data/mtp_speculative.csv). Raw data: [`data/raw/2026-05-16/mtp-server-qwen36-35b/`](data/raw/2026-05-16/mtp-server-qwen36-35b/), [`data/raw/2026-05-17/mtp-iq4xs-q8nextn/`](data/raw/2026-05-17/mtp-iq4xs-q8nextn/), [`data/raw/2026-05-19/`](data/raw/2026-05-19/), [`data/raw/2026-05-26/latest-llamacpp-b9334/`](data/raw/2026-05-26/latest-llamacpp-b9334/), [`data/raw/2026-05-27/latest-llamacpp-b9360/`](data/raw/2026-05-27/latest-llamacpp-b9360/), and [`data/raw/2026-06-01/qwen36-27b-mtp-latest-de6f727/`](data/raw/2026-06-01/qwen36-27b-mtp-latest-de6f727/).

| Route | Mean t/s | Min-Max | Read |
|-------|---------:|--------:|------|
| Official Qwen3.6 35B MTP Q8_0, no MTP | 56.20 | 53.35-69.44 | Heavy baseline. |
| Official Qwen3.6 35B MTP Q8_0, `draft-n=2` | 67.04 | 60.81-75.55 | Best 35B Q8 average; about +19%. |
| Local Qwen3.6 MTP Q4_K_M requant, no MTP | 74.13 | 72.55-74.56 | Faster baseline from reduced model weight. |
| Local Qwen3.6 MTP Q4_K_M requant, `draft-n=2` | 87.53 | 82.18-95.68 | Best Q4_K_M average; about +18% over the Q4_K_M no-MTP server baseline. |
| Local Qwen3.6 MTP Q4_K_M requant, `draft-n=3`, `-t 16`, `--poll 10` | 83.13-84.19 repeats | best prompt 99.86-100.74 | Repeatable single-prompt 100 t/s result, but lower broad average. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, no MTP | 72.44 | 72.12-72.62 | Published small MTP quant baseline. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, `draft-n=2`, `-t 16`, `--poll 50` | 90.80 | 83.23-100.37 | Previous best broad MTP average before the b9235 rerun. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, `draft-n=3`, `-t 16`, `--poll 10` | 90.27 | 73.81-110.61 | Former single-prompt peak, but not a broad 100 t/s average. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9235, no MTP | 74.54 | 74.36-74.86 | Latest-stack baseline rerun. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9235, `draft-n=2`, `-t 16`, `--poll 50` | 91.88 | 80.40-100.67 | Latest-stack MTP rerun, stronger than the b9187 draft-n=2 average. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9235, `draft-n=3`, `-t 16`, `--poll 10` | 92.30 | 76.57-109.21 | Former best local Beelink broad MTP average. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9334, no MTP | 74.39 | 70.77-75.14 | Latest no-speculative baseline. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9334, `draft-n=2`, `-t 16`, `--poll 50` | 96.14 | 86.58-107.24 | Latest-stack MTP improvement. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9334, `draft-n=3`, `-t 16`, `--poll 100` | **98.57** | 81.94-116.22 | Former best local Beelink broad MTP average before the b9360 `-ub 1024` rerun. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9334, `draft-n=3`, `-t 16`, `--poll 10` | 98.52 | 82.24-116.75 | Best b9334 single-prompt peak. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9360, no MTP | 74.88 | 74.82-74.97 | Latest no-speculative baseline. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9360, `draft-n=2`, `-t 16`, `--poll 100`, `-ub 512` | 99.56 | 86.91-108.28 | Very close, but still below broad 100 t/s. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9360, `draft-n=2`, `-t 16`, `--poll 100`, `-ub 1024` | **101.15** | 88.36-109.87 | First repeated local broad 100+ t/s MTP route; t16 repeats were 101.15 / 101.10 / 101.06. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9360, `draft-n=2`, `-t 12`, `--poll 100`, `-ub 1024` | **101.16** | 88.29-109.71 | Highest single six-prompt average in this b9360 sweep, essentially tied with t16. |
| Qwen3.6 MTP IQ4_XS-Q8nextn, b9360, `draft-n=3`, `-t 16`, `--poll 100`, `-ub 1024` | 99.83 | 83.28-117.53 | Higher prompt peak, lower broad average than draft-n=2. |
| Community GMKtec Qwen3.6 MTP IQ4_XS-Q8nextn, b9235, `draft-n=2`, `-t 16`, `--poll 50` | **93.29** | 71.79-161.54 | First independent exact-model reproduction; best community broad average so far. |
| Community GMKtec Qwen3.6 MTP IQ4_XS-Q8nextn, b9235, `draft-n=3`, `-t 16`, `--poll 50` | 93.01 | 68.28-175.97 | Higher prompt peak, slightly lower broad average than `draft-n=2`. |
| Official Qwen3.6 27B MTP Q8_0, b9235, no MTP | 7.74 | 7.74-7.75 | Heavy dense route; not a speed candidate. |
| Official Qwen3.6 27B MTP Q8_0, b9235, best MTP | 14.59 | 12.70-16.56 | MTP helps, but this route remains far slower than the 35B-A3B MoE path. |
| Official Qwen3.6 27B MTP Q8_0, `de6f727aa`, no MTP | 7.61 | 7.59-7.62 | Latest-stack sanity rerun; still a heavy dense route. |
| Official Qwen3.6 27B MTP Q8_0, `de6f727aa`, `draft-n=3` | 14.69 | 12.87-16.53 | Confirms the negative/control conclusion: MTP helps, but this route is not competitive with 35B-A3B MoE speed. |

Takeaway: MTP is useful for server/speculative experiments and likely worth tracking as `llama.cpp` support matures. The latest local b9360 rerun raises the practical MTP range to about 101.1 t/s on the Beelink when `-ub 1024` is used. Do not write this as a direct `llama-bench` result or as a universal "all Qwen3.6 runs at 100 t/s" claim. The GMKtec reproduction makes the earlier 92-93 t/s route more credible, and the official 27B Q8_0 MTP GGUF is a useful negative speed result here. The 2026-06-01 latest-stack rerun confirmed the same 27B conclusion.

## Qwen3.6 Quant Sweep

Measured 2026-05-07 with llama.cpp b9049 Vulkan/RADV on the Beelink GTR9 Pro. Raw data: [`data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen36-top-confirm-r20/`](data/raw/2026-05-07/max-performance-campaign/benchmarks/qwen36-top-confirm-r20/).

| Quant | pp512 | tg128 | Use |
|-------|------:|------:|-----|
| Q4_0 | 1243.51 | **81.30** | Fastest measured Qwen3.6 row; speed-first, lower-quality tradeoff. |
| Q4_0 with q8 KV | 1229.97 | 79.90 | Slightly slower decode; q8 KV may be useful for some context/memory tradeoffs. |
| IQ4_NL | 1199.41 | 77.29 | Fast candidate; quality sanity needed before recommending broadly. |
| Q4_K_M | 1105.78 | 76.94 | Balanced Strix quant candidate; likely more practical than Q4_0 if quality matters. |
| UD-Q4_K_M | 1059.45 | 62.56 | Older default headline row from the clean latest-stack rerun. |

Takeaway: Qwen3.6 can be pushed well past the old 63 t/s row, but the guide should not hide the quant tradeoff. For beginners, keep "use Qwen3.6 Q4_K_M/UD-Q4_K_M as the all-rounder" and add "use Q4_0 when you want maximum speed and have accepted the quality tradeoff."

## gpt-oss-120b Local Check

Measured 2026-05-07 with llama.cpp b9049 Vulkan/RADV and the `ggml-org/gpt-oss-120b-GGUF` MXFP4 split GGUF. This is a performance/loadability check, not a quality evaluation.

Raw data:

- first load/speed check: [`data/raw/2026-05-07/gpt-oss-120b-local-attempt/`](data/raw/2026-05-07/gpt-oss-120b-local-attempt/)
- clean paused-system long-context rerun: [`data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/)

| Workload | Result | Raw CSV |
|----------|-------:|---------|
| pp512 | 726.99 t/s | [`long-context rerun`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-prefill-512-32768-r3.csv) |
| pp2048 | 728.60 t/s | [`long-context rerun`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-prefill-512-32768-r3.csv) |
| pp8192 | 678.59 t/s | [`long-context rerun`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-prefill-512-32768-r3.csv) |
| pp16384 | 605.21 t/s | [`long-context rerun`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-prefill-512-32768-r3.csv) |
| pp32768 | 478.25 t/s | [`long-context rerun`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-prefill-512-32768-r3.csv) |
| pp65536 | 293.73 t/s | [`pp65536 r1`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-pp65536-r1.csv) |
| tg128 | 55.57 t/s | [`tg128 r20`](data/raw/2026-05-07/max-performance-campaign/benchmarks/gpt-oss-120b-long-context-vulkan/gpt-oss-120b-tg128-r20.csv) |

Takeaway: the 128GB Strix Halo setup can load and run a 117B-parameter open-weight MoE locally at about 55-56 t/s generation on the measured direct Vulkan path. The first tg32 attempt was correctly aborted by the benchmark guard when swap-free dropped under 2 GiB; after clearing swap with ample free RAM, tg32 and tg128 completed. The later paused-system rerun also proves prompt processing through 65K tokens, but the 65K row is one repeat.

## Ollama Vulkan

### Qwen3.6-35B-A3B, Ollama 0.23.1 and isolated 0.24.0, Vulkan RADV

| Prompt Tokens | Prompt Eval | Generation | Notes |
|---------------|-------------|------------|-------|
| 19 | 158 t/s | **50.5 t/s** | Controlled 2026-05-07 API warm average across 10 runs; matches 0.21.2 |
| 25 | 188 t/s | 49.1 t/s | 2026-05-16 same-prompt Ollama 0.23.1 control |
| 25 | 188 t/s | 49.1 t/s | 2026-05-16 isolated Ollama 0.24.0 check; no speedup |
| 20 | 163 t/s | 45.6 t/s | Older result, superseded by controlled API run |
| 22 | 174 t/s | 45.4 t/s | Older result, superseded by controlled API run |

### Historical March Ollama Results

These remain useful as historical data, but they are not the current headline numbers.

| Model | Prompt Tokens | pp (t/s) | tg (t/s) | Notes |
|-------|---------------|----------|----------|-------|
| Qwen3.5 35B-A3B, Ollama 0.20.4 | 14 | 121.3 | **48.0** | Mesa 26.0.2 era |
| Qwen3.5 35B-A3B, Ollama 0.20.4 | 23 | 182.3 | **47.5** | Mesa 26.0.2 era |
| Qwen3.5 35B-A3B, Ollama 0.20.4 | 122 | 456.7 | **47.4** | Mesa 26.0.2 era |
| Qwen3-Coder 30B-A3B Q8_0 | 12 | 118.3 | **51.4** | Ollama path |
| Qwen3-Coder-Next | 120 | 301.2 | **37.9** | Dense 51GB model |
| Qwen2.5-VL 7B | 23 | 81.7 | **21.4** | Vision-language model |

## Multi-User llama-server

### Qwen3.6-35B-A3B UD-Q4_K_M, llama.cpp b9010, Vulkan RADV

This is a serving benchmark, not a single-user `llama-bench` headline. Each row is the average of 3 measured repetitions with streaming `/completion`, 128 generated tokens per request, prompt cache disabled, continuous batching enabled, and about 4096 context tokens per slot.

| `-np` | Concurrent Requests | Aggregate tg | Avg per Request | Mean TTFT | Mean ITL | Notes |
|-------|---------------------|--------------|-----------------|-----------|----------|-------|
| 1 | 1 | 59.21 t/s | 59.21 t/s | 0.117 s | 16.1 ms | Server/API path baseline |
| 2 | 2 | 92.21 t/s | 46.11 t/s | 0.198 s | 20.3 ms | Good scaling |
| 4 | 4 | 130.81 t/s | 32.71 t/s | 0.237 s | 29.0 ms | Strong batching gain |
| 8 | 8 | **161.98 t/s** | 20.25 t/s | 0.307 s | 47.4 ms | Practical sweet spot |
| 16 | 16 | 165.98 t/s | 10.38 t/s | 0.547 s | 92.9 ms | Throughput plateau |

Takeaway: continuous batching makes Strix Halo much more useful as a local API box than single-user numbers imply. `-np 8` gives about 2.7x the `-np 1` aggregate throughput while keeping TTFT near 0.3 seconds. `-np 16` is viable for many low-rate clients, but not faster overall.

### Qwen3-Coder 30B-A3B UD-Q4_K_XL, llama.cpp b9010, Vulkan RADV

| `-np` | Concurrent Requests | Aggregate tg | Avg per Request | Mean TTFT | Mean ITL | Notes |
|-------|---------------------|--------------|-----------------|-----------|----------|-------|
| 1 | 1 | 90.20 t/s | 90.20 t/s | 0.079 s | 10.6 ms | Server/API path baseline |
| 2 | 2 | 121.65 t/s | 60.83 t/s | 0.133 s | 15.5 ms | Good scaling |
| 4 | 4 | 157.41 t/s | 39.36 t/s | 0.207 s | 24.0 ms | Strong batching gain |
| 8 | 8 | **173.16 t/s** | 21.65 t/s | 0.382 s | 43.5 ms | Practical sweet spot |
| 16 | 16 | 129.56 t/s | 8.10 t/s | 0.571 s | 119.9 ms | Regression |

Takeaway: `-np 8` is the best measured setting for Qwen3-Coder serving. `-np 16` regresses, so avoid it for throughput-focused coding workloads.

## Long-Context Prompt Scaling

These rows measure prompt processing at the listed prompt lengths. They do not measure decode speed after a fully occupied KV cache.

| Model | Quant | 4K pp | 8K pp | 16K pp | 32K pp | 64K pp | tg128 row |
|-------|-------|-------|-------|--------|--------|--------|-----------|
| Qwen3.6 35B-A3B | UD-Q4_K_M | 1081.93 | 1089.48 | 1024.58 | 908.61 | 740.25 | 57.84 |
| Qwen3-Next 80B-A3B | UD-Q4_K_XL | 741.68 | 735.50 | 700.49 | 644.82 | 543.89 | 55.58 |

Takeaway: Qwen3.6 retains 68% of its 4K prompt-processing speed at 64K. Qwen3-Next 80B retains 73%, which is a strong result for a 46GB-on-disk 80B MoE model.

## Filled-KV Decode

These rows measure a full `llama-server` request: long prompt ingestion plus 128 generated tokens after the KV cache is filled. Prompt cache was disabled. Prompt content was synthetic and repetitive, so compare within this table rather than against arbitrary real-world documents.

| Model | Prompt | KV | Prompt Eval | Decode After Fill | Wall Time |
|-------|--------|----|-------------|-------------------|-----------|
| Qwen3.6 35B-A3B | 32K | f16 | 1216.64 t/s | 51.00 t/s | 29.50 s |
| Qwen3.6 35B-A3B | 32K | q8_0 | 1023.43 t/s | 54.59 t/s | 34.46 s |
| Qwen3.6 35B-A3B | 32K | q4_0 | 1048.70 t/s | 56.03 t/s | 33.58 s |
| Qwen3.6 35B-A3B | 64K | f16 | 931.89 t/s | 41.44 t/s | 73.52 s |
| Qwen3.6 35B-A3B | 64K | q8_0 | 731.22 t/s | 49.13 t/s | 92.33 s |
| Qwen3.6 35B-A3B | 64K | q4_0 | 750.04 t/s | 51.33 t/s | 89.97 s |
| Qwen3.6 35B-A3B | 128K | f16 | 616.77 t/s | 32.23 t/s | 216.69 s |
| Qwen3-Next 80B-A3B | 32K | f16 | 972.57 t/s | 46.17 t/s | 36.51 s |
| Qwen3-Next 80B-A3B | 64K | f16 | 753.26 t/s | 38.18 t/s | 90.45 s |
| Qwen3-Next 80B-A3B | 128K | f16 | 497.79 t/s | 29.12 t/s | 268.54 s |

Takeaway: q4_0/q8_0 KV cache improves Qwen3.6 decode speed after a filled context, but slows prompt ingestion enough that full first-turn wall time is worse than f16. Use f16 for first-turn long prompts; use q4_0/q8_0 only when memory pressure or long continued generation matters more than ingest speed. The 128K f16 rows completed without truncation.

### Real-Corpus 64K Check

| Model | Prompt Type | Tokens | Prompt Eval | Decode After Fill | Wall Time |
|-------|-------------|--------|-------------|-------------------|-----------|
| Qwen3.6 35B-A3B | synthetic repeated token | 65,533 | 931.89 t/s | 41.44 t/s | 73.52 s |
| Qwen3.6 35B-A3B | real guide corpus | 65,120 | 706.21 t/s | 40.84 t/s | 95.41 s |
| Qwen3-Next 80B-A3B | synthetic repeated token | 65,532 | 753.26 t/s | 38.18 t/s | 90.45 s |
| Qwen3-Next 80B-A3B | real guide corpus | 63,507 | 504.53 t/s | 37.75 t/s | 129.40 s |

Takeaway: synthetic repeated-token prompts are optimistic for prompt-ingest speed. Real guide/documentation text slowed prompt eval by 24-33%, while decode-after-fill barely changed.

## Backend and Build Comparison

### Qwen3.5-35B-A3B Q4_K_M

| Backend / Build | pp512 | tg128 | Takeaway |
|-----------------|-------|-------|----------|
| Ollama Vulkan RADV, bundled older llama.cpp | ~457 | 47.4 | Easy, but slower |
| Vulkan RADV, b8298 | 868 | 52.06 | Baseline kyuz0-era direct path |
| Vulkan RADV, b8460 | **1080** | **64.85** | Best short-context result |
| ROCm HIP, b8301, HSA fix | 1059 | 47.87 | Old self-compiled ROCm build |
| ROCm HIP, b8460, HSA fix | 1047 | 54.67 | ROCm improved, still slower tg than RADV |

### AMDVLK Correction

AMDVLK is not recommended. It was installed during earlier testing and its ICD file silently overrode RADV for some direct `llama-bench` commands. That caused false "RADV regression" conclusions. Corrected current state:

- RADV is the default Vulkan path and wins the measured generation-heavy GGUF rows used for this guide's beginner recommendation.
- ROCm/HIP is not a Vulkan driver and can win prompt-processing-heavy rows, so compare pp and tg separately instead of reducing every backend to one winner.
- AMDVLK should be uninstalled, not just ignored.
- Verify RADV in output: `(RADV STRIX_HALO) (radv)` and `shared memory: 65536`.
- AMDVLK output shows `(AMD open-source driver)` and `shared memory: 32768`.

## ROCm Status

ROCm is no longer "all broken" on kernel 6.19.x. It works when both environment variables are set before running ROCm/HIP binaries:

```bash
export HSA_OVERRIDE_GFX_VERSION=11.5.1
export HSA_ENABLE_SDMA=0
```

| Build | Kernel | pp128 | pp512 | tg128 | Notes |
|-------|--------|-------|-------|-------|-------|
| b8460 | 6.19.4 | **547** | **1047** | **54.67** | Current fair ROCm comparison |
| b8301 | 6.19.4 | 542 | 1059 | 47.87 | Old build, HSA fix |
| b8301 | 6.18.14 | 488 | 996 | 48.80 | Previous reference |

ROCm remains relevant for batch processing, hipBLASLt, vLLM experiments, and long-context/rocWMMA work. For current generation-heavy MoE chat/coding rows, Vulkan RADV is faster on the measured data; for prompt-processing-heavy work, HIP can win and should be tested separately.

### 2026-05-03 ROCm HIP Spot Check

| Model | Quant | ROCm pp512 | ROCm tg128 | Vulkan Reference |
|-------|-------|------------|------------|------------------|
| Qwen3.6 35B-A3B | UD-Q4_K_M | 1186.19 | 52.69 | Vulkan b9010: 1108.93 pp, 63.06 tg |
| Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1285.32 | 73.69 | Vulkan b9010: 1346.27 pp, 97.24 tg |

The local HIP build is b8460 and requires `LD_LIBRARY_PATH=/usr/local/lib/ollama/rocm` plus the HSA override. It emitted a missing `TensileLibrary_lazy_gfx1151.dat` warning, so treat this as a ROCm HIP baseline, not a tuned rocBLASLt/rocWMMA result.

### 2026-05-07 HIP vs Vulkan Crossover Spot Check

The new local spot check separates prompt processing from token generation. It is not a perfect same-build fairness claim: Vulkan rows use b9010, while HIP rows use the available local b8460 HIP build. The result is still useful because it matches the direction of the independent same-build Strix Halo study in [`nabe2030/hip-vs-vulkan-evo-x2`](https://github.com/nabe2030/hip-vs-vulkan-evo-x2).

Structured data: [`data/backend_crossover.csv`](data/backend_crossover.csv). Full notes: [`BACKEND_CROSSOVER.md`](BACKEND_CROSSOVER.md).

| Model | Vulkan pp16384 | HIP pp16384 | Prompt-processing read | Vulkan tg128 | HIP tg128 | Generation read |
|-------|---------------:|------------:|------------------------|-------------:|----------:|-----------------|
| Qwen3.6 35B-A3B UD-Q4_K_M | 1038.14 | **1295.38** | HIP +24.8% | **62.24** | 52.72 | Vulkan +18.1% |
| Qwen3-Coder 30B-A3B UD-Q4_K_XL | 564.68 | **756.16** | HIP +33.9% | **93.67** | 72.19 | Vulkan +29.8% |

Takeaway: keep Vulkan/RADV as the default for generation-heavy chat/coding and low-concurrency API use, but keep ROCm/HIP available for prompt-heavy experiments such as RAG ingestion, long prompts, summarization, and future vLLM/AWQ/DFlash work.

### 2026-05-16 Qwen3-Next 80B HIP vs Vulkan Spot Check

This spot check used the current b9172 Vulkan/RADV build against the existing Lemonade `llamacpp-rocm` b1259/gfx1151 bundle. It is a small r3/r20 comparison, not a final same-build backend shootout, but it is useful because it repeats the same workload split: HIP can help prefill, while Vulkan remains better for decode/generation.

Structured data: [`data/backend_crossover.csv`](data/backend_crossover.csv).

| Model | Vulkan pp512 | HIP pp512 | Prompt-processing read | Vulkan tg128 | HIP tg128 | Generation read |
|-------|-------------:|----------:|------------------------|-------------:|----------:|-----------------|
| Qwen3-Next 80B-A3B UD-Q4_K_XL | 751.70 | **800.38** | HIP +6.5% | **59.06** | 49.57 | Vulkan +19.1% |

Takeaway: do not phrase the guide as "RADV wins everything." For beginners, the practical rule is still simple: use Vulkan/RADV for chat, coding, and generation-heavy GGUF inference. Advanced users doing RAG ingest, long-prompt summarization, or server/batch experiments should test HIP/ROCm too.

Gemma 4 26B-A4B is a negative result on the local HIP path: Vulkan loaded and ran, but HIP b8460 failed to load the local GGUF. No local Gemma 4 HIP speed claim is made.

## Current Takeaways

1. Direct llama.cpp with Vulkan RADV is the fastest measured short-context path for Qwen MoE models.
2. Updating llama.cpp from b8298 to b8460 produced the largest improvement: +24% pp and +25% tg on Qwen3.5-35B-A3B.
3. AMDVLK caused false regression reports through ICD hijacking; keep it removed.
4. ROCm works on kernel 6.19.4 with HSA overrides. The latest measured generation rows are still behind Vulkan RADV, but HIP can win prompt processing.
5. Before any new benchmark campaign, keep `tuned accelerator-performance` active and log raw commands/results into a single dataset.
