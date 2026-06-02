#!/usr/bin/env python3
"""
LM Studio Performance Benchmark (WSL2 Ubuntu Optimized)
Tests latency & throughput against LM Studio's local API.
GPU acceleration happens in Windows; WSL2 only measures API response times.
"""

import argparse
import csv
import subprocess
import sys
import time
import statistics
from typing import List, Dict

try:
    from openai import OpenAI
except ImportError:
    print("Error: 'openai' package is required. Install with: pip install openai")
    sys.exit(1)

def benchmark_completion(client: OpenAI, model: str, prompt: str, max_tokens: int, temperature: float) -> Dict:
    """Run a single completion and return metrics."""
    start = time.perf_counter()
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens, temperature=temperature, stream=False
    )
    latency = time.perf_counter() - start
    
    # Use API usage field (LM Studio supports this)
    if hasattr(response, 'usage') and response.usage:
        in_tok, out_tok = response.usage.prompt_tokens, response.usage.completion_tokens
    else:
        in_tok, out_tok = int(len(prompt.split()) * 1.3), max_tokens
        
    return {
        "latency_sec": latency,
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "total_tokens": in_tok + out_tok,
        "tokens_per_second": (in_tok + out_tok) / latency if latency > 0 else 0
    }

def run_benchmark(base_url: str, model: str, prompts: List[str], num_runs: int, max_tokens: int, temperature: float, csv_path: str):
    client = OpenAI(base_url=base_url, api_key="lm-studio")
    all_results = []
    
    print(f"🚀 Benchmarking model: {model}")
    print(f"📍 Endpoint: {base_url} (WSL2 ↔ Windows host forwarding)")
    print(f"💡 GPU work runs in Windows. WSL2 measures API latency only.\n")
    
    for i, prompt in enumerate(prompts):
        p_name = f"prompt_{i+1}"
        print(f"▶️ Testing {p_name} ({len(prompt)} chars)...")
        
        run_data = []
        for j in range(num_runs):
            res = benchmark_completion(client, model, prompt, max_tokens, temperature)
            row = {"prompt": p_name, "run": j+1, "latency_s": round(res["latency_sec"], 4),
                   "in_tok": res["input_tokens"], "out_tok": res["output_tokens"],
                   "tps": round(res["tokens_per_second"], 2)}
            run_data.append(row)
            all_results.append(row)
            print(f"   Run {j+1}/{num_runs}: {res['latency_sec']:.3f}s | {res['tokens_per_second']:.2f} tok/s")
            
        lats = [r["latency_s"] for r in run_data]
        tps = [r["tps"] for r in run_data]
        print(f"✅ {p_name}: Avg Lat={statistics.mean(lats):.3f}s | P50={sorted(lats)[len(lats)//2]:.3f}s\n"
              f"   Avg TPS={statistics.mean(tps):.2f} | Median TPS={statistics.median(tps):.2f}\n")

    # Export CSV
    if all_results:
        with open(csv_path, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=all_results[0].keys())
            w.writeheader(); w.writerows(all_results)
        print(f"📊 Results saved to: {csv_path}")

    all_lats = [r["latency_s"] for r in all_results]
    all_tps = [r["tps"] for r in all_results]
    print("\n" + "="*45)
    print("📈 OVERALL SUMMARY")
    print("="*45)
    print(f"Total Runs: {len(all_results)}")
    print(f"Avg Latency: {statistics.mean(all_lats):.3f}s (P50: {sorted(all_lats)[len(all_lats)//2]:.3f}s)")
    print(f"Avg Throughput: {statistics.mean(all_tps):.2f} tok/s (Median: {statistics.median(all_tps):.2f})")
    print("="*45)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:1234/v1")
    parser.add_argument("--model", required=True)
    parser.add_argument("--num-runs", type=int, default=10)
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--prompts", nargs="+")
    parser.add_argument("--csv", default="lm_studio_bench_wsl.csv")
    args = parser.parse_args()
    
    prompts = args.prompts if args.prompts else [
        "Hi there.",
        "Write a concise explanation of quantum entanglement suitable for a high school student. Include one real-world analogy.",
        "Derive the time-independent Schrödinger equation from first principles, explain each term physically, discuss boundary conditions in 1D infinite well, and summarize quantization."
    ]
    
    run_benchmark(args.base_url, args.model, prompts, args.num_runs, args.max_tokens, args.temperature, args.csv)
