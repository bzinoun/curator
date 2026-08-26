---
topic: distributed-dto-contracts-silent-divergence
date: 2026-08-26
project: insurtech
session: 30d6e924
density: 3.5
tone: factual
lang_hint: en
tags: [architecture, typescript, contract-testing, observability]
status: new
---
A microservice bot and API exchanged a DTO `NegotiationContext` with fields `claimId`, `quittanceId`. The bot typed it locally; the API never exposed these fields. TypeScript compiled without error. At runtime both fields were `undefined`, silently skipping two branches of bot logic—no exception, no log, just silence.

When you type a distributed DTO in two separate projects, the contract is unverified. The TypeScript safety is illusory: a schema mismatch at runtime produces the most dangerous outcome—code that doesn't crash but doesn't work.

**Fix:** OpenAPI + runtime validation, or a shared generated client; never hand-typed DTOs across service boundaries.

**Diagnosis:** Silence (not error) is the telltale. Root cause required tracing through the API response to spot the gap. Add explicit logging on *both* success and skip paths so divergence shows up in logs, not in hidden control flow.

---
