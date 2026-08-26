---
topic: wcag-contrast-ratio-small-text-trap-in-design-systems
date: 2026-08-26
project: agentic-factory
session: f2fcfdab
density: 3
tone: factual
lang_hint: en
tags: [accessibility, wcag, design-systems, color-contrast]
status: parked
---
A common design-system pitfall: a single "faint" gray variable passes WCAG AA contrast testing on large text (44px+) but fails on small text (≤12.5px). The same color (#9aa1ad on white) achieves 2.7:1 contrast but requires ≥4.5:1 for footnotes and labels.

Systems often define one `--faint` applied uniformly to footer text (12.5px), metadata labels (0.7rem), and larger elements. Testing reveals the failure only on the smallest deployed sizes. Fix: either create separate `--faint-small` and `--faint-large` variables tied to text size, or validate contrast at the smallest deployed size first and ensure the single variable exceeds 4.5:1 across all contexts. This is especially critical for footnotes, captions, and helper text in form fields.
---
