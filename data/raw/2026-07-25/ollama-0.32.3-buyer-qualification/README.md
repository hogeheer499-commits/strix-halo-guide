# Ollama 0.32.3 Strix Halo buyer qualification

Isolated qualification of the official Ollama 0.32.3 Linux AMD64 bundle before
changing the host's existing 0.31.2 system service.

## Method

- Hardware: Beelink GTR9 Pro, Ryzen AI MAX+ 395, Radeon 8060S, 128GB unified memory.
- Backend: Ollama Vulkan/RADV with `OLLAMA_IGPU_ENABLE=1`.
- Existing model cache was mounted read-only in practice: no pull or model change was needed.
- Both versions ran on the same isolated port with the same environment.
- Text model: `qwen3.6:35b-a3b`, ID `07d35212591f`, Q4_K_M.
- Text workload: three deterministic prompts, three measured repeats after warm-up,
  256-token limit, context 32768.
- Vision model: `qwen2.5vl:7b`, ID `5ced39dfa4ba`, Q4_K_M.
- Vision input: this repository's 1280x640 `social-preview.png`.

The official `ollama-linux-amd64.tar.zst` SHA-256 was verified as
`2597d74fbe654ef6a37db56f771cf37d4a85c6bde4018127874e3927d3113800`.

## Text result

| Version | Mean decode | Range | Initial model load |
| --- | ---: | ---: | ---: |
| 0.31.2 | 73.20 t/s | 72.84-73.50 t/s | 20.92 s |
| 0.32.3 | 73.13 t/s | 72.95-73.36 t/s | 21.92 s |

The mean difference was -0.09%, which is measurement noise rather than evidence
of a version regression. All nine measured response hashes matched between the
two versions.

## Vision and restart result

Ollama 0.32.3:

- detected `Radeon 8060S Graphics (RADV STRIX_HALO)` as an iGPU;
- offloaded all 29 Qwen2.5-VL layers to Vulkan;
- reported the loaded vision model as `100% GPU`;
- correctly read the guide title, benchmark values, and AMD Strix Halo platform
  from the supplied image;
- returned the exact same response after the isolated server was stopped and
  started again.

The matching vision-response SHA-256 was
`b67be0c8c3397d9e1c95eeb484152aed9e8df353fadff053e535b43205473349`.

## Guidance

Ollama 0.32.3 is a clean upgrade candidate for this tested Vulkan/RADV buyer
path. It preserved Qwen3.6 text speed and output, local vision offload worked,
and a server restart did not break the model path.

The host system service was deliberately left on 0.31.2 during this isolated
test. A full host-package replacement and reboot were not required to establish
runtime compatibility and remain a separate maintenance action.
