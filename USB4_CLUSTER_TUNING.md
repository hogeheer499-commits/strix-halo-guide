# USB4 Cluster Tuning

These are community-reported notes from [Fail-Safe](https://github.com/Fail-Safe) in [issue #13](https://github.com/hogeheer499-commits/strix-halo-guide/issues/13), building on the multi-node RPC data in [issue #12](https://github.com/hogeheer499-commits/strix-halo-guide/issues/12).

This is advanced Strix Halo cluster material. It is not needed for a normal one-machine local AI setup.

Structured data:

- [`data/community_usb4_latency.csv`](data/community_usb4_latency.csv)
- [`data/community_usb4_idle_power.csv`](data/community_usb4_idle_power.csv)
- related RPC results: [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md)

## Practical Recommendation

For a Strix Halo USB4 RPC cluster, the only default recommendation from this report is:

```bash
for f in /sys/devices/system/cpu/cpu*/power/pm_qos_resume_latency_us; do
  echo 100 | sudo tee "$f" > /dev/null
done
```

Run it on every box that participates in the USB4 link.

Use MTU 9000 for the `thunderbolt-net` link unless you have a reason to retest. In this community RPC cell, MTU 9000 beat both MTU 1500 and MTU 65520.

To revert:

```bash
for f in /sys/devices/system/cpu/cpu*/power/pm_qos_resume_latency_us; do
  echo 0 | sudo tee "$f" > /dev/null
done
```

This is not persistent across reboot. Use a small systemd unit if you want it applied automatically for cluster nodes.

## Why This Matters

The `llama.cpp` RPC path in [`COMMUNITY_RPC.md`](COMMUNITY_RPC.md) showed that multi-box Strix Halo is useful for capacity, not automatic speed. USB4 link latency is part of that cost.

Fail-Safe tested the same Qwen3-Coder 30B Vulkan/RADV 2-node RPC cell from issue #12:

- ai-2 leader plus ai-3 follower
- USB4 `thunderbolt-net` mesh
- MTU 9000
- Qwen3-Coder-30B-A3B UD-Q4_K_XL
- `llama-bench -fa 1 -ngl 999 -mmp 0 -p 512 -n 128 -r 20`

The recommended `pm_qos` step reduced ping RTT from about 600-700 us to about 134 us and improved tg128 by about 2%.

Follow-up idle-power testing corrected the initial worst-case estimate. On two toggled Corsair nodes, `pm_qos_resume_latency_us=100` raised idle power by about 1.4-1.6 W per box, not 5-15 W.

## MTU Check

The raw follow-up rows also tested MTU size on the same 2-node Vulkan/RADV RPC cell.

| MTU | Vulkan 2-node tg128 | Interpretation |
|-----|---------------------|----------------|
| 1500 | 73.89 t/s | slower than jumbo frames |
| 9000 | 75.27 t/s | best stock setting in this report |
| 65520 | 74.65 t/s | did not beat MTU 9000 |

Practical read: use MTU 9000 for this `thunderbolt-net` RPC path before spending time on larger jumbo settings.

## Measured Tuning Ladder

| Configuration | Ping RTT avg | Vulkan 2-node tg128 | Change vs stock | Per-rep stddev | Recommendation |
|---------------|--------------|---------------------|-----------------|----------------|----------------|
| Stock defaults | about 600-700 us | 75.27 t/s | baseline | 0.27-0.79 | baseline only |
| `pm_qos_resume_latency_us=100` | 134 us | 76.79 t/s | +2.0% | 0.13-0.17 | recommended for active cluster nodes |
| patched thunderbolt `throttle=64` | 103 us | 77.54 t/s | +3.0% | 0.06-0.11 | experimental |
| patched thunderbolt `throttle=0` | 103 us | 77.56 t/s | +3.0% | 0.06-0.08 | experimental; not worth defaulting |

Interpretation:

- `pm_qos_resume_latency_us=100` gives most of the measured gain and is easy to apply/revert.
- The patched thunderbolt module adds another roughly 1% in this specific RPC cell, but requires kernel-module work.
- `throttle=0` and `throttle=64` were effectively tied on this Strix Halo setup.
- The lower stddev is also useful for benchmark repeatability, not only throughput.

## Tradeoff

`pm_qos_resume_latency_us=100` keeps CPUs out of deeper sleep states, but the measured Strix Halo idle-power cost was small in this report.

| Box | Role | Baseline idle | `pm_qos=100` idle | Reverted idle | Delta |
|-----|------|---------------|-------------------|---------------|-------|
| ai-1 | untouched control | 33.94 W | 34.03 W | 34.30 W | -0.09 W |
| ai-2 | toggled | 29.29 W | 30.50 W | 28.50 W | +1.60 W |
| ai-3 | toggled | 33.04 W | 34.10 W | 32.43 W | +1.36 W |

The control box staying flat makes the roughly 1.5 W rise on the toggled boxes credible. For a three-box cluster, that is about 4-5 W total idle increase, which is a much more comfortable tradeoff than the original worst-case estimate. Still, measure your own system if idle power matters.

Structured rows: [`data/community_usb4_idle_power.csv`](data/community_usb4_idle_power.csv).

## Experimental Thunderbolt Patch

Fail-Safe also tested `yann`'s out-of-tree thunderbolt patch from the Level1Techs thread. It exposes the hard-coded interrupt throttle in `drivers/thunderbolt/nhi.c` as a module parameter.

The reported workflow was:

```bash
mkdir tb-build && cd tb-build
git init -q && git remote add origin https://github.com/torvalds/linux.git
git config core.sparseCheckout true
echo "drivers/thunderbolt/*" > .git/info/sparse-checkout
git fetch --depth=1 origin tag v7.0-rc6
git checkout FETCH_HEAD

# apply yann's patch from the Level1Techs thread, then build out-of-tree
make -C /lib/modules/$(uname -r)/build M=$(pwd) modules

sudo modprobe -r thunderbolt_net thunderbolt
sudo insmod ./thunderbolt.ko throttle=64
sudo modprobe thunderbolt_net
```

Do not treat this as the default guide path:

- both ends of the USB4 link need the patched module
- repeated module reloads can leave a USB4 host router/interface in a bad state until another reload cycle
- `throttle=0` has been reported to risk CPU saturation during bandwidth-heavy tests on other hardware
- local gains over `pm_qos` were small in this specific Strix Halo RPC benchmark

## Forward Pointer

The same Level1Techs thread also discusses `mgeppert`'s zero-copy DMA work, which bypasses the IP stack and reports much higher USB4 throughput and much lower latency than `thunderbolt-net`.

That is a kernel-driver/research path, not a copy-paste setup step. It is relevant if someone is trying to find the actual Strix Halo USB4 ceiling, but it is out of scope for the beginner guide.

## Sources

- Fail-Safe issue: [#13](https://github.com/hogeheer499-commits/strix-halo-guide/issues/13)
- Related RPC matrix: [#12](https://github.com/hogeheer499-commits/strix-halo-guide/issues/12)
- Level1Techs USB4 thread: <https://forum.level1techs.com/t/benchmarking-usb4-performance-on-strix-halo/245299>
