#!/bin/bash
set -euo pipefail
MODEL="${1:-qwen3.6:35b-a3b}"
PROMPT="${2:-hello how are you}"
echo "Model: $MODEL | $(date -u +%Y-%m-%dT%H:%M:%SZ)"
if command -v ollama >/dev/null 2>&1; then
    echo "Local tag and manifest ID (ollama list):"
    ollama list 2>/dev/null | awk -v m="$MODEL" 'NR==1 || $1==m || $1==m":latest"' || true
    echo "Model parameters (a draft_num_predict above 0 means Ollama-default speculative drafting):"
    ollama show --parameters "$MODEL" 2>/dev/null || echo "  (ollama show --parameters unavailable)"
fi
python3 -c 'import json,sys; print(json.dumps({"model":sys.argv[1],"prompt":sys.argv[2],"stream":False,"options":{"num_predict":128}}))' "$MODEL" "$PROMPT" |
curl --fail --silent --show-error --connect-timeout 5 --max-time 600 http://localhost:11434/api/generate -H 'Content-Type: application/json' --data-binary @- | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('done') is not True or not isinstance(d.get('response'),str) or not d['response'].strip() or d.get('error'):
    raise ValueError('Missing completed visible response or server error')
for key in ('prompt_eval_count','prompt_eval_duration','eval_count','eval_duration','total_duration'):
    if type(d.get(key)) is not int or d[key] <= 0:
        raise ValueError('Invalid counter: ' + key)
pp=d['prompt_eval_count']/d['prompt_eval_duration']*1e9
tg=d['eval_count']/d['eval_duration']*1e9
print(f'Prompt eval: {pp:.1f} t/s ({d[\"prompt_eval_count\"]} tokens)')
print(f'Generation:  {tg:.1f} t/s ({d[\"eval_count\"]} tokens)')
print(f'Total time:  {d[\"total_duration\"]/1e9:.2f}s')
"
