# Kyuz0 Toolbox Cross-OEM Validation

Date: 2026-07-29

Status: published first-party compatibility evidence. This is not a
strict-clean headline benchmark.

## Purpose

Independently validate the current Kyuz0 Vulkan/RADV and ROCm 7.2.4
container images on a Beelink GTR9 Pro running Ubuntu 24.04.

This validates the images, bundled `llama.cpp` binaries, GPU detection,
direct `llama-bench`, an OpenAI-compatible `llama-server` smoke test, and
the current Ubuntu/Distrobox create-refresh-enter path. It does not validate
the complete Llama Cockpit UI.

## Host And Model

- Host: Beelink GTR9 Pro
- CPU/iGPU: AMD Ryzen AI MAX+ 395 / Radeon 8060S
- OS: Ubuntu 24.04.4
- Kernel: 7.0.0-28-generic
- RAM: 128GB class
- Container engine: rootless Podman 4.9.3
- Distrobox: 1.7.0
- Toolbox source:
  [`kyuz0/amd-strix-halo-toolboxes`](https://github.com/kyuz0/amd-strix-halo-toolboxes)
- Toolbox source commit:
  [`5aa1e8155d9a1ce339b94fea9b00e3abecad8939`](https://github.com/kyuz0/amd-strix-halo-toolboxes/commit/5aa1e8155d9a1ce339b94fea9b00e3abecad8939)
- Model: `Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf`
- Model bytes: `17665334432`
- Model SHA-256: `2841aa314d916434860cfb8990347528dcdfe5c350dbcb9d1461dbee88ff2533`
- `llama.cpp`: build `10182`, commit `afeebe103`

The host retained its documented real-world background workload, including
the Zoom VM, Zoom, FFmpeg/DocRemote, RustDesk, and the desktop. These are
compatibility and same-host A/B results, not strict-clean headline results.
Local usernames and model paths in the published command output were
sanitized to `/home/USER`; benchmark values and runtime output were otherwise
left unchanged.

## Exact Images

### Vulkan/RADV

- Tag: `docker.io/kyuz0/amd-strix-halo-toolboxes:vulkan-radv`
- Manifest digest: `sha256:dd3f8423e847d98752d799ba04fc30139a152f27e1e13e8684ad52ab7e4d39f2`
- Image ID: `67407c6f3a8a91a04a1af1e483669a4531e5a70dd41638465e622843cc571867`
- Created: `2026-07-29T17:27:26Z`
- Detected device: `Vulkan0: AMD Radeon 8060S Graphics (RADV GFX1151)`
- Container graphics stack: Mesa/RADV 25.3.6

### ROCm

- Tag: `docker.io/kyuz0/amd-strix-halo-toolboxes:rocm-7.2.4`
- Manifest digest: `sha256:4b2878d02083cdb71c04dcc0ca3017a8de36bdb87221efaece0d0d45f6a8ce1c`
- Image ID: `aab50b8862c2156e38fa0e183f5637c92e1442d372a1871e9009653ba5da340f`
- Created: `2026-07-29T17:36:25Z`
- Detected device: `ROCm0: AMD Radeon 8060S Graphics`

## Direct Benchmark

Identical settings were used apart from the selected backend device:

```bash
llama-bench \
  -m /models/Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf \
  -p 512 -n 128 -r 5 \
  -b 2048 -ub 512 \
  -ngl 999 -fa on \
  -dev BACKEND_DEVICE \
  -o jsonl
```

| Backend | pp512 mean | pp512 samples | tg128 mean | tg128 samples |
|---|---:|---|---:|---|
| Vulkan/RADV | 1370.47 t/s | 1393.48, 1374.92, 1359.47, 1365.75, 1358.74 | 92.16 t/s | 92.45, 92.09, 92.55, 92.20, 91.50 |
| ROCm 7.2.4 | 1384.81 t/s | 1387.14, 1386.41, 1398.18, 1378.86, 1373.44 | 71.39 t/s | 71.21, 71.38, 71.47, 71.51, 71.38 |

For this 30B-A3B GGUF and these settings:

- ROCm prompt processing was 1.05% above Vulkan.
- Vulkan generation was 29.09% above ROCm.
- Both backends completed all five repetitions without an error.

This is a backend result for one model shape, not a universal ranking.

## Minimal Rootless Podman Route

Both current images completed a three-repeat 30B benchmark using rootless
Podman without `--privileged`, extra capabilities, `--ipc=host`, a custom
seccomp policy, or host-root mounts.

Vulkan/RADV:

```bash
podman run --rm \
  --device /dev/dri \
  -v /home/USER/models:/models:ro \
  docker.io/kyuz0/amd-strix-halo-toolboxes:vulkan-radv \
  llama-bench \
    -m /models/Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf \
    -p 512 -n 128 -r 3 -b 2048 -ub 512 \
    -ngl 999 -fa on -dev Vulkan0 -o jsonl
```

ROCm 7.2.4:

```bash
podman run --rm \
  --device /dev/dri \
  --device /dev/kfd \
  -v /home/USER/models:/models:ro \
  docker.io/kyuz0/amd-strix-halo-toolboxes:rocm-7.2.4 \
  llama-bench \
    -m /models/Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf \
    -p 512 -n 128 -r 3 -b 2048 -ub 512 \
    -ngl 999 -fa on -dev ROCm0 -o jsonl
```

| Rootless Podman path | pp512 mean | tg128 mean | Result |
|---|---:|---:|---|
| Vulkan/RADV, minimal flags | 1385.98 t/s | 94.71 t/s | pass |
| ROCm 7.2.4, minimal flags | 1396.37 t/s | 73.58 t/s | pass |

This is a host-specific minimum, not a promise that every distribution has
the required device permissions by default. Users still need working
`/dev/dri` and, for ROCm, `/dev/kfd` access.

## Ubuntu/Distrobox Refresh Validation

The current `refresh-toolboxes.sh` correctly detected Ubuntu and selected
Distrobox. The following sequence passed for both `llama-vulkan-radv` and
`llama-rocm-7.2.4`:

1. Create from the current image.
2. Enter the container and detect the Radeon 8060S.
3. Run the refresh script again, removing and recreating the container.
4. Re-enter the refreshed container and detect the Radeon 8060S again.

Vulkan also completed the full benchmark after refresh:

- pp512: 1391.01 t/s
- tg128: 93.64 t/s

The ROCm path exposed a separate migration hazard. This host still exported
the legacy workaround:

```bash
HSA_OVERRIDE_GFX_VERSION=11.0.0
```

Distrobox inherited it from the shared host shell configuration. The current
ROCm image then detected the Strix Halo iGPU as `gfx1100` instead of
`gfx1151` and `llama-bench` crashed in `libamdhip64.so.7.2.70204` with exit
139. Direct rootless Podman did not inherit the override and passed.

The scoped Distrobox correction was:

```bash
env -u HSA_OVERRIDE_GFX_VERSION \
  llama-bench \
    -m /home/USER/models/Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf \
    -p 512 -n 128 -r 3 -b 2048 -ub 512 \
    -ngl 999 -fa on -dev ROCm0 -o jsonl
```

After unsetting the stale override, the refreshed ROCm toolbox detected
`gfx1151` and completed all repetitions:

- pp512: 1396.78 t/s
- tg128: 72.94 t/s

The practical fix is to remove the old override from the host shell startup
files when using a current ROCm build with native `gfx1151` support. Merely
adding another export inside the container can hide the migration problem.

## Server Smoke Test

Both images passed:

- model load
- `GET /health` returning `{"status":"ok"}`
- `GET /v1/models`
- `POST /v1/completions`
- deterministic control text containing `STRIX_HALO_TOOLBOX_OK`

Server command:

```bash
llama-server \
  -m /models/Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf \
  -ngl 999 -fa on \
  -dev BACKEND_DEVICE \
  --host 0.0.0.0 --port 8080 \
  -c 4096
```

The short completion timings are retained as smoke-test diagnostics rather
than benchmark claims because the prompt contained only 12 evaluated tokens.

## Key Evidence Files

- `host_snapshot.txt`
- `model_sha256.txt`
- `model_metadata.txt`
- `image_metadata.txt`
- `vulkan_runtime.txt`
- `rocm_runtime.txt`
- `vulkan_results.jsonl`
- `rocm_results.jsonl`
- `vulkan_stderr.log`
- `rocm_stderr.log`
- `vulkan_health.json`
- `rocm_health.json`
- `vulkan_models.json`
- `rocm_models.json`
- `vulkan_completion.json`
- `rocm_completion.json`
- `vulkan_server.log`
- `rocm_server.log`
- `distrobox_vulkan_create.log`
- `distrobox_vulkan_refresh.log`
- `distrobox_vulkan_after_refresh_bench.jsonl`
- `distrobox_rocm_create.log`
- `distrobox_rocm_refresh.log`
- `distrobox_rocm_isolated_retry.stderr`
- `rocm_stale_override_kernel.log`
- `distrobox_rocm_unset_override_bench.jsonl`
- `podman_minimal_vulkan_bench.jsonl`
- `podman_minimal_rocm_bench.jsonl`
- `podman-minimal-matrix/`

## Current Conclusion

Both current Kyuz0 images are directly runnable on this second OEM/OS path:
Beelink GTR9 Pro plus Ubuntu 24.04. The current refresh script also survives
complete Distrobox recreate-and-reenter cycles on Ubuntu.

The most actionable findings are not the throughput numbers:

1. A minimal rootless Podman route works without `--privileged`, answering
   the main operational question in
   [upstream issue #80](https://github.com/kyuz0/amd-strix-halo-toolboxes/issues/80).
2. A stale `HSA_OVERRIDE_GFX_VERSION=11.0.0` inherited through Distrobox can
   misidentify Strix Halo as `gfx1100` and crash current ROCm 7.2.4. Removing
   the obsolete workaround restores correct `gfx1151` detection and inference.
3. The current Ubuntu-aware refresh script appears to resolve the original
   refresh failure reported in
   [upstream issue #62](https://github.com/kyuz0/amd-strix-halo-toolboxes/issues/62)
   for both tested backends.

These are independent compatibility and migration results with exact
artifacts. They are not a claim that one backend is always faster.
