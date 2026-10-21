# Get Local AI Running On Strix Halo

<a id="local-chat-start-and-acceptance-checks"></a>

Follow these steps to run a local AI model on your own computer, get an answer
in the terminal, check that it runs on the GPU rather than the CPU, and check
that Ollama currently listens only on the loopback address. After that, you
choose a model for your work and, if you want, a chat window in your browser.

**Is this your system?** This route is for an AMD Strix Halo / Ryzen AI MAX+ 395
machine with **128GB installed**, showing 120–136GiB to Linux, with **Ubuntu 24.04**
installed directly on the hardware. A larger machine that reserves memory in the
BIOS can show the same amount and is still not covered. For another memory size,
Windows or another operating system, use the [manual reference](README.md#quick-start-6-steps)
or the [Windows route](WINDOWS_START.md); each has its own checks.

Where this route stands: the current setup script has **not yet been run from
start to finish on a freshly installed Strix Halo**. Parts of it were checked
separately; see [what has been checked](#version-and-security-status). Read the
result of every step instead of assuming it worked.

## Before You Install

**What you need:** the system described above with Ubuntu already installed, an
internet connection (the model download alone is large), a normal user account
that can use `sudo`, and a backup of anything you cannot afford to lose. Save
your work before the reboot in step 4. The script does not install Ubuntu and
does not change BIOS settings; the BIOS is yours to set in step 1.

- **The script changes your system.** It edits the boot settings (GRUB), adds
  your user to the GPU groups, writes an Ollama service setting, adds the kisak
  Mesa driver PPA and runs a full `apt upgrade -y`. If it stops halfway, the
  changes made so far stay in place; there is no automatic rollback. The
  [manual undo table](README.md#undo-the-setup-script) exists but is **untested on hardware**.
- **Ollama has no password.** Anyone who can reach its port can use it. Keep
  Ollama, and any browser interface, listening only on this computer (the
  loopback address). Do not open them to your home network, a tailnet or the
  internet. A firewall alone does not prove this boundary. Step 5 checks the
  current Ollama listener; the optional browser interface has its own checks.
- **A fresh machine gets Ollama 0.31.2.** That is the version this guide
  measured through a full reboot, but it also falls inside published security
  advisories. Read the [security status](SECURITY.md#security-status-of-pinned-components)
  before you continue, so the choice is yours.
- **Already have Ollama working?** The script keeps your existing Ollama
  version. Before you change anything, [write down what you have and test your backup](#existing-installations-and-upgrades).

Before you install, confirm your system and your free disk space with these
read-only checks:

```bash
cat /etc/os-release
free -h
LC_ALL=C lscpu | grep 'Model name'
df -h / /usr/local /usr/share /var "$HOME"
df -i / /usr/local /usr/share /var "$HOME"
```

**Continue when:** the output shows Ubuntu 24.04, a Ryzen AI MAX+ 395 and
roughly 120–136Gi of memory, and every filesystem in the two `df` lists has
plenty of free space (`df -h`) and free inodes (`df -i`). Inodes are a
filesystem's limit on the number of files; a disk can run out of them before it
runs out of bytes. If you keep models or backups somewhere else, run both `df`
commands on that directory as well.
**Stop if:** any of those filesystems is nearly full or out of inodes, or you
cannot see room for the model download, the package upgrade and a recovery
copy. Do not make room by deleting models or backups to pass this check.

<details>
<summary>Why there is no exact disk-space number</summary>

On 2026-10-14 the model tag pointed to **22.6GB of model files (blobs)** (21.1GiB); the
tag can move to a different size later. That figure covers only the model. A
fresh installation also needs room for the Ollama runtime, AMD runtime files,
the package upgrade and its cache, your backups and working space. A safe total
has not been measured, so this page does not name one. By default Ollama stores
models under `/usr/share/ollama`, which is why the checks include that path;
free space on `/` says nothing about a model store or backup on another disk.

</details>

## 1. Get Terminal Chat Working First

### Step 1: Set The BIOS Memory Option

In the BIOS, set the **UMA Frame Buffer** (memory reserved for the GPU) to
**512MB if offered**, or to the lowest value your vendor allows, often **2GB**.
The small BIOS reservation leaves more memory available to Linux; on this
route the GPU can also use shared memory managed by Linux. Leave **IOMMU** at
**enabled/default**, save, and boot Ubuntu.

**Good:** Ubuntu boots and Linux sees 120–136GiB. **If not:** put the BIOS back
to a setting that boots and stop here. Do not try to make a different memory
size fit the 128GB values; see the [BIOS reference](README.md#phase-1-bios-configuration).

<!-- PAID_HELP_STEP: bios -->
Stuck? Get free error help in [Discussions](https://github.com/hogeheer499-commits/strix-halo-guide/discussions) or [paid setup help on strixhaloguide.com](https://strixhaloguide.com/services/#setup-rescue).

### Step 2: Get And Review The Guide

The commands below install the few tools the script needs and download this
guide into a new folder, `$HOME/strix-halo-guide`. If that folder already
exists, stop and check what is in it before you reuse it.

```bash
sudo apt update
sudo apt install -y git curl python3 zstd software-properties-common
cd "$HOME"
git clone https://github.com/hogeheer499-commits/strix-halo-guide
cd "$HOME/strix-halo-guide"
less setup.sh
```

The last command opens the setup script so you can read what it will change;
press `q` to close it. **Good:** every command finishes without an error and
you have seen the script. **If not:** stop at the first error, whether it comes
from a package, a signature, the network or the download. Do not work around
the script's own check for missing tools. That preflight stops setup.sh before
that script makes changes; the package commands above already change the system.

<details>
<summary>Reproducible run</summary>

A fresh download gives you the latest `main` branch, which changes over time.
To run exactly the version you reviewed, switch to a tag or commit with
`git checkout <tag-or-commit>` before running setup. No tag is currently marked
as tested on hardware for a fresh installation with the revised script.

</details>

### Step 3: Run The Setup Script

From the `$HOME/strix-halo-guide` folder, as your normal user. This is the
long step: it upgrades packages and downloads the model.

```bash
bash setup.sh
```

**If the output says `REBOOT REQUIRED`, reboot before you test any model**,
even though an earlier line in the summary may already show a quick-start
command. By default the script leaves your power settings alone. It configures Ollama to
use the GPU through Vulkan/RADV and downloads a model that the next steps use
to check the installation; you pick a model for real work later.

**Good:** the output ends with `Configuration run finished; qualification pending`.
That line means the configuration was written; steps 4 to 7 show whether it
works. **If not:** note the first error message, not the last, and look it up
in [If A Step Fails](#if-a-step-fails). Changes made before the error are still
in place, so do not simply run the script again and again.

<!-- PAID_HELP_STEP: setup -->
Stuck? Get free error help in [Discussions](https://github.com/hogeheer499-commits/strix-halo-guide/discussions) or [paid setup help on strixhaloguide.com](https://strixhaloguide.com/services/#setup-rescue).

### Step 4: Activate And Check The Boot Settings

Only if the script asked for a reboot: save your work, then run:

```bash
sudo reboot
```

After you log back in, go back to the guide folder and let the checker read
the live settings. If the `cd` part fails, stop; the checker must run from
inside the guide folder.

```bash
cd "$HOME/strix-halo-guide" && python3 scripts/check_local_ai.py boot
```

**Good:** each of the three boot parameters and both GPU groups (`render`,
`video`) shows `OK`, and the last line is `PASS`. If the script only added you
to groups and did not ask for a reboot, log out completely and back in first;
group changes take effect at login. **If not:** stop at the first `MISSING` or
`STOP` line and compare it with the [boot settings](README.md#step-32-configure-grub-boot-parameters)
or [GPU access](README.md#step-34-verify-gpu-access) reference. Fix the setting
that is wrong; do not add a second, competing configuration next to it. If
Ubuntu no longer boots, use the recovery path you prepared. The
[manual undo table](README.md#undo-the-setup-script) is still untested on hardware.

<!-- PAID_HELP_STEP: reboot -->
Stuck? Get free error help in [Discussions](https://github.com/hogeheer499-commits/strix-halo-guide/discussions) or [paid setup help on strixhaloguide.com](https://strixhaloguide.com/services/#setup-rescue).

### Step 5: Get Your First Answer And Check A Known Task

This is where you find out whether it works. If you opened a new terminal, go
back to the guide folder first; stop if the `cd` part fails. You can read
the checker first with `less scripts/check_local_ai.py`. It does not change
your system configuration; `answer` sends one local model request, which can
load the model and use the GPU.

```bash
cd "$HOME/strix-halo-guide" && python3 scripts/check_local_ai.py answer
```

The checker first checks that every Ollama listener on port 11434 is bound to
`127.0.0.1` in the current Linux network namespace, then asks the model a
question with one right answer: 17 × 23. The listener check describes that
moment; it does not test a browser interface or access from a second device.
**Good:** you see `Answer: STRIX_CHECK=391`, `Completion: True stop` and
`PASS`. That means the model answered, answered correctly, and finished
normally. On October 15 this checker passed with an isolated 0.31.2 runtime
on a separate port; a fresh native installation remains unverified.
**If not:** stop at the error line, which is written to be readable, and look it
up in [the failure table](#if-a-step-fails). Do not "fix" a listener warning by
opening Ollama to the network, and do not treat a speed figure as a substitute
for a correct answer.

Now have a real conversation with it. The `OLLAMA_HOST=` part at the front makes
sure the command talks to the Ollama on this computer and nothing else:

```bash
OLLAMA_HOST=http://127.0.0.1:11434 ollama run qwen3.6:35b-a3b
```

Type a question, for example: **Explain two useful things I can do with a local
AI assistant, in two short sentences.** **Good:** a readable answer appears and
you get the prompt back. A fluent answer can still be wrong; this model was
measured for speed, not ranked for answer quality. Type
`/bye` to leave the chat. **If not:** stop and read the last lines of the Ollama
service log with `journalctl -u ollama -n 50`. If you ask for help, share only
the lines that show the error, with anything private removed.

<!-- PAID_HELP_STEP: first-answer -->
Stuck? Get free error help in [Discussions](https://github.com/hogeheer499-commits/strix-halo-guide/discussions) or [paid setup help on strixhaloguide.com](https://strixhaloguide.com/services/#setup-rescue).

### Step 6: Confirm GPU Use

If Ollama still has the model loaded after the chat, ask it where the model
is running:

```bash
OLLAMA_HOST=http://127.0.0.1:11434 ollama ps
```

**Good:** the model's processor column shows `100% GPU`. (That is the expected
value; this page does not reproduce a captured run.) If the model has already
unloaded, repeat the chat in step 5 once and check again. **If not:** `CPU`, or
a mix of CPU and GPU, means the model is not fully on the GPU and this check has
not passed. Follow the [CPU fallback troubleshooting](README.md#troubleshooting)
before you look at speed. An answer on screen proves nothing here: the CPU can
produce one too.

<!-- PAID_HELP_STEP: gpu -->
Stuck? Get free error help in [Discussions](https://github.com/hogeheer499-commits/strix-halo-guide/discussions) or [paid setup help on strixhaloguide.com](https://strixhaloguide.com/services/#setup-rescue).

### Step 7: Check Speed, Then Start Using It

```bash
OLLAMA_HOST=http://127.0.0.1:11434 bash ~/bench-ollama.sh
```

This runs the small benchmark that the setup script placed in your home folder.
**Good:** three lines, `Prompt eval`, `Generation` and `Total time`, each with a
value above zero. **If not:** use the failure table. If `Generation` shows only
a few tokens per second on this model, go back to step 6 and recheck for CPU
fallback. Speed figures say nothing about whether answers are correct or whether
the GPU is used; steps 5 and 6 cover those.

<details>
<summary>What speed to expect</summary>

When this guide measured Ollama 0.31.2 with an earlier build of the same model
tag, generation reached roughly 60 tokens/s. Treat that as an indication, not a
promise: the tag has since moved to a build with MTP drafting, and the exact mix
of versions on your machine matters. The benchmark helper only checks that a run
completed with output and counters; it does not check whether the answer was
right or whether the model stopped normally. If the script found an older copy
of the helper and kept it, compare that copy with [`scripts/ollama_smoke.sh`](scripts/ollama_smoke.sh)
before you use it, and do not overwrite it just to run setup again.

</details>

**Done, if all checks above passed.** The model answered you, got a known task
right and runs fully on the GPU. The Ollama listener was bound only to
`127.0.0.1:11434` when checked; browser and second-device access need their own
checks below. Three
good next moves: save [your result](#your-result-save-and-share) so you can
compare later, pick a model that suits your work in [Best Known Profiles](BEST_KNOWN_PROFILES.md),
or set up a [browser interface](#2-optional-browser-ui-linux-docker-engine) for
everyday use. Once that works, the [manual guide](README.md#phase-4-performance-tuning)
shows how to get more speed out of it.

## If A Step Fails

| Message or symptom | What to do next |
|---|---|
| `Missing required commands: ... no system changes were made` | Install the named prerequisites first. `zstd` is provided by Ubuntu's `zstd` package; `add-apt-repository` by `software-properties-common`. Rerun only after that early prerequisite failure is resolved. |
| `This script is only recorded on Ubuntu 24.04` | Stop: use the manual reference for that OS. Bypassing the guard does not qualify it. |
| `This automatic memory profile is limited...` or `above the measured 128GB-class route` | Stop: check installed and visible RAM. Do not apply the 128GB limits to another size. |
| `GRUB drop-in needs manual review` or `Cannot inspect GRUB drop-in directory` | The installer stopped before changing the system. Extra boot configuration can override its settings. Keep those files; use the [manual boot-settings reference](README.md#step-32-configure-grub-boot-parameters) and ask for help reviewing the effective configuration. Do not delete a fragment to bypass the check. |
| `Ollama binding requires manual review` or `Ollama profile conflicts or missing values` | Review the existing service deliberately. Preserve administrator settings and loopback; do not disable the check. |
| `Existing legacy profile needs manual review`, `Conflicting ... in GRUB` or `Guide drop-in already exists with different content` | Preserve the files; follow the [manual configuration/access reference](README.md#step-34-verify-gpu-access). Resolve the specific conflict before considering a rerun. |
| `Ollama did not become ready within 30 bounded attempts` or `Benchmark failed` | Read `journalctl -u ollama -n 50`; share only the relevant redacted error. Do not publish full service environments. |
| `Existing ~/bench-ollama.sh differs; preserved` | Earlier configuration may already be applied. Compare the old helper with [`scripts/ollama_smoke.sh`](scripts/ollama_smoke.sh); do not delete it merely to rerun setup. |
| `This version requires zstd for extraction` from an older checkout | That failure may follow earlier system changes. Stop and inspect what already changed; install `zstd` only after review. The early tool check in the revised script prevents this particular missing-tool path. |
| Download fails or disk becomes full | Stop. Read `df -h`/`df -i` for the affected filesystem and preserve model data/backups. Resolve the storage budget and first error before retrying the pull; do not rerun the whole installer as a disk fix. |
| No answer, wrong task answer, or CPU/mixed placement | The route has not passed. Keep the exact version/model ID and redacted error; use [Troubleshooting](README.md#troubleshooting). |

**Free help.** [Search or ask in Discussions](https://github.com/hogeheer499-commits/strix-halo-guide/discussions).
Include the step number, your hardware and installed memory, the versions
involved (Ubuntu, Ollama, the model tag) and the exact error, with passwords,
keys, private paths and documents removed. If you need to undo what the script
changed, use the [manual undo table](README.md#undo-the-setup-script), which is
**untested on hardware**.

<!-- PAID_HELP_STEP: failure-table -->
**Personal help, paid.** If Discussions does not get you unstuck, the maintainer
offers [paid setup help](https://strixhaloguide.com/services/#setup-rescue) on
strixhaloguide.com. Send the same information you would post in Discussions:
the step where you stopped, your hardware and memory, the versions involved and
the redacted error. It covers one machine and one goal in a remote session, and
ends in either a working path or a clearly described blocker, with a short
written follow-up. It is a paid service; the scope and conditions are on that page.

## Your Result: Save And Share

Before you change versions or models, save a short record of what works now:

```bash
OLLAMA_HOST=http://127.0.0.1:11434 ollama --version
OLLAMA_HOST=http://127.0.0.1:11434 ollama list
OLLAMA_HOST=http://127.0.0.1:11434 ollama show qwen3.6:35b-a3b --parameters
# Run while the model is loaded:
OLLAMA_HOST=http://127.0.0.1:11434 ollama ps
```

**Good:** you have the runtime version, model tag/manifest ID, draft settings and
processor placement. Tags can change; a model weight-blob digest is also needed
for exact artifact reproduction, as described in [Reproducibility](REPRODUCIBILITY.md).
Do not present the tag alone as an identical measured artifact. If a command
fails, record that failure rather than filling in an expected value.

```text
Device / installed memory:
Ubuntu / kernel:
Ollama version:
Model tag / manifest ID:
Draft parameters:
Visible answer / task / normal completion: pass | fail | not tested
GPU processor placement:
Prompt eval / Generation / Total time:
Listener / second-device denial: pass | fail | not tested
Browser UI: not installed | pass | fail | not tested
```

Share a [benchmark report](https://github.com/hogeheer499-commits/strix-halo-guide/issues/new?template=benchmark-report.md)
or a [Discussion](https://github.com/hogeheer499-commits/strix-halo-guide/discussions);
[Share This Guide](SHARE.md) has reusable links. Reproducible community results
can be credited in [Community Results](COMMUNITY_RESULTS.md). If the guide saved
you time, a GitHub star helps other owners find it. Failed routes are useful
reports too; include the [step that failed](#if-a-step-fails).

**Keep it working:** write down versions and model IDs before any update, keep
a backup and test that it restores, and read the upgrade notes below before you
change a runtime that works. A first answer that works today says nothing about
an update you install later.

## 2. Optional Browser UI: Linux Docker Engine

For everyday use, you may prefer a chat window in the browser to a
terminal. Open WebUI is one option; nothing above depends on it, and it is not
the only choice. **The pinned version passed an isolated hardware check on
October 15:** a new data directory, first admin account, login, local model,
correct answer, loopback listeners and a restart of both the UI and Ollama.
Follow the checks below on your own machine too. Docker installation, a fresh
native setup and a full computer reboot remain unverified; this is not a
current security qualification. [See the test and its limits](data/raw/2026-10-15/ollama-0312-webui-0114-isolated-acceptance/).

**Security check October 21:** the [October 18 channel-webhook advisory](https://github.com/open-webui/open-webui/security/advisories/GHSA-3vvh-g22g-jq6r)
includes this 0.11.4 pin (affected: >=0.7.0,<0.12.2; patched: 0.12.2).
It requires enabled channels, a channel webhook and a member with write access.
The advisory says instances with channels disabled (the default), or without
channel webhooks, are not affected. Keep channels and channel webhooks off and
do not add untrusted users. This is source-based guidance, not a new mitigation
test. Newer stable 0.12.3 exists but has not been qualified here; a fixed image
digest does not receive patches automatically. [Full check scope](MAINTENANCE_REVIEW_2026-10-21.md).

You need Docker Engine already installed and working on this Ubuntu machine.
Installing Docker, and Docker Desktop, are outside this page. First check that
Docker responds:

```bash
docker version
docker info
```

**Good:** both commands print information without an error. **If not:** stop
and follow Docker's own installation and access documentation. Do not change
socket permissions or add yourself to the Docker group as a quick fix without
understanding what that grants. Terminal chat keeps working in the meantime.

The command below uses a container name and a **new data volume** that must not
exist yet. Do not point it at an old volume or replace an existing container: a
newer version may convert the database, and then you cannot go back. Leave login
switched on. The container shares the host's network so that it can reach Ollama
on loopback; that means it is not isolated from your machine's network, and `-p`
port mappings would be ignored.

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

**Good so far:** Docker prints a long container ID. That only means the start
was requested, not that the interface works. Check which addresses are
listening, then open `http://127.0.0.1:3000` in a browser on this computer:

```bash
ss -ltn '( sport = :3000 or sport = :11434 )'
```

**Good:** both ports show only `127.0.0.1`. In the browser, choose **Get started**,
then **Create Admin Account** and create your own first account right away,
before anyone else on this computer can. Close the release notes if they
appear, select your local model and send the same short prompts as in step 5.
Check that the answers are readable and that the GPU is still used.

The first account can be created even though signup is switched off
(`ENABLE_SIGNUP=False`); this worked in the October 15 browser test. A second
registration was rejected, and a request without a login cookie could not
generate an answer. Confirm on your machine that signup stays closed after the
first account, that a signed-out browser cannot use the model, and that
community sharing is off. The first start may download an embedding model and
check for updates, so do not assume startup is fully offline.

**If not:** stop if a port listens on anything other than `127.0.0.1`, if the
first account or login fails, if your model does not appear, or if answers come
back empty. Read the error with `docker logs --tail 50 strix-webui-local`,
remove anything private, and ask for help. Do not switch authentication off to
get past a problem, and do not attach the volume of a working installation as
an experiment.

<!-- PAID_HELP_STEP: browser-ui -->
Stuck? Get free error help in [Discussions](https://github.com/hogeheer499-commits/strix-halo-guide/discussions) or [paid setup help on strixhaloguide.com](https://strixhaloguide.com/services/#setup-rescue).

<details>
<summary>Why this exact image and these settings</summary>

The long `sha256` digest pins one exact image: the public multi-platform
**v0.11.4** registry index as observed on 2026-10-03, which includes Linux
amd64. That source review did not run the image; the separate October 15 test
ran the same digest from the local image cache. Because the digest is
fixed, the image never receives patches on its own; check for newer advisories
before you deploy it.

With persistent configuration switched off, the environment supplies the
startup configuration. Changes an admin makes in the web interface apply in memory
and are gone after a restart, so recheck login, signup and sharing after any
admin change. To keep a changed setting, recreate the container deliberately
with the same pinned image, a reviewed set of environment variables and the
existing volume, after checking your backup.

Sources read 2026-10-03: [startup host/port](https://github.com/open-webui/open-webui/blob/v0.11.4/backend/start.sh),
[configuration defaults](https://github.com/open-webui/open-webui/blob/v0.11.4/backend/open_webui/config.py),
[in-memory/nonpersistent behavior](https://github.com/open-webui/open-webui/blob/v0.11.4/backend/open_webui/models/config.py),
[first-admin signup](https://github.com/open-webui/open-webui/blob/v0.11.4/backend/open_webui/routers/auths.py),
[release](https://github.com/open-webui/open-webui/releases/tag/v0.11.4) and
[published advisories](https://github.com/open-webui/open-webui/security/advisories).

</details>

## 3. Use From Another Computer

Keep Ollama and the browser interface on loopback. Do not open their ports
for this. Instead, use an SSH tunnel from the other
computer, with an SSH account you already have on the Strix Halo machine.
Replace `user@your-box` with that account and machine:

```bash
ssh -N -L 127.0.0.1:3000:127.0.0.1:3000 user@your-box
```

On that other computer, open `http://127.0.0.1:3000` while the tunnel stays
open, and keep the WebUI login enabled. The address looks the same on both
machines, but the tunnel carries it to the Strix Halo box. **Good:** you can log
in and chat through the tunnel. Then check the other direction: from a second
device, try to reach ports 11434 and 3000 on the Strix Halo machine directly,
over every network path you use (home LAN, tailnet, IPv4 and IPv6). Those
attempts must fail. The listener check shows the actual binding in the current
network namespace at that moment. A failed direct connection establishes only
that the tested route and port were unreachable from that device at that time;
it does not establish that every other path is closed.

**If not:** stop and check your SSH setup. Never fix a tunnel problem by
exposing Ollama or the web interface to the network. Remote use counts as
working for the recorded paths only when the tunnel works and the direct
connections fail. Record which devices, paths and ports you tested and when.

<!-- PAID_HELP_STEP: remote-use -->
Stuck? Get free error help in [Discussions](https://github.com/hogeheer499-commits/strix-halo-guide/discussions) or [paid setup help on strixhaloguide.com](https://strixhaloguide.com/services/#setup-rescue).

## 4. Acceptance: When Is The Installation Working?

Use this list to say exactly what works. Record **pass / fail / not tested**
for each item that applies to you, together with the exact Ollama version,
image digest and model ID. A terminal-only result says nothing about the
browser interface.

1. The terminal shows a readable answer; the known task returns `STRIX_CHECK=391`
   with `done=true` and `done_reason=stop`. Full GPU placement is confirmed while
   the model is loaded. A timing-only result does not pass these checks.
2. If using WebUI: model discovery and visible answers work; login succeeds,
   signed-out access cannot use the model, subsequent signup is disabled and
   community sharing is off.
3. Listeners are loopback-only. For remote use, direct access from a second
   device fails while the intended SSH tunnel works, across applicable paths.
4. After a planned service/container restart, repeat response, model discovery,
   login and listener checks as applicable. A full-host reboot needs its own
   planned test. The UI requests `unless-stopped`; Docker must start at boot and
   the container must not have been deliberately stopped.
5. If image input or tool calling is part of your work, exercise it with the
   exact model and client. Plain chat does not qualify those features.
6. Verify backup/restore, update ownership and which integrations or models can
   contact cloud services. Local-only/offline operation is a separate check.

<details>
<summary>Additional acceptance for an agreed installation service</summary>

For paid installation, agree on workload, supported versions, checks, handover
and remedy before accepting an order. Installed software alone is not delivery;
every model, plugin and future update cannot be promised. This page defines the
checks, **not a report that they have all passed**.

</details>

## Existing Installations And Upgrades

Record `ollama --version`, `ollama list`, model weight-blob digests and
`ollama show <model> --parameters` before changing a working setup. Record the
runner/backend and relevant service configuration privately; a full environment
can contain secrets. Keep a recoverable copy of the model store, UI data and
configuration, and verify restore before treating it as a rollback plan.

The script retains an existing runtime and administrator drop-ins. An existing
nonlocal `OLLAMA_HOST`, environment-file override, legacy GPU rules or competing
boot settings needs deliberate review. Do not copy in a new profile to silence
a conflict. [Manual configuration](README.md#phase-5-ollama-setup-vulkan) provides the
reference. Qualification from a different version or an earlier LAN-reachable
service does not establish your new loopback-only setup.

## Ollama 0.40.7: Paused Migration And Rollback Before Qualification

**Scoped release/source review 2026-10-21.** [Ollama v0.40.7](https://github.com/ollama/ollama/releases/tag/v0.40.7)
is an available stable release, not a tested replacement for the historical
versions below. This note does not change the setup-script pin or establish a
performance or security improvement on Strix Halo.

[v0.40.3 release notes](https://github.com/ollama/ollama/releases/tag/v0.40.3)
say background model upgrade was paused for embedding and other request
performance. In the [v0.40.7 runner scheduling source](https://github.com/ollama/ollama/blob/v0.40.7/server/routes.go),
the automatic compatibility-migration call remains commented out. Do not
describe automatic first-use background upgrading as active v0.40.7 behavior.

The earlier [v0.40.2 migration note](https://github.com/ollama/ollama/releases/tag/v0.40.2)
described first-use background upgrades and retaining original copies as rollback
backups, temporarily increasing storage use; `ollama list` hides duplicate
entries. Stores already migrated on that version still need review. A model
name alone does not identify its artifact or runner, and pausing migration does
not prove old backups were restored or removed.

Before upgrading, record version, manifests/blobs, runner and configuration;
check disk space and verify a recoverable model-store/configuration backup.
Retain original model backups while testing: v0.40.2's optional cleanup removes
them, and its notes say a later downgrade to before 0.40 requires re-pulling
models. Hidden duplicate rows do not prove migration or cleanup was absent.

Qualify a separate candidate against visible text, image/tools where used,
model identity, GPU offload, access boundaries, service restart and restore.
Full-host reboot remains a separate unperformed test. Stop if storage, identity
or rollback is unclear; a newer version number alone does not qualify a route.

## Version And Security Status

Component acceptance added 2026-10-15; scoped release/advisory check added
2026-10-21 ([scope](MAINTENANCE_REVIEW_2026-10-21.md)). Earlier upstream/security observations remain dated
2026-10-14 and the UI source/digest review 2026-10-03.

| Component | What is established | What is still open |
|---|---|---|
| Ollama 0.31.2 | Historical text/vision/service/full-reboot qualification; October 14 clean VM installation and model download; October 15 isolated known-answer/GPU/browser and runtime-restart acceptance | Known advisory ranges include it; the VM boot check failed as described below. The revised fresh Strix Halo installation and recovery still need qualification |
| Existing Ollama 0.32.15 | Scoped September 19 text/image/tool/client acceptance after service restart; October 14 isolated loopback task/GPU check using an existing model cache | No new full-host reboot or fresh install; the earlier shared-service client result was LAN-reachable |
| Ollama 0.40.7 | Stable release observed 2026-10-21; release notes and scoped source read | Background model upgrade is paused; previously migrated stores need identity/rollback review. No local upgrade/client/reboot qualification or confirmed fix for CVE-2026-85180 established |
| Open WebUI 0.11.4 | October 15 pinned-image startup with new data, first admin/login, visible GPU answer, closed signup, anonymous-request rejection, loopback listeners and UI/runtime restart | Docker installation, the exact default-port/named-volume command, host reboot and restore remain open; the October 18 channel-webhook advisory includes this pin (see above) |

**October 15 hardware check: [isolated Ollama 0.31.2 + browser evidence](data/raw/2026-10-15/ollama-0312-webui-0114-isolated-acceptance/).**
The guide's checker and the pinned browser UI both returned the correct known
answer using the official model manifest `a7eb95c53bcf` and fully verified cached
blobs, with 42/42 layers on the GPU. Normal login and a new browser answer also
worked after restarting both temporary processes. This used separate ports and
new UI data on an existing host; it did not run `setup.sh`, change the BIOS,
reboot the host or qualify access from another device. It is no speed ranking
or fresh-native-installation claim.

**Maintainer check: [redacted raw evidence](data/raw/2026-10-14/ollama-03215-isolated-task-gpu-probe/).**

The October 14 task/GPU probe used an isolated existing **0.32.15** runtime and
cached `qwen3.6:35b-a3b`, manifest `096fdbd02fe6`, weight blob `d372de8e9348`,
Vulkan/RADV, context 8192 and MTP drafting. It produced visible text and an exact
`STRIX_CHECK=391` response; both requests finished with `done=true` and
`done_reason=stop`, with 42/42 layers offloaded. It performed no fresh install,
model download, service change, reboot, recovery, UI or second-device network
test. The requests used `stream=true`; the later check helper uses
`stream=false` and was not live-tested by this probe. It is not a speed
ranking or proof of the script's 0.31.2 default.

**Clean VM test, October 14: [installation and boot-check evidence](data/raw/2026-10-14/ollama-0312-clean-vm-install/).**
A clean Ubuntu 24.04 VM installed Ollama 0.31.2 and downloaded the model; both
remained available after a guest reboot. The boot check correctly failed:
extra configuration in the cloud image overrode all three required parameters.
The revised script now stops before changing such a system, verified on a
second clean VM. This is a deliberate limit: all GRUB `*.cfg` fragments need
manual review, including harmless ones. There was no GPU passthrough, so
Ollama's GPU-specific installer path was not exercised. No inference or browser
test ran; neither VM qualifies a fresh Strix Halo installation.

The revised script has offline fixture coverage, not fresh-install/upgrade
hardware qualification. Required-tool checks do not establish sufficient disk
space or make the upstream installer transactional. Consult
[security status](SECURITY.md#security-status-of-pinned-components) before any
runtime choice. Keep credentials and private documents out of reports.
