# Starting On Windows (community and vendor sources, checked 2026-09-30, not measured by this guide)

This page collects what AMD, LM Studio and community reports say about running local LLMs on a Strix Halo system under Windows 11. The guide's measured route is native Linux. **No first-party Windows measurement exists in this guide**; the Windows rows it does have are community reports (see the last section). Versions, issue states and dates below were read on 2026-09-30 unless a different date is given.

## Short Version

- Windows works for Vulkan-based inference with Ollama or LM Studio ([README.md](README.md), FAQ "Do I need Linux? Can I use Windows?").
- Many community sources recommend Linux for this hardware. The reasons they give are memory handling, loading of large models and speed. These are claims of third parties; the guide has not run a same-machine comparison ([README.md#windows-vs-linux](README.md#windows-vs-linux)).
- Two things to check before planning around a large model on Windows: how much memory Variable Graphics Memory leaves for Windows, and whether models above about 48 to 64GB load at all (open reports, below).
- In LM Studio, choose the Vulkan runtime. The ROCm runtime has open correctness reports on this GPU.

## Memory: Variable Graphics Memory

The README states that AMD's Adrenalin drivers from 25.8.1 added Variable Graphics Memory (VGM) for up to 96GB. Two things the README does not say:

- **Less is left for Windows.** One community Windows report (128GB machine, Adrenalin 26.5.2, VGM set to 96GB) listed about 31.6GB as usable by the operating system ([raw report](data/raw/2026-06-02/community-windows-lmstudio-issue3/README.md)).
- **Loading above about 48 to 64GB failed for some users.** LM Studio issue [#1790](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/1790) was opened on 2026-04-13 and had its last reply on 2026-06-17; it was still open when read again on 2026-10-01. It reports, on Windows 11 with a 128GB Strix Halo, Adrenalin 26.3.1 and VGM at 96GB, that loading a 120B-class model with the Vulkan runtime fails at roughly 64GB. Commenters report the same behaviour with `llama.cpp` and `transformers` outside LM Studio, and one reports a test allocator that did not get past 48GB. AMD has not confirmed it. The release notes of Adrenalin 26.9.1 (2026-09-03) and 26.9.2 (2026-09-29) do not mention Ryzen AI Max, VGM or this problem, so **whether the current driver fixes it is unknown**. An older thread, [#1088](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/1088) (2025), reports large models loading only with a very large Windows pagefile or a 64/64 split.

The Windows evidence in this guide used a model of about 20GB, so it does not test this boundary. A Windows large-model load test (a GGUF between 64 and 90GB with VGM at 96GB) is listed in the [test queue](data/current_test_queue.csv). Until it is measured, treat loads above 64GB on Windows as unverified; the Linux profile in this guide (small fixed UMA plus GTT) is the tested route for large models.

## AMD's Official Windows Routes

None of these routes was run by this guide. All facts are from AMD's or the vendor's pages, read on 2026-09-30.

| Route | What the source says | Notes and limits | Source |
| --- | --- | --- | --- |
| Adrenalin "AI Bundle" | Optional bundle since Adrenalin 26.1.1: PyTorch on Windows, ComfyUI, Ollama, LM Studio and Amuse in one install; Ryzen AI Max is listed as supported. | About 35GB of disk space according to press reports. The release notes of 26.9.1 and 26.9.2 list a known issue: the install can fail in regions with restricted access to Hugging Face or GitHub. The bundle installs Ollama and LM Studio versions that this guide does not pin; compare the installed Ollama version with the advisories in [SECURITY.md](SECURITY.md). | [AMD blog](https://www.amd.com/en/blogs/2026/amd-software-adrenalin-edition-ai-bundle-ai-made-si.html), [FAQ](https://www.amd.com/en/resources/support-articles/faqs/ai_bundle.html), [26.9.2 notes](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-26-9-2.html) |
| ComfyUI Desktop | Official ROCm support on Windows since v0.7.0 (2026-01-06), based on ROCm 7.1.1; ROCm is selected during install. | Different from AMD's manual ComfyUI recipe (ROCm 7.2.1) that the README links. One Framework community post (2026-07-30) reports stable use of ROCm 7.14 in ComfyUI Portable and 20 to 30% faster runs than the default ROCm of ComfyUI Desktop (one owner, claim of a third party). | [ComfyUI blog](https://blog.comfy.org/p/official-amd-rocm-support-arrives), [forum post](https://community.frame.work/t/83762) |
| WSL with ROCDXG | Official AMD support for Ryzen Strix and Strix Halo on WSL since Adrenalin 26.2.2 with ROCm 7.2.1, through the ROCDXG library (`librocdxg`). | The guide has only a community WSL2/HIP baseline with a different workload ([README.md](README.md), "Windows vs Linux"). | [AMD WSL how-to](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/wsl/howto_wsl.html) |

**AMD's own limits for ROCm on Windows (Ryzen limitations page for release 7.2.1):** PyTorch only, no training, Python 3.12 only, officially batch size 1, and the page asks you to turn off Smart App Control and Windows Defender Application Guard ([source](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/limitations/limitationsryz.html)). The README links AMD's Windows ComfyUI recipe without mentioning these costs; whether that blog itself mentions the Smart App Control and Application Guard settings was not checked.

**Drivers.** Adrenalin 26.9.1 (2026-09-03) and 26.9.2 (2026-09-29) contain nothing specific to Strix Halo, ROCm or VGM in their release notes; 26.9.2 is on a new driver branch (26.20.15.02). For ROCm 10.0 on Windows and the `win-rocm-10.0` `llama.cpp` builds, see the dated paragraph in the README FAQ; it is also unmeasured here.

## LM Studio On Strix Halo

The guide's only LM Studio result used version 0.4.15 with the Vulkan runtime. What has changed since, as read on 2026-09-30:

| Version or issue | What the source says | Status |
| --- | --- | --- |
| 0.4.25 (2026-09-19) | Latest version read. | Not measured here. |
| 0.4.17 (2026-06-26) | Strix Halo supported through the `llama.cpp` 2.22.1 runtime (a maintainer says ROCm 7 is bundled). iGPUs under the Vulkan backend are shown but disabled by default. | What the Vulkan default means for Strix Halo was not checked. |
| 0.4.22 (2026-08-28) | MTP, DFlash and DSpark drafters, engine 2.29.1 or newer. | Not measured here. |
| 0.4.24 (2026-09-09) | Custom `llama.cpp` arguments. | Not measured here. |
| [#2310](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/2310) | ROCm runtime newer than 2.25 gives incorrect output on Ryzen AI Max (Windows). | Open, no LM Studio reply when read. |
| [#1502](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/1502) | Comment of 2026-08-19: Gemma 4 produces `<unused24>` tokens on the ROCm runtime 2.29.0 (Linux); Vulkan and CPU are correct. Upstream: [`llama.cpp` #26239](https://github.com/ggml-org/llama.cpp/issues/26239). | Both open when read. |
| [#2294](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/2294) | Vulkan runtime 2.29.0 decodes slower with MTP models than 2.27.1. | Open. |
| [#2376](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/2376) | Tool calls broke on ROCm extension 2.29.2 to 2.34.0; the reporter says it is fixed in 2.47.0 (2026-09-12). | Reporter's statement; not verified. |

These are reports by users; LM Studio has not confirmed them. The runtime version is separate from the app version, so **record both, plus the Adrenalin version, with every result.**

- **Authentication.** The LM Studio documentation says it does not require authentication by default and that "Serve on Local Network" binds beyond localhost; it recommends enabling authentication ([authentication](https://lmstudio.ai/docs/developer/core/authentication), [serve on network](https://lmstudio.ai/docs/developer/core/server/serve-on-network)). Enable it before you serve on the network.
- **Prompt logging.** A preprint ([arXiv 2609.18526](https://arxiv.org/abs/2609.18526), 2026-09-16; tested LM Studio 0.4.21 on Ubuntu with an NVIDIA GPU, **not** on Strix Halo or Windows) reports that LM Studio logged prompts in readable form by default and that no matches were found with a setting called `logSensitiveData` turned off. Check where your version exposes that setting.
- **Agent app.** The LM Studio website now leads with "Bionic", an agent app that offers shell modes up to "allow-all". Treat it as an agent that can run commands ([SECURE_LOCAL_AI.md](SECURE_LOCAL_AI.md)).

## Laptops: Display Off

One third-party Windows benchmark repository ([strix-halo-windows-llm-bench](https://github.com/ihanesman/strix-halo-windows-llm-bench), ROG Flow Z13 128GB, 2026-09-25) reports that the SoC clock falls to about 50% roughly 45 seconds after the display turns off, independent of Modern Standby, and that token rates fall to roughly a fifth of the display-on values (pp2048 248.3 t/s and tg128 11.90 t/s with the display on). Its suspected cause, AMD Platform Management Framework, is unconfirmed, and the workaround it gives is to keep the display on; all of its other numbers were taken with the display on. This is one source on one laptop. Whether mini PCs without a built-in display behave the same is unknown. See also [LAPTOPS_AND_HOMELAB.md](LAPTOPS_AND_HOMELAB.md).

## Windows Or Linux

In community threads and forums read on 2026-09-30, many answers to "which operating system?" say Linux, usually with the BIOS UMA buffer at its smallest setting (the profile this guide documents), a mixture-of-experts model and a Strix-specific engine. Some owners need Windows for work or games and run Lemonade or LM Studio with Vulkan, accepting lower speeds. Linux is also the only route with first-party evidence here. A dual-boot setup lets you compare on your own machine; if you do, [issue #3](https://github.com/hogeheer499-commits/strix-halo-guide/issues/3) (Windows versus Linux, open since 2026-05-07) is where a result is useful. Engines named in those threads are in [ENGINES.md](ENGINES.md); most are distributed as Linux containers, and Windows ports exist for some of them as separate forks (for example Gufo's README lists one).

## What This Guide Has Measured On Windows

Nothing first-party. The Windows rows in this repository are community reports:

- **LM Studio, native Windows.** One MS-S1-Max report: LM Studio 0.4.15 with the Vulkan runtime 2.18.0, Windows 11 Pro 25H2, Adrenalin 26.5.2, Qwen3.6 35B-A3B Q4_K_M (about 20GB), `n_parallel=4`, 262K context: 89.49 tok/s script average; the long 512-token prompt rows were about 69 to 70 tok/s. See [COMMUNITY_RESULTS.md](COMMUNITY_RESULTS.md#windows-lm-studio-ms-s1-max-report).
- **WSL2/HIP.** One GMKtec EVO-X2 report: 44.05 t/s on a TG512 generation-only run, while the same contributor's native Ubuntu Vulkan/RADV run measured 61.52 t/s on the guide's TG128 shape. Different workloads; not a same-machine comparison.

**Not measured:** loading models above 64GB on Windows; any ROCm route on Windows; the AI Bundle; ComfyUI Desktop; WSL with ROCDXG; LM Studio runtimes after 0.4.15; display-off throttling; the effect of different VGM sizes; a same-machine Windows versus Linux comparison.

**If you report a Windows result,** record the Windows build, Adrenalin version, VGM setting, LM Studio app and runtime versions, power mode, whether the display was on, the model and quant, and the context size.

Last checked: 2026-09-30; issue states re-read on 2026-10-01.
