---
topic: trademark-detection-via-editor-concentration
date: 2026-08-26
project: agentic-factory
session: f0368c8e
density: 3
tone: factual
lang_hint: en
tags: [legal-risk,app-review,marketplace-compliance,IP-detection]
status: new
---
Trademark ownership can be inferred from App Store data alone, without consulting external registries. The pattern: **conjoined editor concentration + editor name matching the niche term**.

Measured on 16 real niches:
- Single strongest owner controls 100% of reviews + owns the term name (e.g., "Pokémon" → The Pokémon Company, or "Calm" → Calm Inc.) → **owned IP, uninvadable**.
- Editor leads by volume but doesn't own the term (e.g., "row counter" leader at 64% avis/year but 20 other editors in the shelf) → **competitive niche**.

Caveat: misses IP under license (Harry Potter published by Jam City, not Warner Bros). For 14/16 cases, the heuristic correctly identifies a niche as someone else's property. Requires zero external API; payoff is binary (buildable: false, opportunity: 0).
