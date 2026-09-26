#!/usr/bin/env python3
"""Check the smoke outputs in this bundle.

arith: the final answer (after the reasoning block) must be exactly 391.
code:  the final answer's is_prime(n) is executed and compared with a reference
       for n in -10..500. Run from this directory: python3 check-smoke.py
"""
import glob
import re


def final_answer(text: str) -> str:
    text = text.replace("[end of text]", "")
    for marker in ("</think>", "to=user<|message|>"):
        if marker in text:
            text = text.rsplit(marker, 1)[1]
    return text.strip()


def ref_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, int(n**0.5) + 1))


for path in sorted(glob.glob("*-smoke-*.out.txt")):
    answer = final_answer(open(path, encoding="utf-8").read())
    if "-smoke-arith-" in path:
        verdict = "PASS" if answer == "391" else f"FAIL (final answer {answer[:40]!r})"
    else:
        code = re.sub(r"^```(?:python)?\s*|\s*```$", "", answer)
        scope: dict = {}
        try:
            exec(code, scope)  # noqa: S102 - local check of model output
            bad = [n for n in range(-10, 501) if scope["is_prime"](n) != ref_prime(n)]
            verdict = "PASS" if not bad else f"FAIL (wrong for {bad[:5]})"
        except Exception as exc:  # truncated or non-code answer
            verdict = f"NO FINAL CODE ({type(exc).__name__})"
    print(f"{path}: {verdict}")
