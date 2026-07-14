# Phase 3 — Rendering

Turn `blueprint-model.json` into the final `service-blueprint.html`.

## How the template works

`assets/blueprint-template.html` is self-contained (inline CSS + vanilla JS, no
network calls). It reads a single JavaScript object, `BLUEPRINT_MODEL`, and
builds the whole blueprint from it at load time. The template ships with a
realistic sample model so it previews on its own.

## To render

1. Copy `assets/blueprint-template.html` to the output as `service-blueprint.html`.
2. Replace the sample object between the two markers:
   ```
   /* === BLUEPRINT_MODEL:START === */
   const BLUEPRINT_MODEL = { ...sample... };
   /* === BLUEPRINT_MODEL:END === */
   ```
   with `const BLUEPRINT_MODEL = <your blueprint-model.json>;`. Do not change any
   code outside these markers.
3. Save `blueprint-model.json` next to the HTML so the model can be edited and
   re-rendered later.

That's it — the template handles both lane models, arbitrary phases, system
badges, the core/full toggle, and deviation overlays automatically. There is no
per-run HTML authoring; the model is the only thing that changes. This is what
keeps the skill reusable and the output consistent.

## What the template renders

- **Left icon rail** (always visible) with a panel toggle plus control icons.
- **Flyout panel** (open by default, collapsible) holding three sections:
  - **Controls** — four toggles: **Deviations** (Core only ⇄ All), **Handoffs**
    (highlight steps where the system of record changes), **Flow lines** (the
    sequential orthogonal connectors), and **Pain points** (the red band at the
    bottom of any card that has pain points), plus a **Minimap** toggle on the rail.
  - **Legend** — core vs deviation, and the confidence dots.
  - **System Inventory** — a vertical list of every identified system with its
    type; tapping one highlights every step that touches it.
- **Header** — title, process domain, source transcripts, `confidence_notes`.
- **Matrix** — phases as numbered columns, lanes as rows; step cards in the
  correct lane×phase cell, each with a **sequence badge**, name, actor, system
  badges, confidence dot. The sequence badge is derived automatically from
  `order` + the deviations: the first core step reads **Start**, the rest of the
  happy path counts 1.0 → 2.0 → 3.0 left-to-right, and each deviation takes its
  branch parent's number plus .5 (a branch off 2.0 becomes 2.5). No numbering
  goes in the model — it's computed at render time, so re-ordering steps
  re-labels them.
- **Connectors** — orthogonal (straight / right-angle only, never curved) lines
  link the steps in sequence, following the model's `connections` (or, if absent,
  the core steps in `order`). Every line anchors to one of a box's four magnet
  points — the mid-point of each side for a card, each tip for a diamond. Forward
  edges step off the right/bottom magnet into the next box's left/top magnet; a
  **loop-back** (target earlier in `order`) is drawn as a separate line routed
  beneath the boxes rather than cutting back through the flow. Deviation branches
  draw dashed amber; arrowheads show direction; lines run behind the cards. The
  **Flow lines** control toggles them.
- **Deviation overlays** — a core step a deviation branches from gets an amber
  badge with a count; the exceptions drawer lists each deviation. Both hidden in
  "core only" mode.

The controls that ship by default are Deviations, Handoffs, Flow lines, and Pain
points (plus the Minimap). To add more
(e.g. a confidence filter, a phase collapse), add an icon to the rail and a row
to the Controls section, wired to a body class — follow the existing pattern.

## If the template needs to change

Only change the template when the *shape* of the visual changes (new lane model,
a new kind of overlay). Style tweaks are fine. Keep it dependency-free and keep
the `BLUEPRINT_MODEL` marker block intact so future renders stay a data swap.
