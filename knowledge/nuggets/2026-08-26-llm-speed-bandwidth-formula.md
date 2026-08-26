---
topic: llm-speed-bandwidth-formula
date: 2026-08-26
project: zakariabelarrem
session: d187ff9b
density: 5
tone: factual
lang_hint: en
tags: [llm-performance, inference, apple-silicon, model-selection]
status: new
---
An LLM's inference speed isn't bounded by compute—it's bounded by **memory bandwidth**.

Every token requires re-reading the model's weights. The formula is elegantly simple:

```
tokens/sec = effective_bandwidth ÷ weights_read_per_token
```

Measured on an M1 Pro (32 GB unified memory): 135 GB/s effective bandwidth. A dense 27B model reads 27 GB per token → 5 tok/s. A 35B MoE reading only 3.2 GB active per token → 42 tok/s — the larger model is 8× faster.

This explains why quantization (reducing weight size) and mixture-of-experts (reducing active weights) are complementary tools: they both shrink the denominator. Before downloading a model, divide your bandwidth by its expected weight footprint to predict real-world performance.

---
