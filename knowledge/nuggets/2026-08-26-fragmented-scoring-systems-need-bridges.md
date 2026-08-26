---
topic: fragmented-scoring-systems-need-bridges
date: 2026-08-26
project: agentic-factory
session: f0368c8e
density: 3
tone: opinionated
lang_hint: en
tags: [system-architecture,data-pipelines,product-operations,feedback-loops]
status: drafted
---
Two scoring systems can measure complementary truths and still be worthless if unconnected. In production: one system measured niche viability by keyword shelf saturation (7 metrics, all measurable); another scored concept feasibility via LLM judgment (douleur, monétisation, risque conformité). Neither was wrong.

They just never spoke. The first system opened 10 issues; the second system's selection criteria couldn't find them (mismatched labels). **For 34 days, 10 discovered niches sat in a dead letter queue.**

The repair was one line in a consigne: add the labels that upstream expects. But the lesson scales: **measure systems are only complete if their outputs are consumable by downstream systems.** A brilliant niche score that gets routed to the void is worse than no score at all — it *appears* productive while staying isolated.
