# Local Chat: Start And Acceptance Checks

Read/reviewed 2026-10-03. This path targets native Ubuntu 24.04 and Linux Docker
Engine. Other operating systems, Docker Desktop and 64/192GB profiles need their
own qualification. You can stop after terminal chat; a browser UI is optional.

## Before You Install

| Component | What is established | What is still open |
|---|---|---|
| Ollama 0.31.2 | Historical text/vision/service/full-reboot qualification | Known advisory ranges include it; qualification is not a security approval |
| Existing Ollama 0.32.15 | Scoped September 19 text/image/tool/client acceptance after service restart | No new full-host reboot; that host's API was LAN-reachable |
| Ollama 0.35.1 | Stable release observed 2026-10-03 | No local upgrade/client/reboot qualification; no confirmed fix for CVE-2026-85180 established |
| Open WebUI 0.11.4 below | Release source and registry digest read; patches listed in the published advisories | The new loopback-only installation, client and reboot checks have not run here |

**Safety panel:** keep the unauthenticated Ollama API and the UI on loopback.
Keep WebUI login enabled; do not expose either service directly to LAN, tailnet
or the internet. A firewall alone does not establish that Docker/Tailscale paths
are closed. Confirm listeners and denial from a second device. See
[security status](SECURITY.md#security-status-of-pinned-components) before choosing
a runtime; there is no currently qualified, fully patched fresh-install promise.

If you already have a working setup, record the versions and model identities
before changing it. Back up data and confirm how to restore it. The
[128GB-class setup script](README.md#setup-script) changes boot, driver and service
configuration; read its scope first. Its revised fresh-install/upgrade path is
offline-fixture-tested, not hardware-qualified. A successful script exit is not
the acceptance result below.

## 1. Get Terminal Chat Working First

Follow the [manual setup](README.md#quick-start-6-steps) for your qualified memory
profile. Native Ollama defaults to `127.0.0.1:11434`; review an existing nonlocal
`OLLAMA_HOST` deliberately, rather than widening it for a container. This
installer/UI profile requires the exact IPv4 endpoint `127.0.0.1:11434`; an
IPv6-only, alternate-port or localhost binding needs manual review.

```bash
curl --fail --silent --show-error http://127.0.0.1:11434/api/version
ollama list
ollama show qwen3.6:35b-a3b --parameters
ollama run qwen3.6:35b-a3b
# While the model is loaded, in another terminal:
ollama ps
ss -ltn '( sport = :11434 )'
```

Pull the model first if it is missing. Model tags move: record the manifest ID,
weight blob and draft settings when comparing with a measured result. Confirm a
visible answer and GPU offload with `ollama ps`/runtime logs; receiving a text
response alone can also be a CPU path. Port 11434 must be loopback-only. Stop
and review if it listens on `0.0.0.0`, `*`, `[::]` or a nonloopback address.

## 2. Optional Browser UI: Linux Docker Engine

**Patched candidate, not yet qualified here.** Docker must already be installed.
This uses host networking so WebUI can reach native, loopback-only Ollama. Host
networking shares the host network namespace; it is not a sandbox and `-p` port
mappings would be ignored. Both `HOST` and `PORT` are explicit.

Use this for a **new** installation, with an unused container name and new data
volume. Do not attach an old volume or overwrite an existing container. A
database migration can prevent rollback: an existing installation needs a
separate, verified backup/restore and migration plan.

```bash
# Both names must be unused. Stop and choose new names if either exists.
if docker container inspect strix-webui-local >/dev/null 2>&1 || \
   docker volume inspect strix-webui-local-data >/dev/null 2>&1; then
  echo "Name or data volume already exists; stop and review before installing." >&2
else
  docker run -d --network=host --restart unless-stopped \
  --name strix-webui-local \
  -v strix-webui-local-data:/app/backend/data \
  -e HOST=127.0.0.1 -e PORT=3000 \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  -e WEBUI_AUTH=True -e ENABLE_SIGNUP=False \
  -e ENABLE_COMMUNITY_SHARING=False \
  -e ENABLE_DIRECT_CONNECTIONS=False \
  -e ENABLE_PERSISTENT_CONFIG=False \
  ghcr.io/open-webui/open-webui@sha256:9591b13f13843c7721c2b8eaf7382846c81b3ffe126526d1888d1fed50c6a33f
fi
```

That digest is the public multi-platform `v0.11.4` registry index observed on
2026-10-03; it includes Linux amd64. No image was downloaded or run for this
documentation review. Check for newer advisories before deployment; a fixed
digest does not receive patches automatically.

Inspect `ss -ltn '( sport = :3000 or sport = :11434 )'`, then open
`http://127.0.0.1:3000`. Create the first administrator yourself before other
local users can reach it. The v0.11.4 signup handler allows initial administrator
creation even with `ENABLE_SIGNUP=False`; this is source-read behavior, not a
UI test here. Subsequent signup is disabled. If bootstrap or login fails, stop
and collect a redacted error; do not disable authentication as a workaround.

Nonpersistent configuration makes the environment the startup configuration.
Admin changes can still apply in memory during the running process, but are not
stored in the configuration database and are lost on restart. Recheck login,
signup and sharing after any admin change. To change a setting, recreate this
container deliberately with the same pinned image, reviewed environment and
retained volume. Do not put passwords, keys or customer documents in a bug report.

Sources read 2026-10-03: [startup host/port](https://github.com/open-webui/open-webui/blob/v0.11.4/backend/start.sh),
[configuration defaults](https://github.com/open-webui/open-webui/blob/v0.11.4/backend/open_webui/config.py),
[in-memory/nonpersistent behavior](https://github.com/open-webui/open-webui/blob/v0.11.4/backend/open_webui/models/config.py),
[first-admin signup](https://github.com/open-webui/open-webui/blob/v0.11.4/backend/open_webui/routers/auths.py),
[release](https://github.com/open-webui/open-webui/releases/tag/v0.11.4) and
[published advisories](https://github.com/open-webui/open-webui/security/advisories).

## 3. Use From Another Computer

On your client, use your existing authorized SSH account and replace
`user@your-box` with it. The two loopback addresses refer to different machines.

```bash
ssh -N -L 127.0.0.1:3000:127.0.0.1:3000 user@your-box
```

Open `http://127.0.0.1:3000` on the client. Keep the tunnel running and WebUI
login enabled. This assumes the explicit port 3000 above and a working SSH
configuration; it does not require publishing Ollama. Confirm direct access to
11434 and 3000 is denied from another device on each applicable LAN/tailnet and
IPv4/IPv6 path. A check on the server itself does not establish this boundary.

## 4. Acceptance: When Is The Installation Working?

Record pass/fail/not tested for each item, with exact runtime/image/model IDs:

1. Terminal chat and WebUI model discovery give a nonempty, visible response for
   the agreed local model; GPU use is confirmed while loaded.
2. Login succeeds, unauthenticated UI access cannot use the model, subsequent
   signup is disabled and community sharing is off.
3. Both listeners are loopback-only; direct access from a second device fails
   while the intended SSH tunnel works. Cover each applicable network/IP family.
4. After a planned service/container restart, repeat discovery, response, login
   and listener checks. Test automatic startup after a **separately authorized**
   host reboot. The candidate requests `unless-stopped`; Docker itself must start
   at boot and the retained container must not have been deliberately stopped.
5. If image input or tool calling is part of the workload, exercise it with the
   exact agreed artifact and client. Plain chat does not qualify these features.
6. Confirm backup/restore, agreed update ownership and which integrations or
   model tags can contact cloud services. Local-only/offline is a separate check.

For paid installation, agree on the workload, supported versions, these tests,
handover and remedy before accepting the order. Do not call it delivered merely
because software installed, and do not promise every model, plugin or future
upgrade. This document defines the checks; it does not report them as passed.
