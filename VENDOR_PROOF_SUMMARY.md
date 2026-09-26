# Vendor and reviewer proof summary

**Scope: September 19, 2026 functional campaign, plus attributed historical evidence.**

## Buyer questions now answered more precisely

- **Which function works through which route?** Existing Ollama 0.32.15 on
  Beelink passed Qwen3.6 text, Qwen2.5-VL image recognition, a genuinely
  executed Devstral tool round-trip and pinned Open WebUI discovery/response
  after service restart. Different models are not conflated into one quality claim.
- **Can a newer release replace the known route?** Isolated Ollama 0.34.2
  passed available-model controls but was not promoted without official
  Qwen3.8, normal upgrade/client and reboot acceptance.
- **Is a successful load enough?** No. Historical HIP b10687 returned HTTP 200
  but failed exact retrieval and concurrent outputs; released v0.4.1 passed
  the tested Coder controls. Both passed the Gemma image fixture. The
  [qualification summary](RUNTIME_QUALIFICATION_2026-09-19.md) preserves these
  boundaries rather than declaring HIP universally fixed.
- **What does the price buy?** The [new snapshot](BUYER_SNAPSHOT_2026-09-19.md)
  separates 64GB from 128GB, SSD variants, mainboards from complete PCs,
  selected stock/ETA and unresolved checkout costs. No unmatched value ranking.
- **Is the route local-only?** Local inference was observed, but the existing
  Ollama listener was reachable from another LAN host. A loopback browser UI
  does not prove that its backend is inaccessible remotely.

These resolve documentation and qualification uncertainties; they are not
measured reductions in support tickets, conversion uplift, revenue or setup time.

## Main remaining limitation

The deepest first-party evidence is still one Beelink retail machine, not a
matched current-OEM fleet. GMKtec EVO-X2 evidence is community/external and
includes different memory configurations and runtime routes. There is no
first-party exact-SKU GMKtec retail setup/reboot campaign; EVO-X3 does not
inherit EVO-X2 qualification. The [coverage matrix](SYSTEM_EVIDENCE_MATRIX.md)
is 10 described owner systems plus 3 external sources, not 13 matched repeats.

Per-OEM evidence class (as of the 2026-09-19 evidence review; classes from
the README [buying-guide table](README.md#buying-guide)): Beelink GTR9 Pro
first-party (plus two community owner systems); GMKtec EVO-X2 community and
external-reference, no first-party exact-SKU test; Corsair AI Workstation 300
community (three-system fleet); Nimo AI Mini PC community; Minisforum MS-S1
MAX community (Windows LM Studio); Minix Elite ER939 community (Ollama
beginner path); Framework Desktop external-reference rows only; Bosgame, HP
and ASUS none (price snapshots or a warning only); GMKtec EVO-X3 none.

## Most informative next hardware experiment

Apply the [retail buyer-path protocol](BUYER_PATH_VALIDATION.md) to one stock,
exactly identified GMKtec EVO-X2 128GB retail configuration: firmware/factory
state, setup time/interventions, the same named text/image/tool/client tests,
service restart and reboot. Preserve failures and compare the same artifacts
with Beelink before making any OEM effect claim. No acquisition, outreach,
sponsorship or completed test is implied here.

There are no affiliate links as of 2026-09-19. Paid work, hardware support and factual
vendor review follow [the editorial firewall](VENDOR_DISCLOSURE.md); they
cannot buy ranking, positive conclusions or removal of negative results.
