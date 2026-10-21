# Clean Ubuntu VM installer test — 2026-10-14

The original setup script completed with exit **0**, including real package upgrades, Ollama **0.31.2**, service readiness and the **22.6GB** model download with digest verification. **Boot acceptance failed after reboot:** all three required kernel parameters were missing; both GPU groups passed.

Ubuntu's cloud-image GRUB fragment overrode the script's edits to `/etc/default/grub`. The revised script was then tested on a **second empty overlay of the same verified clean image**. It stopped with exit **1** at that fragment. Before/after system snapshots were identical across **108 entries**, and Ollama/model storage remained absent. This validates the new stop condition, not a full fresh installation of the revised script.

[evidence.json](evidence.json) records exact input hashes, the signed official image/checksum provenance, guest commands, output excerpts, model identity and equal snapshot hashes. Named full source captures remain private and are identified there by hash.

The guest genuinely reported **125GiB** to `free -g`; OS/RAM checks were not bypassed or mocked. The VM used two vCPUs, no GPU passthrough and no shared writable host filesystem. Hard resource limits, free-page reporting and bounded guest cache reclamation protected the host; no performance claim follows. No host sudo, package, network, persistent-service or reboot changes were made. Both test guests were powered off.

This is **installer plumbing plus a demonstrated boot failure and verified guard fix**. The upstream installer detected no GPU, so its GPU-specific download path was not exercised. It does not qualify Strix Halo BIOS/GPU behavior, inference, answer quality, WebUI or native-hardware reboot. The 0.31.2 runtime/model identity is separate from the earlier 0.32.15 GPU probe, and the default runtime's advisory caveat remains.
