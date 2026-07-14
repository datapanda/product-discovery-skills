# Service Blueprint Skill

Turn customer discovery-call transcripts into an interactive, self-contained
HTML **service blueprint** — a swimlane map of how a process actually runs:
the steps, who performs them, the systems of record they touch, the common
core ("happy path"), and the deviations from it.

Built iteratively with Claude; portable to any LLM agent that can read
markdown and write JSON.

## What it produces

A single `service-blueprint.html` (no external dependencies, opens in any
browser) with:

- **Zoned swimlanes** — Customer Journey, Front Stage (Employee actions +
  Systems), Backstage actions, Support processes — each zone with a thin
  colored section bar, plus numbered phases across the top.
- **Rich step cards** — color-coded category header with a sequence number
  (`Start`, `1.0`, `2.0`…; deviations get `n.5`), title, description,
  actor/time/channel/evidence meta, tags, an inline-expand (systems + success
  metric), and a full-detail lightbox.
- **Pain points** as a red band on the bottom of affected cards; **handoffs**
  (system-of-record changes) as a blue band that stacks with it.
- **Decision diamonds** for genuine core-path forks, with labeled branches.
- **Orthogonal flow connectors** (straight/right-angle, magnet-point anchored;
  loop-backs route beneath the flow as separate lines).
- **Controls** in a push/pull flyout: core-only ⇄ all variations, handoffs,
  flow lines, pain points, a legend, and a **System Inventory** (tap a system
  to highlight every step that touches it).
- **Navigation** for large maps: StarCraft-style minimap (drag to pan,
  collapsible), zoom (Ctrl/Cmd+wheel or pinch, Ctrl/Cmd +/−/0, on-canvas
  buttons), frozen phase headers and lane labels.
- An **exceptions drawer** listing every deviation with its trigger,
  frequency, impact, and rejoin point.

## How it works

Three phases, each writing an artifact the next reads:

1. **Extract** (`references/extraction.md`) — per transcript, independently:
   ordered steps, actors, systems, conditional language (deviation
   candidates), pain points, and card details. → `extract-<name>.json`
2. **Synthesize** (`references/synthesis.md`) — align extractions into one
   canonical process; decide core vs deviation. Handles both **overlapping**
   interviews (frequency-based) and **role-segmented** interviews where each
   person owns a different slice (role-ownership-based). Conflicts between
   interviewees are preserved and shown, not silently resolved.
   → `blueprint-model.json`
3. **Render** (`scripts/render.py`) — validate the model (referential
   integrity) and splice it into `assets/blueprint-template.html`.
   → `service-blueprint.html`

The `blueprint-model.json` schema (`references/blueprint-schema.md`) is the
contract between phases — hand-editable and re-renderable.

## Usage

**With Claude:** install `service-blueprint` as a skill (or point Claude at
this folder), then provide one or more transcripts: *"Build a service
blueprint from these interviews."*

**With any LLM agent:** have it read `SKILL.md` and follow the pipeline. A
known-good model built from three real interviews is in
`examples/blueprint-model.example.json` — the best reference for shape.

**Render manually:**

```bash
python3 scripts/render.py path/to/blueprint-model.json
# → service-blueprint.html (validates first; stdlib only, no installs)
```

## Inputs

One or more discovery-interview transcripts (`.txt`, `.md`, `.vtt`, `.docx`,
or pasted text). More transcripts sharpen the core-vs-deviation distinction;
a single transcript yields a provisional core based on conditional language
("usually…", "unless…", "when it's urgent…").

## Package contents

```
service-blueprint/
├── SKILL.md                              # pipeline orchestration + modeling concepts
├── README.md                             # this file
├── references/
│   ├── extraction.md                     # per-transcript extraction procedure
│   ├── synthesis.md                      # alignment + core-vs-deviation logic
│   ├── blueprint-schema.md               # the model contract + validation checklist
│   └── rendering.md                      # template mechanics + manual splice
├── assets/
│   └── blueprint-template.html           # self-contained render target (built-in sample)
├── examples/
│   └── blueprint-model.example.json      # validated model from 3 role-segmented interviews
└── scripts/
    └── render.py                         # stdlib-only validate + render
```

## Design notes

Step cards implement the "Blueprint Card (Direction 1a)" design handoff:
Helvetica type system, 28px color-coded header, meta grid, inline expansion,
and a 520px lightbox. Category colors — Customer Journey `#D07B45`, Front
Stage `#587DA8`, Backstage `#8A8177`, Support `#7E8D80`; decisions are ember orange;
pain bands `#A85043`. Spacing keeps ≥16px between objects, including the
diamonds' rotated footprint. Zone section bars sit at the back of the
z-order; connectors above them; cards on top.

## Requirements

- To generate: an LLM agent that can read these files and write JSON/text.
- To render: Python 3 (stdlib only) — or do the marker splice by hand per
  `references/rendering.md`.
- To view: any modern browser. No network access needed at any stage.
