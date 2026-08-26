---
topic: mock-data-visibility-marker
date: 2026-08-26
project: ao-assurance
session: a8ff953a
density: 3
tone: factual
lang_hint: en
tags: [ux, demo, data-integrity]
status: new
---
When displaying mocked data alongside real data, don't concatenate a `(*)` to the string—carry a boolean `mocke: true` in the DTO and render the marker as a **visual-only annotation** in the UI layer.

**Why**: tables with sort and filter will split "Bris de glace" and "Bris de glace (*)" into separate values. The asterisk also pollutes exports, spreadsheets, and customer-facing outputs. With a flag, the marker stays purely informational and removal—when the real table arrives—happens in one place.
