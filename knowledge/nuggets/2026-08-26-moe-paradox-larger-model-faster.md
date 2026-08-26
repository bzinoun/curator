---
topic: moe-paradox-larger-model-faster
date: 2026-08-26
project: zakariabelarrem
session: d187ff9b
density: 4
tone: opinionated
lang_hint: en
tags: [moe, model-architecture, model-selection, performance]
status: drafted
---
Counterintuitive: a **larger** open-weight LLM runs faster than a smaller one on the same hardware.

A 35B mixture-of-experts (MoE) with 3.2B active parameters beats a 27B dense model by 5× in throughput. Same Mac, same RAM, different architecture.

The dense model reloads all 27B weights per token. The MoE stores 35B on disk but routes only 3.2B through computation per forward pass—activating different expert sets by token position.

This inverts the conventional "bigger = slower" intuition. On constrained hardware (a single GPU, a Mac, an edge device), prioritize models by **active parameters**, not total parameters. A 100B MoE with 5% activation can outperform any 20B dense model while offering richer world knowledge.

---
