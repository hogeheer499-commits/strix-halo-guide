# FastFlowLM / NPU Preflight - 2026-05-16

This directory records a non-invasive NPU preflight for the Beelink GTR9 Pro.

Primary source:

- FastFlowLM Linux setup docs: <https://fastflowlm.com/docs/install_lin/>

Local result:

- The kernel has `amdxdna` loaded.
- `/dev/accel/accel0` exists.
- The NPU PCI device is present as AMD device `1022:17f0` at `0000:c7:00.1`.
- NPU firmware files are present under `/lib/firmware/amdnpu/`.
- XRT / FastFlowLM user-space tools are not installed:
  - no `xrt-smi`
  - no `flm`
  - no `lemonade` NPU runtime

Interpretation:

- The hardware and kernel driver are visible, but this is not enough to run FastFlowLM.
- A real NPU benchmark needs an XRT/FastFlowLM install lane, memlock validation, and likely a reboot.
- This should stay separate from the default Vulkan/RADV guide path until a tiny NPU model can be measured cleanly.
