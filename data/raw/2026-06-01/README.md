# 2026-06-01 Latest llama.cpp Direct Spot Check

This folder records the 2026-06-01 latest-stack direct Qwen3-Coder check.

Host state:

- T3 stayed running and was guarded.
- RustDesk, DocFlock/ffmpeg, Ollama, and the Zoom VM were stopped for the run.
- Hermes, SSH, desktop/session, audio, and T3 were not touched.
- `scripts/check_benchmark_cleanliness.sh` reported clean before and after the run.

Result:

- `de6f727aa` (`b9453-7`) Qwen3-Coder 30B-A3B Q4_K_S, `mmap=0`: 1384.30 pp512 / 95.55 tg128.
- The same route with default `mmap=1`: 1371.77 pp512 / 94.20 tg128.

Interpretation:

- This is useful latest-stack negative evidence.
- It does not replace the b9179 strict-clean 98.51 t/s direct headline.
