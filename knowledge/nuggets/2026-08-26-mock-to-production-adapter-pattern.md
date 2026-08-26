---
topic: mock-to-production-adapter-pattern
date: 2026-08-26
project: ao-assurance
session: a8ff953a
density: 5
tone: factual
lang_hint: en
tags: [architecture, testing, interfaces]
status: new
---
Replace feature-flag-gated mock code with two **implementations behind a shared port**. One adapts the real database; another serves hardcoded data. Exactly one bean is active per domain, configured independently.

```
interface QuittanceRepository
├── JpaAdapter (real table)
└── MockAdapter (data in-memory)
```

**Why this works**: the service layer never changes. When un assureur delivers the real schema, flip one config line and swap implementations. No feature flags, no dead code paths, no "TODO when table arrives." Tested here on four domains (quittances, contracts, referentials, audit trail); all four flipped independently.

**Caveat**: the mock must **replicate constraints** (e.g., agent-level filtering) exactly, or tests won't catch real bugs.
