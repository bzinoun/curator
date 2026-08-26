---
topic: regex-boundaries-in-error-detection
date: 2026-08-26
project: agentic-factory
session: f0368c8e
density: 2
tone: factual
lang_hint: en
tags: [reliability,error-handling,monitoring,api-integration]
status: new
---
A missing word in an error-detection regex cost 8 days of pipeline downtime. The provider's message was *"You've hit your monthly spend limit"*; the pattern matched only *"usage limit | rate limit | limit reached | out of quota."* 

The generic error branch treated it as retryable-once, then permanent. The auto-recovery mechanism existed already but never triggered.

Lesson: **error messages from external APIs are ephemeral and vendor-specific.** Each provider phrases quotas differently. Maintaining per-provider regex patterns breaks under API churn. Better approach: *positive lookahead for the semantic intent* (cost/quota/exhausted) plus broad fallback classification, plus explicit logging of classification failures.

---
