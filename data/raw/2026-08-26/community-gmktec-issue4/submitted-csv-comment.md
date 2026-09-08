## Raw llama-bench CSV output (cleaned, `-o csv` format)

### Gemma 4 26B-A4B UD-Q4_K_M

```csv
build_commit,build_number,cpu_info,gpu_info,backends,model_filename,model_type,model_size,model_n_params,n_batch,n_ubatch,n_threads,cpu_mask,cpu_strict,poll,type_k,type_v,n_gpu_layers,n_cpu_moe,split_mode,main_gpu,no_kv_offload,flash_attn,devices,tensor_split,tensor_buft_overrides,load_mode,embeddings,no_op_offload,no_host,fit_target,fit_min_ctx,n_prompt,n_gen,n_depth,test_time,avg_ns,stddev_ns,avg_ts,stddev_ts
"c1d0e7a","1","AMD RYZEN AI MAX+ 395 w/ Radeon 8060S","Radeon 8060S Graphics (RADV STRIX_HALO)","Vulkan","/home/james-matheson/models/gemma-4-26b/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf","gemma4 26B.A4B Q4_K - Medium","16931716216","25233142046","512","512","16","0x0","0","50","f16","f16","999","0","layer","0","0","1","auto","0.00","none","none","0","0","0","0","0","512","0","0","2026-08-26T06:31:51Z","433193976","3085697","1181.976054","8.497062"
"c1d0e7a","1","AMD RYZEN AI MAX+ 395 w/ Radeon 8060S","Radeon 8060S Graphics (RADV STRIX_HALO)","Vulkan","/home/james-matheson/models/gemma-4-26b/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf","gemma4 26B.A4B Q4_K - Medium","16931716216","25233142046","512","512","16","0x0","0","50","f16","f16","999","0","layer","0","0","1","auto","0.00","none","none","0","0","0","0","0","0","128","0","2026-08-26T06:32:00Z","2363621001","4273263","54.154367","0.098134"
```

### Qwen3-Coder 30B-A3B Q4_K_S

```csv
build_commit,build_number,cpu_info,gpu_info,backends,model_filename,model_type,model_size,model_n_params,n_batch,n_ubatch,n_threads,cpu_mask,cpu_strict,poll,type_k,type_v,n_gpu_layers,n_cpu_moe,split_mode,main_gpu,no_kv_offload,flash_attn,devices,tensor_split,tensor_buft_overrides,load_mode,embeddings,no_op_offload,no_host,fit_target,fit_min_ctx,n_prompt,n_gen,n_depth,test_time,avg_ns,stddev_ns,avg_ts,stddev_ts
"c1d0e7a","1","AMD RYZEN AI MAX+ 395 w/ Radeon 8060S","Radeon 8060S Graphics (RADV STRIX_HALO)","Vulkan","/home/james-matheson/models/qwen3-coder-q4ks/Qwen3-Coder-30B-A3B-Instruct-Q4_K_S.gguf","qwen3moe 30B.A3B Q4_K - Small","17450039296","30532122624","512","512","16","0x0","0","50","f16","f16","999","0","layer","0","0","1","auto","0.00","none","none","0","0","0","0","0","512","0","0","2026-08-26T06:32:55Z","407308887","4724901","1257.192821","14.662954"
"c1d0e7a","1","AMD RYZEN AI MAX+ 395 w/ Radeon 8060S","Radeon 8060S Graphics (RADV STRIX_HALO)","Vulkan","/home/james-matheson/models/qwen3-coder-q4ks/Qwen3-Coder-30B-A3B-Instruct-Q4_K_S.gguf","qwen3moe 30B.A3B Q4_K - Small","17450039296","30532122624","512","512","16","0x0","0","50","f16","f16","999","0","layer","0","0","1","auto","0.00","none","none","0","0","0","0","0","0","128","0","2026-08-26T06:33:03Z","1291935824","2500714","99.076481","0.191808"
```

### Qwen3-Coder 30B-A3B UD-Q4_K_XL

```csv
build_commit,build_number,cpu_info,gpu_info,backends,model_filename,model_type,model_size,model_n_params,n_batch,n_ubatch,n_threads,cpu_mask,cpu_strict,poll,type_k,type_v,n_gpu_layers,n_cpu_moe,split_mode,main_gpu,no_kv_offload,flash_attn,devices,tensor_split,tensor_buft_overrides,load_mode,embeddings,no_op_offload,no_host,fit_target,fit_min_ctx,n_prompt,n_gen,n_depth,test_time,avg_ns,stddev_ns,avg_ts,stddev_ts
"c1d0e7a","1","AMD RYZEN AI MAX+ 395 w/ Radeon 8060S","Radeon 8060S Graphics (RADV STRIX_HALO)","Vulkan","/home/james-matheson/models/qwen3-coder/Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf","qwen3moe 30B.A3B Q4_K - Medium","17659361280","30532122624","512","512","16","0x0","0","50","f16","f16","999","0","layer","0","0","1","auto","0.00","none","none","0","0","0","0","0","512","0","0","2026-08-26T06:33:36Z","396807623","4672036","1290.467259","15.152259"
"c1d0e7a","1","AMD RYZEN AI MAX+ 395 w/ Radeon 8060S","Radeon 8060S Graphics (RADV STRIX_HALO)","Vulkan","/home/james-matheson/models/qwen3-coder/Qwen3-Coder-30B-A3B-Instruct-UD-Q4_K_XL.gguf","qwen3moe 30B.A3B Q4_K - Medium","17659361280","30532122624","512","512","16","0x0","0","50","f16","f16","999","0","layer","0","0","1","auto","0.00","none","none","0","0","0","0","0","0","128","0","2026-08-26T06:33:45Z","1323069694","3517369","96.745362","0.256256"
```

### Qwen3.6 35B-A3B MTP IQ4_XS-Q8nextn

```csv
build_commit,build_number,cpu_info,gpu_info,backends,model_filename,model_type,model_size,model_n_params,n_batch,n_ubatch,n_threads,cpu_mask,cpu_strict,poll,type_k,type_v,n_gpu_layers,n_cpu_moe,split_mode,main_gpu,no_kv_offload,flash_attn,devices,tensor_split,tensor_buft_overrides,load_mode,embeddings,no_op_offload,no_host,fit_target,fit_min_ctx,n_prompt,n_gen,n_depth,test_time,avg_ns,stddev_ns,avg_ts,stddev_ts
"c1d0e7a","1","AMD RYZEN AI MAX+ 395 w/ Radeon 8060S","Radeon 8060S Graphics (RADV STRIX_HALO)","Vulkan","/home/james-matheson/models/Qwen3.6-35B-A3B-MTP-IQ4_XS-Q8nextn.gguf","qwen35moe 35B.A3B IQ4_XS - 4.25 bpw","19382469120","35505251456","512","512","16","0x0","0","50","f16","f16","999","0","layer","0","0","1","auto","0.00","none","none","0","0","0","0","0","512","0","0","2026-08-26T06:34:14Z","446693871","6166163","1146.405775","15.781659"
"c1d0e7a","1","AMD RYZEN AI MAX+ 395 w/ Radeon 8060S","Radeon 8060S Graphics (RADV STRIX_HALO)","Vulkan","/home/james-matheson/models/Qwen3.6-35B-A3B-MTP-IQ4_XS-Q8nextn.gguf","qwen35moe 35B.A3B IQ4_XS - 4.25 bpw","19382469120","35505251456","512","512","16","0x0","0","50","f16","f16","999","0","layer","0","0","1","auto","0.00","none","none","0","0","0","0","0","0","128","0","2026-08-26T06:34:24Z","1679730061","2088230","76.202832","0.094647"
```
