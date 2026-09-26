# 64GB-tier 30B-class candidates on llama.cpp b11146 (2026-09-26, routine)

**Question:** do the newer 30B-class models listed in the
[64GB published-size tier](../../../../docs/models.md#64gb-published-size-tier)
load and run on the current official llama.cpp release v0.5.0 (build b11146)
with Vulkan/RADV, how fast is direct `llama-bench` decode and prefill, and do
they give a coherent, repeatable answer to two short deterministic prompts?

This bundle is **direct `llama-bench` evidence plus a short correctness smoke**,
measured under **routine** host conditions. It contains no server/API,
MTP/speculative, DFlash, vision, concurrency or Ollama results. It was measured
on a 128GB machine: it is **not a 64GB fit result** and records no peak-memory
figure. Two prompts are a smoke test, not a coding-quality evaluation.

## Stack

- Beelink GTR9 Pro, Ryzen AI MAX+ 395, Radeon 8060S (RADV STRIX_HALO), 128GB.
- Kernel `7.0.0-31-generic`; Mesa/RADV `26.2.3` (kisak PPA);
  linux-firmware `20240318.git3b128b60.0ubuntu3.1`.
- Runtime: official prebuilt release asset `llama-b11146-bin-ubuntu-vulkan-x64.tar.gz`
  (the same file as the
  [strict-clean b11146 bundle](../strict-clean-headline-b11146/README.md)),
  reports `version: 0.5.0-dev (build 11146, commit 7fe450e19)`
  (`build-version.txt`). Device line:
  `fp16: dot2 | int dot: 1 | matrix cores: KHR_coopmat`.
- `AMD_VULKAN_ICD=RADV`, all layers offloaded (`-ngl 999`), flash attention on
  (`-fa 1`), llama-bench defaults otherwise (`-b 2048 -ub 512`, load mode auto).

## Artifacts

Downloaded at pinned Hugging Face revisions; the local SHA-256 of every file
matches the Hugging Face LFS hash (`artifact-sha256.txt`). Licenses were read
from the model cards on 2026-09-26.

| Model | Repository @ revision | File | Size (bytes) | GGUF metadata | License |
| --- | --- | --- | ---: | --- | --- |
| Nemotron 3.5 Lightning 30B-A3B | [ggml-org/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF](https://huggingface.co/ggml-org/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF) @ `8a08a1c` | `NVIDIA-Nemotron-3.5-Lightning-30B-A3B-Q4_0.gguf` | 18,898,091,584 (18.90GB) | `nemotron_h_moe`, 31.58B params | OpenMDW-1.1 (upstream NVIDIA card; GGUF card says `other`) |
| Laguna XS 2.1 | [ggml-org/Laguna-XS-2.1-GGUF](https://huggingface.co/ggml-org/Laguna-XS-2.1-GGUF) @ `273068c` | `Laguna-XS-2.1-Q4_K_M.gguf` | 19,563,570,240 (19.56GB) | `laguna` MoE, 33.44B params | OpenMDW-1.1 |
| Muse Glimmer 30B | [meta-models/Muse-Glimmer-30B-GGUF](https://huggingface.co/meta-models/Muse-Glimmer-30B-GGUF) @ `70bf1b6` | `Muse-Glimmer-30B-KQuant-17GB-Q4_K_M.gguf` | 16,756,683,904 (16.76GB) | `muse-glimmer` dense, 27.85B params in the text file | Apache 2.0 |

The Nemotron MTP sidecar and the Muse Glimmer mmproj and DFlash files were not
downloaded: speculative decoding and vision are separate lanes.

## Host conditions (Background-Load Policy: routine)

Nothing was paused. The libvirt desktop VM stayed `running`; the desktop session,
Zoom, Chrome, the remote-access agent and CLI sessions stayed active; the power
profile stayed `balanced` with AMDGPU DPM `auto` (no boost). Ollama had no model
loaded before, during or after the run (`ollama ps` empty in every snapshot).
`gpu_busy_percent` was 0 before and after; the 7GB swap was already full before
the run and stayed full. See `host-snapshot-*.txt` (runtime names only).

Order: one model at a time (Nemotron, Laguna, Muse Glimmer), in one session
without reboot, 10 s between benchmarks, between 05:06 and 05:24 local time.

## Results

Direct `llama-bench`, t/s. Pass 1 is the CSV run (mean ± llama-bench stddev).
The b11146 CSV output has no per-repeat samples, so a second r10 pass was run
immediately afterwards with `-o json`; it gives the mean and the min-max range
of the 10 repeats. The long-context point is r3 (mean ± stddev).

| Model / quant | pp512 pass 1 (r10) | pp512 pass 2 mean (min-max) | tg128 pass 1 (r10) | tg128 pass 2 mean (min-max) | pp8192 (r3) | tg128 at depth 8192 (r3) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Nemotron 3.5 Lightning 30B-A3B Q4_0 | 1450.33 ± 3.31 | 1446.36 (1438.04-1458.09) | 66.80 ± 0.14 | 67.15 (67.00-67.25) | 1409.10 ± 2.77 | 65.99 ± 0.08 |
| Laguna XS 2.1 Q4_K_M | 1399.02 ± 9.82 | 1385.83 (1369.68-1400.02) | 80.45 ± 0.12 | 80.31 (78.80-80.61) | 1026.84 ± 0.52 | 70.05 ± 0.04 |
| Muse Glimmer 30B Q4_K_M | 370.89 ± 1.32 | 369.72 (368.82-371.30) | 13.24 ± 0.01 | 13.24 (13.23-13.25) | 346.52 ± 0.89 | 13.01 ± 0.02 |

No load error, unsupported-architecture failure or crash occurred: every
benchmark and smoke exited with code 0 (`run-order.log`).

## Correctness smoke

`llama-completion` with the model's own chat template (`--jinja -st`), greedy
(`--temp 0 --top-k 1 --seed 42`), `-c 4096 -n 1024`, each prompt run twice.
Default reasoning behavior of each template was left on. `check-smoke.py`
takes the final answer after the reasoning block and checks it; its output is
`smoke-check.txt`.

- **arith:** "What is 17 multiplied by 23? Answer with the number only."
  Pass = final answer exactly `391`.
- **code:** "Write a Python function is_prime(n) ... Reply with only the code."
  Pass = the returned `is_prime` matches a reference for n = -10..500.

| Model | arith (2 runs) | code (2 runs) | Run 1 = run 2 |
| --- | --- | --- | --- |
| Nemotron 3.5 Lightning | pass, `391` | pass | identical output, both prompts |
| Laguna XS 2.1 | pass, `391` | **no final answer at `-n 1024`** (still reasoning at the token cap); pass in a supplementary pair at `-c 8192 -n 4096` (1115 generated tokens) | identical output in every pair |
| Muse Glimmer 30B | pass, `391` | pass | identical output, both prompts |

Load warnings (not failures): Laguna and Muse Glimmer log
`special_eot_id is not in special_eog_ids - the tokenizer config may be incorrect`;
Muse Glimmer also re-marks `<|start|>` and `<|message|>` as user-defined tokens.
Generation still stopped at end of text in every run.

## Read

- All three candidates load and run on the official v0.5.0 Vulkan build with
  their default llama-bench settings.
- The two MoE models (about 3B active) decode at 67 (Nemotron) and 80 (Laguna)
  t/s at short context; Laguna keeps 70 t/s and Nemotron 66 t/s at depth 8192.
  Nemotron's hybrid Mamba-2 design loses little prefill speed at 8192 tokens
  (1409 vs 1450), while Laguna drops from about 1399 to 1027.
- Muse Glimmer is dense (27.85B in the text file) and decodes at about 13 t/s,
  the bandwidth-bound speed class of a dense 30B Q4 model, not the MoE class.
- For context only: the same b11146 build measured Qwen3-Coder 30B-A3B
  UD-Q4_K_XL at 1437.52 pp512 / 96.33 tg128 under strict-clean conditions
  earlier the same night
  ([bundle](../strict-clean-headline-b11146/README.md)). Conditions differ
  (strict-clean vs routine), so this is not a matched A/B.

## Caveats

- Routine conditions, not strict-clean; not a headline claim.
- Measured on 128GB. File size is not total memory use; KV cache, compute
  buffers and the OS need room, and how much a 64GB machine lets the GPU
  address depends on firmware and driver settings. No 64GB fit is claimed.
- Direct `llama-bench` only. Server throughput, MTP (Nemotron), DFlash and
  vision (Muse Glimmer) and tool use are not tested here.
- Two deterministic prompts do not measure coding quality, long-context
  quality or Dutch. Laguna needed more than 1024 tokens of reasoning for the
  code prompt.
- One artifact per model; other quants and revisions are not qualified.
- IBM Granite 4.2 30B and a matched Qwen3.8 27B control from the same queue
  row were not run in this pass.

## Commands

The exact harnesses are `run-routine.sh` (benchmarks, smokes, snapshots),
`run-samples.sh` (pass 2) and `run-laguna-code-n4096.sh` (supplementary Laguna
code smoke). Per model:

```bash
BIN=~/llama-cpp-b11146/llama-b11146
export AMD_VULKAN_ICD=RADV
$BIN/llama-bench -m MODEL.gguf -fa 1 -ngl 999 -p 512 -n 128 -r 10 -o csv
$BIN/llama-bench -m MODEL.gguf -fa 1 -ngl 999 -p 512 -n 128 -r 10 -o json
$BIN/llama-bench -m MODEL.gguf -fa 1 -ngl 999 -p 8192 -n 0 -r 3 -o csv
$BIN/llama-bench -m MODEL.gguf -fa 1 -ngl 999 -p 0 -n 128 -d 8192 -r 3 -o csv
$BIN/llama-completion -m MODEL.gguf -ngl 999 -fa 1 -c 4096 -n 1024 \
  --temp 0 --top-k 1 --seed 42 --jinja -st -p "PROMPT"
```

## Files

- `*.command.txt`, `*.csv` / `*.json`, `*.stderr.log`: per-run command,
  llama-bench output and stderr.
- `*-smoke-*.out.txt`: full smoke transcripts; `smoke-check.txt`: checker output.
- `host-snapshot-{before,mid-1,mid-2,after,after-pass2}.txt`: kernel, power,
  DPM, Mesa, memory, disk, `ollama ps`, VM state, GPU render-node holders
  (runtime names only) and a `top` sample.
- `run-order.log`, `build-version.txt`, `artifact-sha256.txt`.

Home paths are written as `~`; hostnames, LAN addresses and process command lines
are not recorded.
