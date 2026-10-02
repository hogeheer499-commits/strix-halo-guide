# Laptops, Homelab, Clusters And Extra GPUs (community sources, checked 2026-09-30, parts re-read 2026-10-02, not measured here)

This page covers setups that differ from the single mini PC on a desk that the rest of this guide measures: laptops and tablets, Proxmox/LXC and virtual machines, small clusters, adding a GPU, and NAS-style chassis. **The guide has no first-party measurement for any of these.** Numbers below are claims of third parties, labelled with source and date, unless marked as this guide's own earlier RPC results or as a calculation. Other pages that touch these topics, such as the buyer guide, link here for the details.

## Laptops And Tablets

**What is different from a mini PC:** the power profile and the charger decide how much power the chip gets, the display setting can change speed, the exact memory configuration varies, and the machine moves between networks.

| Topic | What the sources say | Source |
| --- | --- | --- |
| Power profiles (ProArt PX13) | Silent 50/40 W, Standard 65/55 W, Performance 85/70 W, Battery 60/55 W (the two numbers are the short-term and sustained limits). | [Notebookcheck review, 2026-02-25](https://www.notebookcheck.net/AMD-Strix-Halo-128-GB-RAM-in-a-13-inch-convertible-Asus-ProArt-PX13-GoPro-Edition-Review.1232755.0.html) |
| Sustained power (HP ZBook Ultra G1a) | About 55 W sustained, with up to 96GB assignable to the GPU. | [StorageReview preview, 2026-09-15](https://www.storagereview.com/review/hp-zbook-ultra-g3a-16-preview-192gb-of-unified-memory-aims-for-the-top-of-the-local-ai-laptop-leaderboard) |
| ROG Flow Z13 on Linux | The default `Performance` profile is limited to 80 W, manually up to 95 W; with a USB-C charger from another brand (65 to 100 W) the highest mode may be blocked. | [Linux guide for the Z13](https://github.com/ib99/ASUS-ROG-Flow-Z13-2025-Linux-Guide-Omarchy-CachyOS-Kernel) |
| Mini PCs, for context | Vendor specifications list up to 140 W (EVO-X2) and 160 W (MS-S1 MAX). | [Laptop and mini PC overview](https://www.ultrabookreview.com/70442-amd-strix-halo-laptops/) |
| Memory | Most Z13 retail configurations have 32GB; 64GB and 128GB only in some markets. The TUF A14 goes to 64GB at most. The exact configuration decides which models fit. | Same overview |
| Display off | One Windows benchmark repository reports about 50% clock and about one fifth of the token rate once the display is off ([details](WINDOWS_START.md)). | Single source |
| Network | A widely read Z13 recipe starts Ollama and Open WebUI with `podman --network=host`, which makes them reachable on every network interface. On a laptop that joins public Wi-Fi this matters more than at home. | [Recipe](https://gist.github.com/geeksville/d8ec1fc86507277e123ebf507f034fe9) |

**Effect of the power limit on LLM speed (extrapolation).** A community wiki measured `koboldcpp` with Vulkan (Q5_K_M quants) at power limits of 55, 85 and 120 W. That measurement was made on a mini PC with the GPU passed through to a Windows virtual machine, not on a laptop, so applying it to laptops is an extrapolation:

| Model | Prompt processing at 55 / 85 / 120 W | Generation at 55 / 85 / 120 W |
| --- | --- | --- |
| Gemma 3 27B (dense) | 77 / 89 / 95 t/s | about 6 t/s at all three limits |
| Qwen3 30B-A3B (MoE) | 92 / 95 / 95 t/s | 25 / 29 / 29 t/s |

Source: [strixhalo.wiki, Power Modes and Performance](https://strixhalo.wiki/Guides/Power_Modes_and_Performance/) (claim of a third party; not reproduced; page read 2026-10-02 in the wiki's public mirror repository). The source's own reading is that for LLMs memory bandwidth, which the APU power limit does not affect, appears to matter more than raw compute (its reading; not checked here). Setup stated by the source: `koboldcpp` with Vulkan and Q5_K_M quants, the GPU passed through to a Windows virtual machine with 12 CPU cores (the source says this costs at least 5% of performance), and values rounded to whole tokens per second (dense generation 6 / 6 / 6; Qwen3 30B-A3B generation 25 / 29 / 29). This guide's own caution, not the source's: the virtual machine setup may limit the result, so do not use this run to predict laptop generation speed. On battery, a limit of about 55 W is reported for the ProArt PX13 (claim of a third party).

**If you run an LLM on a laptop:**

- Check the exact memory configuration of the model you buy; do not assume 128GB.
- Measure on mains power with the vendor's own charger and the highest vendor profile, and note the profile, mains or battery, and charger wattage in any report.
- Keep IOMMU enabled: `amd_iommu=off` prevented deep sleep on a reproduced Z13 case ([README.md#step-12-choose-the-iommu-policy](README.md#step-12-choose-the-iommu-policy)).
- Do not run Ollama or Open WebUI on `0.0.0.0` on a laptop. See [SECURE_LOCAL_AI.md](SECURE_LOCAL_AI.md).

**Smaller chips are a different class.** Laptops and handhelds with the Ryzen AI Max+ 388 and 392 exist, and the README notes that they are not measured here. A review of a 388 laptop (2026-08-27) lists 32GB, and comments mention a 64GB 392 variant, which was not verified. With 32 to 64GB such machines fall outside the 128GB-oriented advice in this guide. Check the memory size on the vendor page before relying on any model recommendation here.

## Proxmox, LXC And Virtual Machines

Community recipes for Proxmox on Strix Halo disagree with each other and, in places, with this guide's evidence. None was run by this guide.

| Topic | What community recipes say | What this guide says or measured |
| --- | --- | --- |
| IOMMU | A [Level1Techs guide for the Minisforum N5 MAX](https://forum.level1techs.com/t/n5-max-proxmox-strix-halo-with-docker-rocm-fp4-and-mtp-ultimate-setup-guide/251182) (tested 2026-06-06 on Proxmox VE 9.1.1, ROCm 7.2.1) calls `amd_iommu=off` required and says ROCm allocations are otherwise limited to about 2GB. | Keep IOMMU enabled for VFIO and passthrough. A GMKtec EVO-X2 run with IOMMU on reproduced the guide's row within about 2%. On a hypervisor, `amd_iommu=off` also removes VM passthrough ([README.md](README.md#step-12-choose-the-iommu-policy), [setup guide](docs/amd-strix-halo-setup.md)). |
| Memory values | The same guide sets the 128GB values (`gttsize=131072`, `ttm.pages_limit=31457280`) on a 64GB system and calls this harmless. | "Do not copy these limits to 64GB/96GB or 192GB systems" ([README.md](README.md)). Set the limits for the RAM you have. |
| HSA override | `HSA_OVERRIDE_GFX_VERSION=11.0.0` in one guide, `11.5.0` in a [Proxmox forum thread](https://forum.proxmox.com/threads/proxmox-9-x-strix-halo-gpu-passthrough.181331/) (2026-03-03). | Start with no global override. A stale `11.0.0` override crashed ROCm 7.2.4 in a dated Beelink validation ([README.md](README.md)). |
| ROCm on the host | The Proxmox forum thread installs ROCm from the Ubuntu noble repository on a Debian trixie host and copies firmware from `linux-firmware` git master. The Level1Techs [review notes](https://forum.level1techs.com/t/nas-review-notes-minisforum-n5-max-amd-strix-halo/251183) for the same hardware advise containerising GPU workloads and not installing ROCm on the Proxmox host. | The guide records a `linux-firmware` tag that broke ROCm ([Step 4.4](README.md#step-44-linux-firmware)). |
| Network exposure | The Proxmox forum thread sets `OLLAMA_HOST=0.0.0.0` and `OLLAMA_ORIGINS=*`. | Keep Ollama on loopback ([SECURITY.md](SECURITY.md)). |
| VM passthrough | [strixhalo.wiki](https://strixhalo.wiki/Guides/VM_iGPU_Passthrough/) reports a reset bug (a Windows guest works once per host boot), a need to extract the VBIOS and a fixed VRAM setting in the BIOS because dynamic allocation was unstable. The host loses the iGPU. | This is the opposite of the guide's small-UMA-plus-GTT model. Not tested here. |

**IOMMU note (dated).** Phoronix tested AMD's PerfOpt ([review](https://www.phoronix.com/review/amd-perfopt), 2026-09-29): an IOMMU bypass for iGPU memory access that is meant to be on by default in Linux 7.4 and can be turned off with `amdgpu.iommu_perfopt=0`. On a Framework Desktop (395, 64GB) with Lemonade it gave 2 to 4%; the larger gains in the headline apply to smaller chips. The patch was ready in the IOMMU tree but not yet merged when read. This may narrow the difference that `amd_iommu=off` makes; no comparison of PerfOpt against `amd_iommu=off` on Strix Halo was found, so this guide's policy is unchanged. Separately, `amd_iommu=off` also removes DMA protection against USB4 and Thunderbolt devices.

**Practical reading of the sources (none tested here):**

- For LLM work, an LXC container is the route the sources favour over a full VM, because the host keeps the GPU.
- The Vulkan route needs `/dev/dri` inside the container; the ROCm route also needs `/dev/kfd`.
- Keep the host to the `amdgpu` kernel driver; one source advises against ROCm on the host.
- Set `ttm.pages_limit` for the RAM you have, and start without a global `HSA_OVERRIDE_GFX_VERSION`.
- A privileged container shares more with the host than an unprivileged one. Weigh that before using a recipe that requires it.
- Comments on the Proxmox thread mention that `gttsize` is deprecated and that GID mapping caused problems, and one user reports more speed from `llama.cpp` with Vulkan.

## Clusters

The guide documents a USB4 `llama.cpp` RPC cluster ([COMMUNITY_RPC.md](COMMUNITY_RPC.md), [USB4_CLUSTER_TUNING.md](USB4_CLUSTER_TUNING.md)) and an RDMA/vLLM phase ([README.md](README.md#phase-9-multi-node-clustering-rdma)). The two RPC pages open with a "Security and cluster notes (checked 2026-09-30; advisory line 2026-10-02)" block, and [SECURE_LOCAL_AI.md](SECURE_LOCAL_AI.md#clusters) has a Clusters section; the sources behind them are summarised here:

- **RPC.** `llama.cpp` published an advisory for its RPC backend ([GHSA-j8rj-fmpv-wcxw](https://github.com/ggml-org/llama.cpp/security/advisories/GHSA-j8rj-fmpv-wcxw), 2026-03-26) that describes unauthenticated remote code execution needing only TCP access to the RPC port; the advisory (CVE-2026-34159, rated critical) lists builds up to b7991 as affected and names no patched version (read via the GitHub API, 2026-10-02). Upstream's RPC README (read 2026-10-02) calls the RPC backend fragile and insecure and says never to run the RPC server on an open network. This guide has not tested whether any RPC authentication exists. Treat an RPC port that others can reach as unsafe.
- **Ray and vLLM.** AMD's playbook "Clustering Two Ryzen AI Halos with RCCL" ([source](https://developer.amd.com/playbooks/clustering-rccl/), read 2026-09-30) starts a Ray head on port 6379 on the LAN address, runs vLLM with `--host 0.0.0.0` and connects Open WebUI with authentication set to none, using `sudo podman --network=host`. The Ray documentation ([source](https://docs.ray.io/en/latest/ray-security/index.html), Ray 2.58.0) says anyone who can reach the dashboard, jobs or client ports can execute arbitrary code; token authentication exists since Ray 2.52.0 and does not replace network isolation.
- **OOM protection.** The same playbook sets `RAY_memory_monitor_refresh_ms=0`, which switches off Ray's out-of-memory monitor (it names the shared memory as the reason). A model that is too large can then hang the whole machine instead of one process.
- **RCCL bulletin.** AMD published bulletin [AMD-SB-6033](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-6033.html) on 2026-09-30 for RCCL (fix: ROCm 7.14). It names Instinct products only; AMD does not say whether Ryzen AI Max is affected.
- **Vendors.** Lenovo's press release describes the ThinkCentre X Ultra as "cluster-ready" for up to four systems ([press release](https://news.lenovo.com/pressroom/press-releases/hybrid-ai-for-business-devices-displays-solutions/)); this is a vendor claim.

**Reading of the sources:** cluster only over a dedicated link (a direct cable or an isolated VLAN); enable Ray token authentication (2.52.0 or later); do not publish ports 6379 or 8265 or the vLLM API to the LAN, or protect the API with `--api-key`; bind `rpc-server` to the cluster link only. See [SECURE_LOCAL_AI.md](SECURE_LOCAL_AI.md).

### One 192GB Box Or Two 128GB Boxes?

Nothing here is measured. At some vendors one 192GB box cost roughly as much as two 128GB boxes when checked on 2026-09-30; see the buyer guide for dated prices with country, currency and VAT status.

| Factor | One 192GB box | Two 128GB boxes |
| --- | --- | --- |
| Memory | 192GB in one memory space | 256GB split over two machines; a model must be sharded across them |
| Bandwidth | Same 256-bit bus as a 128GB box: 256 GB/s at 8000 MT/s or about 273 GB/s at 8533 MT/s (calculation, not measured). Vendor pages disagree on the speed of 192GB systems, so check with `dmidecode -t memory`. | Each box has its own bus; the shards talk over a network or USB4 |
| Measured by this guide | Nothing on 192GB | 2-node RPC lost about 14 to 22% generation speed on models that fit on one box; 3-node was slower again; MiniMax-M2.7 (140.8GB) needed two nodes ([COMMUNITY_RPC.md](COMMUNITY_RPC.md)) |
| Setup | One machine | Two machines, a dedicated link and matching software versions (the RPC protocol major version must match; see the caveat in [COMMUNITY_RPC.md](COMMUNITY_RPC.md)) |
| Power | One box | Two boxes; wall power is not measured here for either |
| Security | Normal single-host exposure | Cluster services must stay off the LAN (above) |
| Suits | Large MoE models within the capacity of one box. A vendor-published claim puts DeepSeek V4.1 Flash at Q2 on one 192GB machine at about 14 t/s ([docs/models.md](docs/models.md)); not reproduced. | Models above 192GB. AMD's playbook runs a 397B-parameter MoE (GPTQ Int4) over two 128GB nodes; at 4 bits that is roughly 200GB of weights, which does not fit one 192GB box (arithmetic, not measured). |

For dense models, generation speed falls roughly in proportion to the bytes read per token (the rule of thumb in the README); for MoE models only the active experts are read, so more memory mainly buys capacity. Vendors advertise up to 160GB addressable by the GPU on 192GB systems; this was not verified here and the guide has not tested a 192GB system.

## Adding A GPU

The guide has no measured eGPU or dGPU result. What owners and vendors report (claims of third parties):

| Report | Source |
| --- | --- |
| Two R9700 cards behind an external PCIe switch made prompt processing up to 2.2 times faster; the iGPU adds capacity but not decode speed. Three kernel-level problems had to be fixed first (`pci=realloc`, `runpm`, `vm_size`). | [Level1Techs thread](https://forum.level1techs.com/t/franken-strix-halo-2x-r9700s-128gb-strix-halo-unified-memory/254736), 2026-08-31 to 2026-09-03 |
| A Bosgame M5 froze repeatedly with an eGPU over USB4 (Fedora 44) and worked through an M.2-to-OCuLink adapter; an EVO-X3 stopped booting after a BIOS change for OCuLink. | [Level1Techs thread](https://forum.level1techs.com/t/gmktec-evo-x3-ai-workstation-lemonade-benchmarks-and-specs/253262) |
| Most boards from the Sixunited family have no OCuLink port; an M.2-to-OCuLink adapter uses an NVMe slot and gives PCIe Gen4 x4. For AMD eGPUs the GPU power limit is tied to the APU limit set in the BIOS; no problems were reported for NVIDIA cards. | [strixhalo.wiki, External GPU](https://strixhalo.wiki/Guides/External_GPU/) |
| LM Studio did not detect the iGPU when a dGPU was present ([lmstudio-bug-tracker #705](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/705), opened 2025-06-14 against 0.3.16); Jan used both but failed when the model was larger than the first GPU; BAR-space problems were reported with large cards; `ik_llama.cpp` was named for the hybrid route. No measured `llama.cpp` gain for iGPU plus dGPU was found. | [Level1Techs thread](https://forum.level1techs.com/t/strix-halo-external-gpu/235280), 19 posts, last 2026-09-01 |
| The Framework Desktop's x4 slot is closed, so a riser is needed; OCuLink on that slot worked only at PCIe Gen3 and was unstable. | [Framework community, x4 slot thread](https://community.frame.work/t/what-external-gpus-work-reliably-in-the-x4-slot/82939) and [mainboard thread](https://community.frame.work/t/framework-desktop-mainboard-and-full-size-video-card/85138) |

Vendor specifications (2026-09-30): the Minisforum MS-S1 MAX has a PCIe x16-sized expansion slot and the Framework Desktop a x4 slot. **Reading of the reports:** a GPU can raise prompt-processing speed and add memory, decode speed does not always improve, USB4 links are reported as unstable, and OCuLink through M.2 is the route owners report as working. Expect BIOS and kernel work.

## NAS-Style Chassis (Minisforum N5 MAX)

The guide does not otherwise mention this chassis. From the vendor's store page and a review (2026-09-30 and 2026-05-27):

- **Memory split.** The Level1Techs [review notes](https://forum.level1techs.com/t/nas-review-notes-minisforum-n5-max-amd-strix-halo/251183) (Proxmox VE 9.1.1) report that on the 64GB variant the GPU sees about 30 GiB by default (2 GiB fixed plus about 28 GiB GTT; the review says the default BIOS partition splits the memory roughly 50/50 and names BIOS settings and kernel parameters as ways to change it), and that models above about 30 GiB load only after the memory split is changed. This guide has a memory profile only for 128GB systems (the recorded 128GB Beelink profile, [README.md](README.md#step-32-configure-grub-boot-parameters)); it has no profile for 64GB, 96GB or 192GB machines, and `setup.sh` accepts only about 120 to 136 GiB of visible RAM. Do not copy the 128GB values to another size. The review also reports that VAAPI decoding failed and that the memory is soldered, so it cannot be upgraded later. All of this is claims of one review of one chassis (read 2026-10-02): not tested here and not checked for other systems, so confirm the memory configuration with the seller before ordering.
- **Preinstalled agent.** The vendor's product text says the NAS operating system ships with a local AI agent that runs Qwen3.6-35B by default, with per-account container isolation (vendor claims, not checked here). An agent with access to shared files is the case where prompt injection through a document matters most. Until you have reviewed what it can reach, give it read access to one folder and disable automatic actions ([SECURE_LOCAL_AI.md](SECURE_LOCAL_AI.md)).
- **Connectivity.** The vendor lists 10GbE (Realtek RTL8127) and two USB4 V2 ports at 80 Gbps.

## Not Measured

All routes on this page: a laptop at any power profile; Proxmox, LXC or VM passthrough; any cluster other than the USB4 RPC report; any 192GB system; an extra GPU; the N5 MAX.

Last checked: 2026-09-30; some issue and thread states re-read on 2026-10-01.
