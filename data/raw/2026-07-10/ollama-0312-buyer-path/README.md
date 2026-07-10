# Ollama 0.31.2 System-Service Buyer Path

This run upgrades the normal system-wide Ollama service from 0.23.1 to the
official Ollama 0.31.2 Linux and ROCm packages. The service remains enabled and
uses Vulkan/RADV with `OLLAMA_IGPU_ENABLE=1` so the Radeon 8060S is retained as
an integrated GPU.

## Result

| Check | Result |
| --- | --- |
| Qwen3.6 35B-A3B, existing service `OLLAMA_NUM_PARALLEL=2` | 60.57 t/s warm mean; 60.00-61.22 t/s; 9 warm runs after one cold run |
| Controlled `OLLAMA_NUM_PARALLEL=1` repeat | 60.71 t/s warm mean; 60.20-61.21 t/s; no material recovery |
| iGPU verification | `Radeon 8060S Graphics (RADV STRIX_HALO)` detected as an iGPU; Qwen3.6 reported `100% GPU` and 42/42 layers offloaded |
| Vision smoke | `qwen2.5vl:7b` correctly read the repository preview; model and vision projector used Vulkan; Ollama reported `100% GPU` |
| Service restart | Version, iGPU environment, model cache, Qwen generation, and GPU offload survived `systemctl restart ollama` |
| Full host reboot | Ollama 0.31.2 autostarted, the persistent iGPU environment returned, Qwen3.6 produced a visible response with 42/42 layers offloaded, and Qwen2.5-VL 7B vision passed with 29/29 layers plus its vision encoder on Vulkan |

This is a current buyer-path pass but a performance regression versus the
separate user-local Ollama 0.31.1 check at 71.82 t/s. Changing parallel slots
from two to one did not explain the difference. Service-restart and subsequent
full-host-reboot persistence both passed.

## Evidence

- [`ollama-qwen36-35b-a3b-0312-parallel2-api-r10.csv`](ollama-qwen36-35b-a3b-0312-parallel2-api-r10.csv)
- [`ollama-qwen36-35b-a3b-0312-parallel1-api-r10.csv`](ollama-qwen36-35b-a3b-0312-parallel1-api-r10.csv)
- [`vision-qwen25vl7b-response.json`](vision-qwen25vl7b-response.json)
- [`systemd-state-after-restart.txt`](systemd-state-after-restart.txt)
- [`qwen36-after-service-restart.json`](qwen36-after-service-restart.json)
- [`post-reboot-state.txt`](post-reboot-state.txt)
- [`post-reboot-qwen36-visible-response.json`](post-reboot-qwen36-visible-response.json)
- [`post-reboot-vision-smoke.json`](post-reboot-vision-smoke.json)
- [`post-reboot-ollama-full.log`](post-reboot-ollama-full.log)
- [`host-snapshot.txt`](host-snapshot.txt)
- service logs and `ollama ps` snapshots in this directory
