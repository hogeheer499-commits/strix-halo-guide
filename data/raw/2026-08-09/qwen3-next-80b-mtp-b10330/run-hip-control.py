#!/usr/bin/env python3
"""Run the same Qwen3-Next MTP matrix on the official b10330 HIP build."""

import importlib.util
import pathlib


ROOT = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("qwen_mtp_repro", ROOT / "run-repro.py")
REPRO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REPRO)
REPRO.ROOT = ROOT / "hip-control"

REPRO.SERVER = pathlib.Path(
    "/home/hoge-heer/local-scratch/llama.cpp-b10330/build-hip/bin/llama-server"
)
REPRO.PORT = 18104
REPRO.BASE_URL = f"http://127.0.0.1:{REPRO.PORT}"
REPRO.PROFILES = (
    {"name": "hip-baseline", "mtp": False},
    {"name": "hip-mtp-n4-p000", "mtp": True, "n_max": 4, "p_min": 0.00},
)


def hip_server_command(profile):
    command = [
        str(REPRO.SERVER),
        "-m", str(REPRO.MODEL),
        "--alias", profile["name"],
        "--host", "127.0.0.1",
        "--port", str(REPRO.PORT),
        "--no-ui",
        "--metrics",
        "--no-cache-prompt",
        "--parallel", "1",
        "-c", "8192",
        "-b", "2048",
        "-ub", "512",
        "-dev", "ROCm0",
        "-ngl", "999",
    ]
    if profile["mtp"]:
        command.extend(
            [
                "--spec-draft-model", str(REPRO.DRAFT),
                "--spec-draft-device", "ROCm0",
                "--spec-draft-ngl", "999",
                "--spec-type", "draft-mtp",
                "--spec-draft-n-max", str(profile["n_max"]),
                "--spec-draft-p-min", str(profile["p_min"]),
            ]
        )
    return command


REPRO.server_command = hip_server_command


if __name__ == "__main__":
    REPRO.main()
