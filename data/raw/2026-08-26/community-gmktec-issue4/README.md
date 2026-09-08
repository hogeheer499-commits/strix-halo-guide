# GMKtec EVO-X2 four-model follow-up — issue #4

Contributor: [mottledMantis](https://github.com/mottledMantis). Measured/submitted 2026-08-26; imported 2026-09-08.

- [System, command, hashes and compatibility report](https://github.com/hogeheer499-commits/strix-halo-guide/issues/4#issuecomment-5427451071), preserved in [report.md](report.md).
- [Contributor-cleaned CSV comment](https://github.com/hogeheer499-commits/strix-halo-guide/issues/4#issuecomment-5427454362), preserved in [submitted-csv-comment.md](submitted-csv-comment.md).
- Four CSV code blocks extracted without changing their fields: [Gemma](gemma4-26b-udq4km.csv), [Coder Q4_K_S](qwen3-coder-q4ks.csv), [Coder UD-Q4_K_XL](qwen3-coder-udq4kxl.csv), [Qwen3.6 IQ4_XS](qwen36-iq4xs-q8nextn.csv). Each has 40 columns and two rows: pp512 and tg128. These are submitted aggregate results, not individual-repeat logs.

## Scope and interpretation

This is the existing contributor's 96GB GMKtec EVO-X2, not an additional system or contributor. Ubuntu 26.04, kernel 7.0.0-30-generic, RADV, UMA 1GB and IOMMU disabled are reported. The August 26 Mesa version is not supplied; do not inherit August 18's version. An idle host and 20 repeats are contributor-reported; the CSV does not independently establish the repeat count or background state. No power/thermal telemetry accompanies this run.

The contributor labels the runtime `llama.cpp v0.3.0`, commit `c1d0e7a`; CSV `build_number` is `1`. Preserve both identifiers. The source repository/full commit and release provenance have not been independently verified, so this is not labelled an official or currently recommended upstream release.

The report supplies four syntactically valid SHA256 values. The model files were not downloaded or rehashed here. CSV `load_mode=none` is preserved alongside the reported `-mmp 0` command. All four measurements are direct non-speculative `llama-bench` pp512/tg128, including the MTP-capable IQ4_XS-Q8nextn file.

The separate approximately 76 t/s MTP server observation and Q6_K_XL target + Q4_K_XL draft failure are narrative-only reports. No server command, acceptance/output checks or complete failure log accompanies them. The contributor reports that b9235 loads the same Q6/draft combination. This supports an exact-stack compatibility warning and a follow-up investigation, not a universal downgrade recommendation or a proven root cause.

## Comparison limits

Gemma decode at 54.154367 t/s is about 2.34% below Beelink b9851 (55.451497) and 0.05% below b9859 (54.183921). Thus the submitted "within ~1–2%" shorthand is not exact for both controls. The Beelink controls use batch 2048 and five repeats, versus reported batch 512 and 20 repeats here. Their 16,852,417,656-byte Gemma artifact is 79,298,560 bytes smaller than the submitted 16,931,716,216-byte artifact. Matching the artifact name and flash-attention/mmap policy does not establish matching model bytes or a controlled OEM comparison.

Against the contributor's August 18 Gemma run, prefill changes from 1209.075618 to 1181.976054 t/s and decode from 53.018213 to 54.154367 t/s. Build, batch and mmap policy changed together; do not attribute the difference to any one setting.

## Useful remaining evidence

- Full runtime source URL/commit, Mesa version and per-repeat logs.
- A Beelink control with identical model hashes, build, flags and repeat policy.
- Complete server commands/logs for Q6/draft failure and IQ4_XS success, including draft acceptance and output validity. The direct 76.20 t/s row cannot substitute for that server evidence.
