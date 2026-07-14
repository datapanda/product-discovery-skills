---
name: service-blueprint
description: >-
  Generate an interactive HTML service blueprint from one or more customer call
  transcripts. Use this whenever the user has call transcripts, discovery-call
  notes, or interview recordings describing how a business process actually runs
  and wants them turned into a service blueprint, process map, swimlane, or
  "as-is" process diagram. Trigger this even when the user says "map this
  process," "blueprint our workflow," "what systems are involved," or "show the
  happy path vs the exceptions" — anytime transcripts need to become a
  structured, visual process artifact that identifies process steps, systems of
  record (ERP, CRM/Salesforce, spreadsheets, email, etc.), the common core
  process, and where deviations from the normal path occur.
---

# Service Blueprint from Call Transcripts

Turn raw customer/discovery call transcripts into a single, self-contained,
interactive HTML **service blueprint**: a layered swimlane view of a process
that shows the steps, who performs them, the systems of record touched at each
step, the **common core ("happy path")**, and the **deviations** (exceptions,
branches, and variants) that occur.

This skill separates *understanding* (reading transcripts and building a
structured model) from *rendering* (turning that model into HTML). Always
produce the intermediate model first — it is what makes the output consistent,
inspectable, and reusable.

## What these transcripts are

The transcripts are **discovery / as-is interviews**: an interviewer asks a team
how their process actually works, and the interviewee narrates it. Two
consequences shape everything downstream:

- **Map the described process, not the conversation.** The process lives in the
  interviewee's narration ("first we log it, then finance checks it…"), not in
  the back-and-forth of the interview. Ignore interviewer scaffolding
  ("walk me through," "and then what?") except as cues to sequence.
- **Track hearsay.** Interviewees often describe steps other teams perform,
  which they may only partly understand. When a step is second-hand, lower its
  `confidence` and note who described it. A blueprint that quietly presents
  second-hand guesses as fact is worse than one that flags them.

## Pipeline overview

Run these phases in order. Each phase writes an artifact the next phase reads.

1. **Extract** — For each transcript independently, pull an ordered list of
   process steps, the actor/lane for each, the systems of record involved, and
   any pain points or conditional language. → one `extract-<name>.json` per
   transcript. See `references/extraction.md`.
2. **Synthesize** — Align the per-transcript extractions into one canonical
   process. Decide what is **core** vs a **deviation**, merge equivalent steps,
   and record which transcripts support each step. → `blueprint-model.json`.
   See `references/synthesis.md`. A known-good example model is at
   `examples/blueprint-model.example.json` — imitate its shape.
3. **Render** — Run `python3 scripts/render.py blueprint-model.json` to validate
   the model and splice it into `assets/blueprint-template.html`, producing
   `service-blueprint.html`. The script is stdlib-only. If Python is
   unavailable, splice by hand per `references/rendering.md` — replace ONLY the
   `const BLUEPRINT_MODEL = {...};` statement between the `BLUEPRINT_MODEL:START`
   and `:END` markers, and run the checks in the schema doc's "Validate before
   rendering" list yourself.

The `blueprint-model.json` schema is the contract between phases and is defined
in `references/blueprint-schema.md`. Read that first if you are unsure what a
field means.

## When you have only one transcript

The skill still works with a single transcript, but "core vs deviation" cannot
be established by cross-transcript frequency. Instead:

- Treat the main narrated sequence as the provisional core process.
- Flag **conditional language** as candidate deviations even within one call:
  phrases like "usually / normally / most of the time," "sometimes / occasionally,"
  "if X then," "unless," "the exception is," "for enterprise customers we
  instead," "when it's urgent." These signal branches off the happy path.
- In the model, mark these steps `variant: "deviation"` with
  `support_count: 1` and note that confidence is lower.

Tell the user explicitly that a single transcript yields a *provisional* core
and that adding more transcripts sharpens the core/deviation distinction.

## Inputs

- One or more transcript files (`.txt`, `.vtt`, `.md`, `.docx`, or pasted text).
- Optional context from the user: the process name/domain (e.g. "order-to-cash,"
  "customer onboarding"), known systems, or which team is being interviewed.

If transcripts are messy (no speaker labels, interleaved crosstalk), still
proceed — infer actors from context and note lower confidence in `meta`.

## Output

A single self-contained `service-blueprint.html` (all CSS/JS inline, no external
dependencies) that opens in any browser. Alongside it, keep
`blueprint-model.json` so the user can edit the model and re-render, or diff
across versions.

## Core modeling concepts

The `blueprint-model.json` fields, the section-bar/lane mechanics, and the exact
category colors are defined in `references/blueprint-schema.md` — this is only the
modeling judgment behind them.

**Lanes.** Prefer the classic service-blueprint stack: **Customer Journey**, a
nested **Front Stage** group (Employee actions + customer-visible **Systems**),
**Backstage actions**, **Support processes**. For an internal cross-team workflow
with no end-customer journey, use **actor lanes** (Customer / Sales / Ops /
Finance…) instead — set `meta.lane_model: "actor_lanes"` and justify it in
`meta.confidence_notes`. The renderer draws whatever lanes the model provides.

**Phases** are the coarse left-to-right stages (Intake → Qualify → Fulfill →
Close); every step belongs to one and carries an `order`.

**Systems of record.** Every tool mentioned (ERP, CRM, spreadsheets, email,
ticketing, homegrown apps) gets one `systems_of_record` entry, referenced by id
from each step that touches it; the render surfaces them as card chips, an
inventory, and a "Handoffs" toggle that marks where the system of record changes.

**Decisions vs deviations — keep these distinct.** A `kind: "decision"` step is a
genuine fork in the core path where *both* outcomes are normal (a diamond with
labeled `branches`). A **deviation** is an exception triggered by a condition
(credit hold, missing data, escalation, rework) or a step seen in only some
transcripts. Never model an exception as a decision.

**Core vs deviation is the central analytical job.** Core = steps consistent
across transcripts (or the main narrated path in a single call); deviations =
conditional branches off it, each naming its trigger, which transcripts show it,
and where it rejoins the core (see `references/synthesis.md` for the alignment
logic). In the render, deviations are not separate lanes — each is an overlay
badge on the core step it branches from, and one global toggle flips the whole
blueprint between core-only and all-variations.

## Quality bar

- Every step must cite evidence: which transcript(s) and a short paraphrased
  reference (do not paste long verbatim transcript passages into the model).
- Do not invent systems or steps not grounded in a transcript; if you infer,
  mark it and lower confidence.
- Deviations must have a stated trigger — "it depends" is not a trigger.
- The final HTML must render with zero external network calls.

## Reference files

- `references/extraction.md` — per-transcript extraction procedure + prompts.
- `references/synthesis.md` — aligning transcripts; core vs deviation logic,
  including the overlapping vs role-segmented coverage distinction.
- `references/blueprint-schema.md` — the `blueprint-model.json` schema and the
  pre-render validation checklist.
- `references/rendering.md` — how the template works and the manual splice.
- `assets/blueprint-template.html` — the self-contained render target (opens
  standalone with a built-in sample).
- `examples/blueprint-model.example.json` — a complete, validated model built
  from three real role-segmented interviews; the best reference for shape.
- `scripts/render.py` — stdlib-only validate + render.

## Portability note

This skill assumes only: (1) an agent that can read these markdown files and
write JSON/text files, and (2) optionally Python 3 for `scripts/render.py`. No
network access, package installs, or vendor-specific tooling is required — the
template is a single self-contained HTML file. Any LLM agent that can follow the
three-phase pipeline and produce a valid `blueprint-model.json` can use it.
