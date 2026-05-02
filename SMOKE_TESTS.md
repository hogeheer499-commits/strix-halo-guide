# Smoke Tests

This file records short validation runs before larger benchmark campaigns. Smoke tests are not headline benchmark data. They are used to decide whether the system is clean enough to collect publishable results.

## 2026-05-02 Smoke Test

### Verdict

**Do not publish these numbers as benchmark results.**

The stack is functional, but the environment was not clean enough for publishable performance data. The smoke test found heavy background load during the run:

- `ffmpeg` using roughly 1000% CPU
- Zoom running
- RustDesk running
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
| b8933 / dcad77cc3 | Qwen3-Coder 30B-A3B | UD-Q4_K_XL | 1327.72 | 76.75 | Below published 87 t/s; environment not clean |
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
