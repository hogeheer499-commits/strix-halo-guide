---
library_name: transformers
license: apache-2.0
license_link: https://huggingface.co/Qwen/Qwen-AgentWorld-35B-A3B/blob/main/LICENSE
pipeline_tag: text-generation
base_model:
- Qwen/Qwen3.5-35B-A3B-Base
datasets:
- Qwen/AgentWorldBench
tags:
- qwen
- world-model
- agent
- environment-simulation
---

# Qwen-AgentWorld-35B-A3B

<div style="text-align: center">
  <img width="400px" src="https://qianwen-res.oss-accelerate-overseas.aliyuncs.com/Qwen-AgentWorld/logo.png">
  <p>
    <a href="http://arxiv.org/abs/2606.24597">📑 Technical Report</a> |
    <a href="https://qwen.ai/blog?id=qwen-agentworld">📖 Blog</a> |
    <a href="https://huggingface.co/collections/Qwen/qwen-agentworld">🤗 Hugging Face</a> |
    <a href="https://modelscope.cn/collections/Qwen/Qwen-AgentWorld">🤖 ModelScope</a> |
    <a href="https://github.com/QwenLM/Qwen-AgentWorld">💻 GitHub</a> |
    <a href="https://qwen.ai/blog?id=qwen-agentworld#interactive-demo-interactive-demo">🖥️ Demo</a>
  </p>
</div>

> [!Note]
> This repository contains the model weights and configuration files for **Qwen-AgentWorld-35B-A3B**, a native language world model trained for agentic environment simulation.
>
> These artifacts are compatible with Hugging Face Transformers, vLLM, SGLang, etc.

**Qwen-AgentWorld** is the first language world model to cover seven agent interaction domains within a single model. It simulates agentic environments via long chain-of-thought reasoning, predicting the next environment state given an agent's action and interaction history. Trained through a three-stage pipeline — CPT injects environment knowledge, SFT activates next-state-prediction reasoning, RL sharpens simulation fidelity — Qwen-AgentWorld is a **native world model**: environment modeling is the training objective from the CPT stage onward, not a post-hoc add-on.


## Highlights

- **Seven Unified Domains.** A single model covers MCP (tool calling), Search, Terminal, SWE (software engineering), Android, Web, and OS — spanning both text and GUI interaction environments.
- **Native World Model.** Environment modeling from CPT onward, not post-hoc adaptation on a general-purpose LLM.
- **Generalizable, Scalable & Controllable Simulator.** Zero-shot generalization to OOD environments (e.g., OpenClaw); controllable perturbations and fictional-world construction surpass real-environment training.
- **Agent Foundation Model.** LWM RL warm-up on single-turn, non-agentic trajectories transfers to multi-turn, tool-calling agentic tasks across 7 benchmarks, including 3 entirely out-of-domain.


## Model Overview

- Type: Causal Language Model (Language World Model)
- Base Model: [Qwen3.5-35B-A3B-Base](https://huggingface.co/Qwen/Qwen3.5-35B-A3B-Base)
- Training Stage: Continual Pre-Training (CPT) → Supervised Fine-Tuning (SFT) → Reinforcement Learning (RL, GSPO)
- Number of Parameters: 35B in total and 3B activated
- Hidden Dimension: 2048
- Token Embedding: 248320 (Padded)
- Number of Layers: 40
- Hidden Layout: 10 × (3 × (Gated DeltaNet → MoE) → 1 × (Gated Attention → MoE))
- Gated DeltaNet:
    - Number of Linear Attention Heads: 32 for V and 16 for QK
    - Head Dimension: 128
- Gated Attention:
    - Number of Attention Heads: 16 for Q and 2 for KV
    - Head Dimension: 256
    - Rotary Position Embedding Dimension: 64
- Mixture Of Experts
    - Number of Experts: 256
    - Number of Activated Experts: 8 Routed + 1 Shared
    - Expert Intermediate Dimension: 512
- Context Length: 262,144 tokens
- Disclaimer: No outputs from external API services are included in the training pipeline.

## Performance

### AgentWorldBench (Open-Ended Evaluation)

Five-dimensional rubric mean per domain, normalized to 0-100 scale.

| Model | MCP | Search | Term. | SWE | Android | Web | OS | **Overall** |
|:------|:---:|:------:|:-----:|:---:|:-------:|:---:|:--:|:-----------:|
| GPT-5.4 | **70.10** | 37.26 | 53.69 | 66.29 | 60.00 | 51.80 | 68.58 | 58.25 |
| Claude Opus 4.8 | 54.93 | 35.14 | **59.18** | 64.10 | 61.50 | **54.66** | 66.62 | 56.59 |
| Claude Opus 4.6 | 69.90 | 29.30 | 57.51 | 64.55 | **61.74** | 51.42 | **70.20** | 57.80 |
| Gemini 3.1 Pro | 59.07 | 30.21 | 52.47 | 59.07 | 61.40 | 52.83 | 66.92 | 54.57 |
| Claude Sonnet 4.6 | 70.00 | 28.79 | 56.98 | 64.52 | 58.03 | 50.78 | 63.17 | 56.04 |
| DeepSeek-V4-Pro | 63.27 | 27.61 | 51.26 | 59.44 | 55.17 | 50.32 | 63.70 | 52.97 |
| GLM-5.1 | 67.60 | 22.46 | 47.32 | 52.07 | 59.10 | 51.50 | 59.13 | 51.31 |
| Kimi K2.6 | 65.23 | 27.48 | 52.54 | 58.77 | 58.93 | 50.20 | 60.80 | 53.42 |
| MiniMax-M2.7 | 55.82 | 27.30 | 41.62 | 37.44 | 52.40 | 50.52 | 57.73 | 46.12 |
| Qwen3.5-35B-A3B | 57.87 | 25.98 | 46.13 | 47.58 | 53.18 | 47.10 | 56.27 | 47.73 |
| Qwen3.5-397B-A17B | 68.31 | 30.81 | 55.30 | 64.44 | 54.90 | 48.55 | 60.85 | 54.74 |
| Qwen3.6-Plus | 55.28 | 21.94 | 50.58 | 59.08 | 57.65 | 50.78 | 60.33 | 50.81 |
| **Qwen-AgentWorld-35B-A3B** | 64.79 | 36.69 | 53.96 | 65.63 | 58.17 | 49.55 | 65.92 | 56.39 |
| **Qwen-AgentWorld-397B-A17B** | 68.24 | **37.82** | 57.73 | **68.49** | 60.20 | 50.98 | 67.89 | **58.71** |

## Quickstart

### Deployment

Qwen-AgentWorld-35B-A3B can be served via APIs with popular inference frameworks. In the following, we show example commands to launch OpenAI-compatible API servers.

> [!Important]
> The model has a default context length of 262,144 tokens.
> If you encounter out-of-memory (OOM) errors, consider reducing the context window.
> However, because Qwen-AgentWorld leverages extended context for multi-turn environment simulation, we advise maintaining a context length of at least 128K tokens.

#### SGLang

[SGLang](https://github.com/sgl-project/sglang) is a fast serving framework for large language models.

```bash
python -m sglang.launch_server \
    --model-path Qwen/Qwen-AgentWorld-35B-A3B \
    --port 8000 \
    --tp-size 4 \
    --context-length 262144 \
    --reasoning-parser qwen3
```

An OpenAI-compatible API will be available at `http://localhost:8000/v1`.

#### vLLM

[vLLM](https://github.com/vllm-project/vllm) is a high-throughput and memory-efficient inference engine for LLMs.

```bash
vllm serve Qwen/Qwen-AgentWorld-35B-A3B \
    --port 8000 \
    --tensor-parallel-size 4 \
    --max-model-len 262144 \
    --reasoning-parser qwen3 \
    --language-model-only \ 
    --trust-remote-code
```

> The `--language-model-only` flag is required because the model architecture includes visual component definitions but the checkpoint only contains language model weights. Without this flag, vLLM will attempt to initialize visual modules and fail.

An OpenAI-compatible API will be available at `http://localhost:8000/v1`.


### Inference with Transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen-AgentWorld-35B-A3B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto",
)

messages = [
    {
        "role": "system",
        "content": "You are a language world model simulating a Linux terminal environment. "
                   "Given the user's command, predict the terminal output."
    },
    {
        "role": "user",
        "content": "Action: execute_bash\nCommand: ls -la /home/user/project/"
    }
]

text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer([text], return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=2048, temperature=0.6)
response = tokenizer.decode(outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
print(response)
```

### Using via the Chat Completions API

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY",
)

# Terminal domain example
messages = [
    {
        "role": "system",
        "content": "You are a language world model simulating a Linux terminal environment. "
                   "Given the user's command, predict the terminal output."
    },
    {
        "role": "user",
        "content": "Action: execute_bash\nCommand: ls -la /home/user/project/"
    }
]

response = client.chat.completions.create(
    model="Qwen/Qwen-AgentWorld-35B-A3B",
    messages=messages,
    max_tokens=32768,
    temperature=0.6,
)
print(response.choices[0].message.content)
```

> [!Note]
> We provide **domain-specific world model system prompt templates** in [`prompts/`](https://github.com/QwenLM/Qwen-AgentWorld/tree/master/prompts) of the GitHub repository for all 7 domains. These serve as general-purpose system prompts when using Qwen-AgentWorld as an environment simulator. Each domain folder contains a `system_prompt.txt` (world model system prompt) and a `judge_system_prompt.txt` (evaluation prompt).


## Evaluate on AgentWorldBench

AgentWorldBench evaluates language world models by scoring each predicted environment observation on 5 dimensions: **Format**, **Factuality**, **Consistency**, **Realism**, and **Quality**.

### Setup

```bash
# Clone the evaluation repository
git clone https://github.com/QwenLM/Qwen-AgentWorld.git
cd Qwen-AgentWorld

# Download the benchmark
huggingface-cli download Qwen/AgentWorldBench --repo-type dataset --local-dir ./AgentWorldBench

# Install dependencies
pip install openai
```

### Run Evaluation

The evaluation follows a three-step pipeline:

```bash
cd eval

# Step 1: Run world model inference
python eval.py infer \
    --data-dir ../AgentWorldBench \
    --model-base-url http://localhost:8000/v1 \
    --model-name Qwen/Qwen-AgentWorld-35B-A3B \
    --output-dir ./results

# Step 2: Run LLM judge scoring
export OPENAI_API_KEY="your-api-key"
python eval.py judge \
    --predictions ./results/predictions.jsonl \
    --judge-base-url https://api.openai.com/v1 \
    --judge-model gpt-5.2-2025-12-11 \
    --output-dir ./results

# Step 3: Aggregate and display scores
python eval.py score --predictions ./results/judged.jsonl
```


## Best Practices

1. **Sampling Parameters**: We recommend `temperature=0.6`, `top_p=0.95`, `top_k=20` for world model inference. The model uses thinking mode by default (`<think>...</think>`) to reason about environment state transitions before producing the predicted observation.

2. **Adequate Output Length**: We recommend an output length of 32,768 tokens for most queries. For long, multi-step trajectories, you may increase the max output length to accommodate detailed environment observations.

3. **Domain-Specific System Prompts**: For optimal simulation fidelity, use the domain-specific system prompts provided in the [`prompts/`](https://github.com/QwenLM/Qwen-AgentWorld/tree/master/prompts) directory of the GitHub repository.


## Citation

If you find our work helpful, feel free to give us a cite.

```bibtex
@article{zuo2026qwen,
  title={Qwen-agentworld: language world models for general agents},
  author={Zuo, Yuxin and Xiao, Zikai and Sheng, Li and Huang, Fei and Tu, Jianhong and Liu, Yuxuan and Tang, Tianyi and Hu, Xiaomeng and Su, Yang and Lan, Qingfeng and others},
  journal={arXiv preprint arXiv:2606.24597},
  year={2026}
}
```
