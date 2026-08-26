---
topic: archimate-rendering-from-python
date: 2026-08-26
project: ao-assurance
session: 3b4dc085
density: 4
tone: factual
lang_hint: en
tags: [architecture-as-code, diagram-generation, draw.io]
status: parked
---
**Rendering ArchiMate diagrams programmatically from Python to draw.io.**

ArchiMate (ISO/IEC 42010) provides standardized architectural notation—eight relationship types (composition, aggregation, affectation, realization, service, trigger, flow, access), layered element types (Motivation, Business, Application, Technology, Implementation). Most teams hand-draw these or use desktop tools. But generating them *from code* is rare.

An approach: write a Python class that emits draw.io XML. Each `element()` call creates a box (colors keyed to layers); each `service()` or `agregation()` adds a typed relationship with the correct marker (losange for composition, oval for affectation, arrow for service). Build an internal graph, then serialize to draw.io's `<mxGraphModel>` format—no CLI dependency, outputs `.drawio` files that open in draw.io and export to SVG/PNG.

Critical detail: ArchiMate's notation is its precision—the type icon (corner square) and relationship terminator must be exact, or the diagram lies. A code generator enforces that discipline; hand-drawn views drift fast.

Result: architecture stays in version control, regenerable, and aligned with code reality.
