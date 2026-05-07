# Smoke Tests

This file records short validation runs before larger benchmark campaigns. Smoke tests are not headline benchmark data. They are used to decide whether the system is clean enough to collect publishable results.

## 2026-05-07 llama.cpp b9010 vs b9049 Spot Check

### Verdict

**Updating from llama.cpp b9010 to upstream b9049 does not materially change the short-context Vulkan RADV results for the two headline Qwen MoE models.**

This is useful negative data. b9049 is current upstream as of 2026-05-07, but it is not a new Strix Halo speed breakthrough for this direct `llama-bench` path.

### Cleanup Before Testing

Before testing:

- The high-CPU DocFlock `ffmpeg` virtual-camera process was paused with `SIGSTOP`.
- Zoom processes were paused with `SIGSTOP`.
- RustDesk user processes were paused with `SIGSTOP`; the system service remained present.
- T3 and Hermes were left running.
- `tuned accelerator-performance`, RADV, Mesa 26.0.6, and 2900 MHz GPU clock were verified.

### Results

All direct runs used:

```bash
AMD_VULKAN_ICD=RADV
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.json
-fa 1 -ngl 999 -mmp 0 -p 512 -n 128 -r 20 -o csv
```

| Build | Model | Quant | pp512 | tg128 | Delta vs b9010 |
|-------|-------|-------|-------|-------|----------------|
| b9010 / d05fe1d7d | Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1376.68 | 94.12 | baseline |
| b9049 / 2496f9c14 | Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1381.55 | 95.04 | tg +1.0%, pp +0.4% |
| b9010 / d05fe1d7d | Qwen3.6 35B-A3B | UD-Q4_K_M | 1093.07 | 61.82 | baseline |
| b9049 / 2496f9c14 | Qwen3.6 35B-A3B | UD-Q4_K_M | 1094.19 | 61.65 | tg -0.3%, pp +0.1% |

### Takeaway

Do not update the guide's headline performance claim based on b9049. The short-context direct Vulkan/RADV conclusion is stable. Move next to the HIP vs Vulkan long-prompt crossover and vLLM AWQ/DFlash reproduction, where new conclusions are more likely.

## 2026-05-03 Before/After llama.cpp Update

### Verdict

**The machine is clean enough for direct llama-bench smoke testing, and updating llama.cpp from b8933 to b9010 did not materially change short-context Qwen MoE token generation.**

This is useful negative data: unlike the b8298 to b8460 jump, the b8933 to b9010 update is not a new speed breakthrough for these two short-context Vulkan RADV smoke tests.

### Cleanup Before Testing

The machine had become polluted again since the previous day:

- A background media service had restarted and spawned a high-CPU `ffmpeg` virtual-camera workload.
- A video-conferencing process was active.
- Remote-desktop user processes had respawned.
- No benchmark-relevant VM was running by the time the baseline was taken.

Before testing:

- The background media service was stopped.
- `ffmpeg` and video-conferencing processes were stopped.
- Remote-desktop user processes were paused with `SIGSTOP`.
- `tuned accelerator-performance`, RADV, Mesa 26.0.6, AMDVLK absence, and 2900 MHz GPU clock were verified.

### Update Applied

Only llama.cpp was changed.

| Component | Before | After |
|-----------|--------|-------|
| llama.cpp | b8933 / `dcad77cc3` | b9010 / `d05fe1d7d` |
| Commits advanced | - | 77 commits |
| Vulkan build | `~/llama-cpp-latest/build-vulkan` | rebuilt successfully |
| Preserved old build | - | `~/llama-cpp-latest/build-vulkan-b8933-20260503` |

Ollama was not upgraded during this run.

### Results

All direct runs used:

```bash
AMD_VULKAN_ICD=RADV
-fa 1 -ngl 999 -mmp 0 -p 512 -n 128 -r 5 -o csv
```

| Phase | Build | Model | Quant | pp512 | tg128 | Delta vs before |
|-------|-------|-------|-------|-------|-------|-----------------|
| before update | b8933 / dcad77cc3 | Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1354.67 | 95.81 | baseline |
| after update | b9010 / d05fe1d7d | Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1334.31 | 95.73 | tg -0.1%, pp -1.5% |
| before update | b8933 / dcad77cc3 | Qwen3.6 35B-A3B | UD-Q4_K_M | 1098.80 | 62.16 | baseline |
| after update | b9010 / d05fe1d7d | Qwen3.6 35B-A3B | UD-Q4_K_M | 1102.46 | 62.07 | tg -0.1%, pp +0.3% |

### Takeaway

Current short-context Vulkan RADV performance is stable across b8933 and b9010 for these two smoke models. The guide should not claim a new update-driven speedup from this llama.cpp update.

## 2026-05-03 Ollama v0.21.2 vs v0.22.1 Smoke

### Verdict

**Ollama v0.22.1 does not change short-context Qwen3.6 35B generation speed in this smoke test.**

The system install was left on Ollama 0.21.2. Ollama 0.22.1 was tested as a temporary verified release tarball on `127.0.0.1:11435`, using the same model store and RADV/Vulkan environment as the system service.

### Release Checked

| Component | Baseline | Checked Update |
|-----------|----------|----------------|
| Ollama | 0.21.2 system service | 0.22.1 temporary binary |
| Release asset | - | `ollama-linux-amd64.tar.zst` |
| Asset SHA256 | - | `e27c0fe8f60a824162f81ce07b4bfda767dce4f357d762e149b3d0de0abad9fb` |
| Server port | `127.0.0.1:11434` | `127.0.0.1:11435` |
| Backend | Vulkan RADV | Vulkan RADV |
| Global install changed | no | no |

### Results

Both runs used `POST /api/generate` with `num_predict=128`, `temperature=0`, `top_k=1`, and the same prompt:

```text
Write one short sentence about local AI benchmarks.
```

| Tool | Run | Prompt tokens | Prompt eval | Generation | Load duration | Interpretation |
|------|-----|---------------|-------------|------------|---------------|----------------|
| Ollama 0.21.2 | cold | 19 | 154.42 t/s | 50.87 t/s | 7.08 s | baseline system service |
| Ollama 0.21.2 | warm | 19 | 156.05 t/s | 50.49 t/s | 0.11 s | stable baseline |
| Ollama 0.22.1 | cold | 19 | 35.71 t/s | 50.19 t/s | 6.60 s | temporary binary; prompt eval affected by cold startup |
| Ollama 0.22.1 | warm | 19 | 159.58 t/s | 50.49 t/s | 0.11 s | matches 0.21.2 |

### Takeaway

Do not update the guide's Ollama performance claim based on v0.22.1. The update may still matter for model support and app behavior, but it does not produce a measurable Qwen3.6 35B short-context generation gain in this smoke test.

## 2026-05-02 Smoke Test

### Clean Rerun Verdict

**The clean rerun is valid as smoke-test evidence. Do not promote it to headline benchmark data until the same commands are run as part of a controlled benchmark campaign.**

After stopping background media, video-conferencing, VM, and remote-desktop load, the same direct llama-bench checks recovered from the polluted 76-52 t/s range to the expected 95-62 t/s range.

This confirms that the earlier low results were caused by background load, not a RADV, Mesa, or llama.cpp regression.

### Clean Rerun Results

| Build | Model | Quant | pp512 | tg128 | Interpretation |
|-------|-------|-------|-------|-------|----------------|
| b8460 / b1c70e2e5 | Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1303.32 | 95.39 | Early signal later superseded by the controlled 97.24 t/s rerun |
| b8933 / dcad77cc3 | Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1317.84 | 95.46 | Matches b8460 on tg and slightly improves pp |
| b8933 / dcad77cc3 | Qwen3.6 35B-A3B | UD-Q4_K_M | 1068.15 | 62.11 | Restores expected UD performance after polluted run |
| b8460 / b1c70e2e5 | Qwen3.6 35B-A3B | UD-Q4_K_M | 1098.13 | 62.02 | b8460 and b8933 align on tg |

Ollama clean smoke:

| Tool | Model | Prompt Tokens | Prompt Eval | Generation | Interpretation |
|------|-------|---------------|-------------|------------|----------------|
| Ollama 0.21.2 | Qwen3.6 35B-A3B | 24 | 174.82 t/s | 49.08 t/s | Functional easy-path smoke; not a controlled benchmark because the model still emitted thinking text |

### What Was Stopped

- Background media service: stopped via user systemd. This removed the high-CPU `ffmpeg` virtual-camera workload and related desktop capture load.
- Benchmark-irrelevant VM: shut down cleanly via libvirt. This removed the 16GB / 8-vCPU VM load.
- Remote-desktop user processes: paused with `SIGSTOP` because the root system service respawned them and system-level stop needs sudo. Resume with `kill -CONT <pid>` or restart the remote-desktop service.
- GNOME System Monitor: closed to remove extra desktop load.

### Polluted First Run Verdict

The first run below is retained as a useful warning.

### Verdict

**Do not publish these numbers as benchmark results.**

The stack is functional, but the environment was not clean enough for publishable performance data. The smoke test found heavy background load during the run:

- `ffmpeg` using roughly 1000% CPU
- video-conferencing process running
- remote-desktop process running
- a QEMU/KVM VM using CPU and 16GB RAM

No background processes were stopped. The numbers below are useful as a warning and as a functional check only.

### Update Check

No upgrades were applied.

| Component | Current | Available / Check Result | Action |
|-----------|---------|--------------------------|--------|
| llama.cpp | local `b8933` / `dcad77cc3` | `origin/master` at `b8999`, local tree 66 commits behind | Benchmark current baseline first, then do a separate before/after update test |
| Ollama | 0.21.2 | GitHub latest release: 0.22.1 | Do not upgrade until current baseline is clean |
| Mesa RADV | 26.0.6 kisak | apt candidate also 26.0.6 | No action |
| linux-firmware | 20240318.git3b128b60-0ubuntu2.27 | apt candidate also same version | No action |
| AMDVLK | not installed | correct | No action |

### Preflight

| Check | Result |
|-------|--------|
| Kernel | 6.19.4-061904-generic |
| `tuned-adm active` | `accelerator-performance` |
| Vulkan device | Radeon 8060S Graphics (RADV STRIX_HALO) |
| Vulkan driver | Mesa 26.0.6 - kisak-mesa PPA |
| GPU clock | 2900 MHz selected |
| AMDVLK | absent |

### Direct llama-bench Results

All direct runs used:

```bash
AMD_VULKAN_ICD=RADV
-fa 1 -ngl 999 -mmp 0 -p 512 -n 128 -r 3 -o csv
```

| Build | Model | Quant | pp512 | tg128 | Interpretation |
|-------|-------|-------|-------|-------|----------------|
| b8933 / dcad77cc3 | Qwen3.6 35B-A3B | UD-Q4_K_M | 1062.02 | 51.68 | Functional, but not publishable under load |
| b8460 / b1c70e2e5 | Qwen3.6 35B-A3B | UD-Q4_K_M | 1061.37 | 51.58 | Matches b8933; not a b8933-only regression |
| b8933 / dcad77cc3 | Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1327.72 | 76.75 | Below the old headline; environment not clean |
| b8460 / b1c70e2e5 | Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1324.51 | 76.70 | Matches b8933; not a b8933-only regression |

### Ollama Result

| Tool | Model | Prompt Tokens | Prompt Eval | Generation | Interpretation |
|------|-------|---------------|-------------|------------|----------------|
| Ollama 0.21.2 | Qwen3.6 35B-A3B | 25 | 31.08 t/s | 40.54 t/s | Functional only; contaminated by background load and long thinking output |

### Follow-up

Before publishing new benchmark rows:

1. Close or pause high-load desktop/VM/video workloads.
2. Confirm `ollama ps` shows no loaded models unless testing Ollama.
3. Re-run Qwen3-Coder 30B direct and Qwen3.6 Ollama smoke tests.
4. Only if smoke tests match expected ranges, run new benchmark campaigns.
