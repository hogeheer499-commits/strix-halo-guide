# AMD rocm-cli 0.1.0 Isolated Strix Halo Scout

First-party packaging and buyer-friction scout from 2026-08-09. The released
AMD `rocm-cli` 0.1.0 binary was run in an isolated user root so it could not
replace the guide's measured host stack.

## Result

- `rocm examine` detected the Ryzen AI MAX+ 395, Radeon 8060S, `/dev/kfd`, and
  the large unified-memory pool.
- `rocm model` returned Strix Halo-oriented recommendations, including Qwen3.6
  35B and Gemma 4.
- The delegated Lemonade 10.10 engine install initially failed because
  `XDG_RUNTIME_DIR` was unset. A retry with a private runtime directory
  progressed further.
- The installed backend was nested below the location expected by the
  released CLI. A local symlink/flattening workaround made the service usable.
- With that workaround, the existing 43 GiB Qwen3-Next target loaded through
  ROCm and returned a coherent API response at 83.53 prompt t/s and 27.14
  decode t/s for this single smoke request.

This is packaging evidence, not a backend speed headline. The main value is
identifying the exact friction between hardware detection, delegated runtime
installation, and a working local endpoint.

## Follow-Up

ROCm `rocm-cli` PR #177 was tested separately because it upgrades the delegated
Lemonade runtime to 11.5.1 and changes engine installation behavior. See the
adjacent [`rocm-cli-pr177-gfx1151-live`](../rocm-cli-pr177-gfx1151-live/)
package.

## Evidence Map

- `examine.*`, `model.txt`: hardware and recommendation output.
- `lemonade-install*.txt`: initial install attempts and XDG retry.
- `backend-tree-*.txt`, `packaging-workaround-created-links.txt`: packaging
  mismatch and local workaround.
- `serve-local-after-flattening.txt`, `service-log-after-flattening.txt`, and
  `response-after-flattening.json`: successful endpoint evidence.
- `host-snapshot.txt`, `source-commit.txt`, `binary-sha256.txt`: provenance.
