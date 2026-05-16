# AMDVLK Isolated Break-100 Test - 2026-05-16

Goal: test whether AMDVLK can beat the current Vulkan/RADV Qwen3-Coder Q4_K_S ceiling without installing AMDVLK on the host.

Environment:

- Container image: `docker.io/kyuz0/amd-strix-halo-toolboxes:vulkan-amdvlk`
- Device: `/dev/dri` passed through to rootless Podman
- ICD: `/etc/vulkan/icd.d/amd_icd64.json`
- Model: Qwen3-Coder 30B-A3B Q4_K_S
- T3 stayed running on the host.

## Result

| Run | Repeats | pp512 | tg128 | Read |
|-----|--------:|------:|------:|------|
| [`amdvlk-q4ks-t15-r5.csv`](amdvlk-q4ks-t15-r5.csv) | r5 | 944.51 | 93.28 | AMDVLK is clearly slower than the RADV 98.51 t/s r50 row for this direct generation workload. |

Conclusion: AMDVLK is not a break-100 route here. It remains useful as an isolated comparison, but not as a public recommendation for this Qwen3-Coder Q4_K_S path.
