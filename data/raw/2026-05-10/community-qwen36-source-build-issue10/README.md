# Community Qwen3.6 Source/Build Follow-Up Issue #10

Source: https://github.com/hogeheer499-commits/strix-halo-guide/issues/10#issuecomment-4415454932

Contributor: Fail-Safe.

This directory stores a structured summary of Fail-Safe's Qwen3.6 source/build/quant follow-up. The source comment reports aggregate tables rather than separate attached raw CSV files, so the canonical provenance remains the linked issue comment.

## Setup

- System: Corsair AI Workstation 300 ai-2.
- OS/kernel: Fedora 43, kernel 7.0-rc6.
- Mesa: RADV 25.3.6.
- Backend: kyuz0 Vulkan/RADV container.
- Tool: llama.cpp b9093, commit `1e5ad35d5`.
- Methodology: N=6 sessions x r20 per t/s value.

## Main Findings

Fail-Safe separated the earlier Qwen3.6 Q4_0 difference into rough components:

| Comparison | What changed | pp512 delta | tg128 delta |
|------------|--------------|-------------|-------------|
| bartowski to 0xSero, both b9093 + kyuz0 defaults | GGUF source | +1.1% | +5.3% |
| kyuz0 defaults to guide flags, both 0xSero + b9093 | flags | +0.03% | +0.06% |
| b9049 to b9093, both 0xSero + guide flags | build | +3.0% | -1.85% |

Practical read: GGUF source can move token generation by about 5%, build changes can move pp and tg in different directions, and guide flags may already match tool defaults on newer builds.

Quality note: these are throughput-only rows. No model-quality eval was done.
