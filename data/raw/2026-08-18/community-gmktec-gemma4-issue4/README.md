# GMKtec EVO-X2 Gemma 4 Direct Benchmark

Community-reported direct `llama-bench` evidence from
[`mottledMantis`' issue #4 comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/4#issuecomment-5324808949),
posted 2026-08-18.

## Submitted System And Route

- GMKtec EVO-X2, Ryzen AI MAX+ 395 / Radeon 8060S, 96GB LPDDR5X-8000
- Ubuntu 26.04, Mesa 26.0.3-1ubuntu1, Vulkan/RADV `STRIX_HALO`
- BIOS UMA 1GB, IOMMU off
- stock `llama.cpp` b9235 (`d14ce3dab`), `llama-bench`
- `unsloth/gemma-4-26B-A4B-it-GGUF`
- `gemma-4-26B-A4B-it-UD-Q4_K_M.gguf`
- `-b 2048 -ub 512`, 16 threads, f16 KV, flash attention on, mmap on,
  all layers offloaded

## Submitted Results

| Test | Throughput | Submitted standard deviation |
|---|---:|---:|
| pp512 | 1209.075618 t/s | 11.138445 |
| tg128 | 53.018213 t/s | 0.074021 |

The CSV preserved here is normalized from the public issue comment. The pasted
tg128 line was one field short: its displayed label/result and `test_time`
position make the intended shape `n_prompt=0,n_gen=128,n_depth=0`, so the
missing `n_prompt=0` cell is restored here. The original pasted text remains
available at the linked issue comment. The CSV reports a 16,931,716,216-byte
model file and 25,233,142,046 parameters. No model hash, full host snapshot,
power state, or repeat count beyond the `llama-bench` aggregate was supplied.

## Comparison Boundary

This is useful cross-OEM portability evidence for an ordinary, non-QAT,
non-speculative Gemma 4 route. Decode was 4.39% below the first-party Beelink
b9851 row and 2.14% below b9859, which places it in the same practical band.
Prefill was 8.85% and 8.64% lower, respectively.

It is not an OEM ranking or a clean same-build A/B. The Beelink controls used
newer `llama.cpp` builds, Mesa 26.1.3, `mmap=0`, a different host state, and a
model file that was 79,298,560 bytes (75.62 MiB) smaller despite the same
artifact name. Without matching model SHA256, build, flags, repeat policy, and
host snapshot, the gap cannot be attributed to BIOS, software, or hardware.
Keep this direct stock row separate from Nimo/community QAT+MTP served rows and
from first-party Beelink QAT/MTP results.

## Highest-Value Follow-Up

Repeat the same file (recording SHA256) on a current official `llama.cpp`
Vulkan build, then use the same build, mmap policy, command, repeats, and host
snapshot on the GMKtec and Beelink. That would turn useful portability evidence
into a controlled cross-OEM regression check.
