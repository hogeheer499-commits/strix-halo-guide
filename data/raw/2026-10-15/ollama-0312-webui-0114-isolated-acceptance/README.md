# Isolated Ollama 0.31.2 and Open WebUI 0.11.4 acceptance — October 15, 2026

On an existing Beelink GTR9 Pro, the official Ollama 0.31.2 binary produced
`STRIX_CHECK=391` through the guide's checker and Open WebUI 0.11.4. After
restarting both temporary processes, a normal browser login and a new prompt
produced `STRIX_RESTART=391`. The runner logged 42/42 layers on the Radeon
8060S through Vulkan/RADV; the loaded-model API placed the entire model on GPU.

The pinned UI started with a new, empty data directory. Its first administrator
account could be created with `ENABLE_SIGNUP=False`; a second registration was
rejected with HTTP 403. Cookie-free model-list and generation requests returned
401. Community sharing and direct connections stayed disabled after restart.
Both temporary listeners were bound only to `127.0.0.1`.

[`evidence.json`](evidence.json) records artifact identities, checks and test
adaptations. The official model manifest and all five existing blobs were
verified by full SHA256. Separate ports, a bind directory and a temporary
restart policy kept the running installation separate. The checker was
imported unchanged with its port constant set to 11436; its success message
still printed the default 11434. This does not verify the default-port command
end to end. The UI onboarding sequence was **Get started → Create Admin
Account → close the release notes → select the local model → send a prompt**.

This is component acceptance on an existing host, not a fresh native
`setup.sh` installation. It does not qualify BIOS changes, the GPU-specific
upstream installer path, Docker installation, host reboot, recovery, access
from another device, security or model quality. The UI downloaded an embedding
model and checked for updates during startup; this is not an offline/no-egress
test. No performance claim is made. Runtime and UI pins still need a current
advisory review before installation.

The temporary processes were stopped; the existing installation remained
available. Private browser captures, local account data and host paths are
excluded from this bundle.
