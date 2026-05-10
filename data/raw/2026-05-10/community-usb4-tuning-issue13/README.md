# Community USB4 Tuning Issue #13 Raw Artifacts

Source: https://github.com/hogeheer499-commits/strix-halo-guide/issues/13#issuecomment-4414140002

Contributor: Fail-Safe.

This directory stores the raw `llama-bench -o csv` rows for the USB4 tuning follow-up, plus the experimental thunderbolt throttle patch and Makefile shared in the issue. Structured summaries are in `data/community_usb4_latency.csv` and `data/community_usb4_idle_power.csv`; interpretation is in `USB4_CLUSTER_TUNING.md`.

The thunderbolt patch is experimental. The guide recommends the reversible `pm_qos_resume_latency_us=100` step first, not an out-of-tree kernel module.
