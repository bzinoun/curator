---
topic: mac-unified-memory-gpu-ceiling
date: 2026-08-26
project: zakariabelarrem
session: d187ff9b
density: 3
tone: factual
lang_hint: en
tags: [apple-silicon, memory, gpu, local-inference]
status: drafted
---
On Apple Silicon Macs, the real VRAM ceiling is **~24–28 GB** (not the full 32 GB), and it's a hard stop.

macOS reserves ~4 GB for the kernel, and the `iogpu.wired_limit_mb` sysctl defaults to 75% of unified memory for GPU use. A 27B model in 4-bit takes 16 GB; a 29 GB model doesn't fit at all, even if you have 32 GB on paper.

When model + KV cache exceed the GPU limit, macOS forcibly swaps to disk (SSD paging), tanking throughput from 42 tok/s to ~4 tok/s. Quantization (16-bit → 4-bit) shrinks weight footprint. Mixture-of-experts shrinks active weight per token. Both are necessary on constrained hardware.

For practitioners: measure your actual `iogpu.wired_limit_mb`, check model size under full cache load, and keep a 2–3 GB safety margin before swap begins.
