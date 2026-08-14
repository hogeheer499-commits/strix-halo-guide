# Qwen3.8 Artifact Scout

Date: 2026-08-14

Status: artifact and provenance scan only. No model was downloaded or benchmarked.

## Official Release

The official Qwen release found during this scan is:

- [`Qwen/Qwen3.8-2.4T-A95B`](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B)
- [`Qwen/Qwen3.8-2.4T-A95B-FP8`](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B-FP8)

The official model card describes:

- 2.4T total parameters;
- 95B activated parameters;
- 262,144 native context, extensible to 1,010,000 tokens;
- text-only input and output;
- vLLM, SGLang, and TokenSpeed deployment paths.

Hugging Face API metadata reported these repository payload totals during the scan:

| Artifact | Bytes | Decimal size | Binary size |
| --- | ---: | ---: | ---: |
| Full repository | 4,892,388,741,252 | 4.89 TB | 4.45 TiB |
| FP8 repository | 2,496,154,395,007 | 2.50 TB | 2.27 TiB |

The 95B active-parameter count describes per-token compute sparsity. It does not reduce the total weight set to 95B for storage or model residency. Even the official FP8 repository is far outside a one-box 128GB target.

## Community Pages From The Alert

### `Pluto-AI-Labs/Qwen3.8-27B-MLX`

Source: <https://huggingface.co/Pluto-AI-Labs/Qwen3.8-27B-MLX>

Observed state:

- created on 2026-08-14;
- only `.gitattributes` and `README.md` were present;
- the README said `Coming Soon` and described an upcoming model;
- no model weights were present;
- the declared runtime was Apple MLX, not an AMD Strix Halo route.

This page is not evidence that an official Qwen3.8 27B model or a runnable local artifact has been released.

### `Youssoufal/Qwen3.8-27B-MTPLX-Bare-Speed`

Source: <https://huggingface.co/Youssoufal/Qwen3.8-27B-MTPLX-Bare-Speed>

The repository API returned HTTP 401 during the scan, so its files, provenance, model identity, format, and memory requirements could not be verified. It must not be used as benchmark or download guidance unless it becomes publicly inspectable and its model card and weights can be validated.

## Strix Halo Guidance

- Do not present either community `27B` page as an official Qwen release.
- Do not start a one-box download of the official Qwen3.8 artifacts.
- Watch for an official or well-proven partitioned low-bit artifact and a runtime that supports the architecture.
- Treat a future route as multi-node or distributed evidence until its complete artifact size and memory plan fit a documented system topology.
- Keep any future server, speculative, or distributed result separate from direct single-box benchmarks.

## Buyer And Vendor Value

This negative triage removes a real adoption risk: a current model name and a community repository title can look like a practical local route even when no downloadable weights or compatible AMD runtime are present. Recording the blocker prevents wasted storage, bandwidth, and setup time while keeping the guide ready to test a credible route when one appears.
