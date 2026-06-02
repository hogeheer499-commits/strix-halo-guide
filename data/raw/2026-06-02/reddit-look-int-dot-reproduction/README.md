# Reddit Look_0ver_There Reproduction And Qwen3.6 27B Follow-Up

This directory contains a local Beelink follow-up prompted by Reddit discussion around the Qwen3-Coder 30B `Q4_K_S` 98.5 t/s headline.

## Files

- `look-exact-reproduction.log`: exact local reproduction of the `llama-bench -fa 1 -n 128` and repeated `-p 0` command shapes on llama.cpp `1fd5f4803`.
- `qwen36-27b-q8-direct-b9467.log`: direct `llama-bench` check for the official Qwen3.6 27B MTP `Q8_0` GGUF on the same source commit.

## Summary

The local Beelink did not reproduce the Reddit-reported GMKtec 100 t/s Qwen3-Coder result on the same source commit. The key visible local difference is that `llama-bench --list-devices` reports `int dot: 0` on this Beelink build path, while the Reddit-reported GMKtec output reported `int dot: 1`.

The host `vulkaninfo` output reports `VK_KHR_shader_integer_dot_product` and `shaderIntegerDotProduct = true`, but this host's Ubuntu `glslc` path did not support `GL_EXT_integer_dot_product` during the llama.cpp CMake feature test. That prevents the llama.cpp Vulkan integer-dot shader path from being enabled here.

The Qwen3.6 27B MTP `Q8_0` direct check landed at 7.70 t/s tg128. That matches the existing conclusion from the MTP server rows: the official dense 27B Q8 route is useful negative/control evidence, not a speed candidate versus the 35B-A3B MoE routes.
