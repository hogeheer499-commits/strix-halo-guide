# Reddit GTR9 Pro Independent Reproduction And -ub Clamp Report

Source: https://www.reddit.com/r/StrixHalo/comments/1v6i88l/comment/p5ffxhi/

Contributor: `Ornery_Specialist_83`

System:

- Beelink GTR9 Pro (separate unit from the guide's first-party machine)
- AMD Ryzen AI MAX+ 395 / Radeon 8060S, 128GB
- Ubuntu 24.04 (stock Mesa 25.2.8 before upgrade); kernel, BIOS UMA, and
  llama.cpp build number were not reported in the captured comment

Benchmark shape:

```bash
llama-bench -fa 1 -ngl 999 -r 3
# Qwen3.6-35B-A3B UD-Q4_K_M, Vulkan/RADV
```

Reported results:

| Config | Mesa | pp512 | tg128 |
|---|---|---|---|
| `-b 256 -ub 1024` | 25.2.8 (stock) | 733.90 +/- 4.9 | 61.09 +/- 0.13 |
| `-b 2048 -ub 512` | 25.2.8 (stock) | 945.83 +/- 3.8 (+28.9%) | 60.79 +/- 0.44 |
| `-b 2048 -ub 512` | 26.1.7 (kisak) | 1105.75 (+16.9%) | 62.65 (+3.1%) |

Combined effect: 733.90 -> 1105.75 t/s pp512 (+50.7%) without hardware or
quant changes.

Key mechanism reported: in `llama-context.cpp` the effective ubatch is
`std::min(n_batch, n_ubatch)`, so `-ub` larger than `-b` is silently
discarded with no warning or error. Generation was unchanged by the batch
fix, consistent with decode being memory-bandwidth bound while prefill is
not. The contributor also reported that no reboot is needed for inference
after a Mesa upgrade: RADV is userspace, so restarting `llama-server` picks
up the new driver.

Status: community-reported Reddit numbers transcribed from the public
comment. The final 62.65 t/s tg128 independently lands on the guide's
first-party ~62-63 t/s Beelink Qwen3.6 figure, making this the first
independent reproduction of that figure on a second GTR9 Pro unit. Build,
kernel, UMA, and raw `llama-bench` output can upgrade this record via a
benchmark-report issue.
