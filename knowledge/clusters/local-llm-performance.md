# Cluster : local LLM performance — la bande passante mémoire, pas le compute
Membres :
- 2026-08-26-llm-speed-bandwidth-formula.md
- 2026-08-26-moe-paradox-larger-model-faster.md
- 2026-08-26-mac-unified-memory-gpu-ceiling.md

Synthèse : sur un Mac M1 Pro 32 GB, tokens/s = bandwidth ÷ poids lus par token
(135 GB/s ÷ 27 GB = 5 tok/s en dense 27B ; 135 ÷ 3.2 = 42 tok/s en MoE 35B/3.2B actifs).
Le modèle plus gros est 8× plus rapide. Le plafond GPU réel est ~24-28 GB (pas 32) :
dépassé, macOS swappe et le débit tombe à 4 tok/s. → Article EN.
