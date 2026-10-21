# Existing-runtime GPU task probe — October 14, 2026

Local, redacted evidence bundle prepared from an existing capture. No model, API,
GPU or installation operation was run while preparing this bundle.

The recorded probe used **Ollama 0.32.15** and the existing cached
`qwen3.6:35b-a3b` model, on the isolated loopback endpoint
`127.0.0.1:11436`. It completed two short native `/api/chat` streaming tasks.
Both recorded responses ended with `done=true`, `done_reason=stop`, and no
thinking content. The second returned exactly `STRIX_CHECK=391` for 17 × 23.
The first response is generated text, without a separate factuality review.

The retained runner lines report Vulkan0, **AMD Radeon 8060S Graphics
(RADV STRIX_HALO)**, **42/42 layers offloaded to GPU**, context **8192**,
one slot, and `draft-mtp` with `n_max=2`. This describes this runtime/model
capture; the 42/42 count is the runner's reported offload count.
The recorded model allocation is 22,045,985,340 bytes. On shared system memory
this is not a measurement of a separate physical VRAM chip.

The model manifest SHA-256 is
`096fdbd02fe620fc10cbeb6537e080f8041aece851e5d696aed024d4f70f2e47`.
The main weight blob digest is
`sha256:d372de8e934898a59e6ccfabc3368474711384d8f1fd4d22d87a3f0a45400cdc`
(recorded size 21,718,480,960 bytes). Digest names and captured byte counts
are retained; this packaging step did not rehash the model weights.

## Evidence

- [configuration.json](configuration.json): whitelisted runtime settings, bounds,
  manifest and blob identities/sizes.
- [startup.json](startup.json): captured version and model metadata; the listener
  record is reduced to the isolated probe address.
- [request-1.json](request-1.json) and [request-2.json](request-2.json): exact
  recorded request bodies, copied byte-for-byte from the original captures.
- [result-1.json](result-1.json) and [result-2.json](result-2.json): byte-identical
  stored response aggregates and their terminal chunks. Individual intermediate
  stream chunks were not retained in these source files.
- [summary.json](summary.json): whitelisted recorded result and scope.
- [server.log](server.log): exact selected device, offload, context and MTP lines.
- [provenance.json](provenance.json): original source-file SHA-256 values,
  excerpt line numbers and transformations.
- [SHA256SUMS](SHA256SUMS): checksums of the files in this redacted bundle.

The recorded requests both set `think=false`, `stream=true`,
`keep_alive="30s"`, context 8192, temperature 0 and seed 42. Request 1 allows
192 output tokens; request 2 allows 96. The later Python check helper uses
`stream=false`. Its matching arithmetic prompt and options do not make this
capture a live test of that helper.

## Scope

This is evidence of two tasks on an existing runtime and cached model. It does
not validate a fresh install, Ollama 0.31.2, the later Python check script,
reboot/recovery, browser UI, or broad answer quality. Recorded timing/counter
fields are preserved as response evidence; this bundle makes no performance,
cold-cache, speed ranking or repeatability claim. No setup page or other guide
file was changed while packaging the evidence.

## Redaction

Only explicitly selected technical JSON fields and log lines are included.
Private paths, account/machine identifiers, process data and unrelated runtime
state are omitted. No private directory tree was opened or copied. Original
source files remain unchanged; their digests identify the capture, while
`SHA256SUMS` identifies this redacted derivative.
