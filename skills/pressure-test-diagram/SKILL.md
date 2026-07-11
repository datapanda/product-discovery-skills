---
name: pressure-test-diagram
description: Pressure-test a process diagram for decomposition quality — flags steps that hide complexity or add noise, and proposes concrete splits/merges.
argument-hint: [path to a mermaid/diagram file, or paste a description of the flow]
allowed-tools: Read
model: opus
---

You are reviewing a process diagram for **decomposition quality**: whether each step is sized right — not so coarse it hides complexity, not so fine it adds noise.

## Input

The diagram to review: $ARGUMENTS

If `$ARGUMENTS` is a file path, read it. If it's a pasted description, work from that. If it's an attached image, read the image. If no diagram is present, ask for one and stop.

## The standard

A well-sized step has exactly three properties:
1. **One owner** — a single actor or system is responsible start to finish.
2. **One exit condition** — there's a single, nameable state that's true when it's done.
3. **One place it can go wrong** — a single dominant failure mode.

When a box violates more than one of these, it's a split candidate. When adjacent boxes *share* all three, they're a merge candidate. Judge against this standard, not against taste.

## Do not skip the inventory

Before any critique, list **every** step and gateway in the diagram as a numbered table with three columns: `Step | Owner | Exit condition (what's true when done)`. If you cannot name the owner or the exit condition for a box, that gap is itself a finding — record it. Do not summarize or judge from memory of the diagram; work off this explicit inventory. This step is mandatory and prevents hand-waving.

## Pass 1 — Under-decomposed? (steps hiding complexity)

For each step, run these. Flag any that fire:

- **And/then test** — Can you describe it without "and" or "then"? "Validate and email" is two steps in one box.
- **Handoff test** — Does one actor/system start it and a different one finish it? A change of hands is a seam.
- **Hidden-decision test** — Could it resolve more than one way (success/failure, approved/rejected) that leads somewhere different downstream? That's a branch buried inside a box — it should be a visible gateway.
- **Wait-state test** — Does it run start-to-finish without pausing on something external (approval, batch job, third-party callback)? A meaningful pause is a seam between two steps.
- **Failure-mode test** — Ask "what if this times out / errors / is rejected?" If the answer is interesting and isn't already on the diagram, it's under-decomposed.

## Pass 2 — Over- or mis-decomposed? (boxes adding noise)

- **State-change test** — After the step, can you name something now true that wasn't before? If nothing meaningfully advanced, the box may be decoration.
- **Altitude test** — Is each step at the same level of abstraction as its siblings? "Log in" next to "Onboard the customer" is uneven decomposition.
- **Merge test** — Do two adjacent steps *always* fire together, same owner, no branch or wait between them? Collapse them.

## Pass 3 — Whole-diagram checks

- Gateways with unlabeled or missing branches (esp. the "no/failure" edge).
- Steps with no failure or timeout path at all.
- Dead ends (a branch that goes nowhere) and orphan steps (nothing leads to them).
- Overall altitude consistency — is the whole diagram pitched at one level, or does it lurch between strategy and keystrokes?

## Build the "after" inventory

Once findings are set, produce a target inventory showing what the diagram *should* become — the before/after side-by-side is what turns a critique into a work plan.

Numbering rules, so the after-table stays diff-able against the before:
- **Splits** keep the parent number with letter suffixes: box `15` becomes `15a Ship Items`, `15b Prepare Invoice`.
- **Genuinely new boxes** (gateways, terminals, steps with no parent) get `NEW-1`, `NEW-2`, … numbered in flow position.
- **Merges** collapse to the lower parent number, noting the absorbed one: `4 (was 4+5)`.
- **Unchanged** boxes keep their original number verbatim.
- Do **not** renumber unchanged boxes — the original numbering is the shared reference across the other diagram commands and must survive.

Every row that isn't fully specified stays an **explicit placeholder**, not a silent omission. Mark status per row:
- `✅ resolved` — the target box is fully defined.
- `⬜ placeholder` — known to be needed but not yet specified (e.g. `NEW-2 vendor-declines terminal — destination undefined`). A placeholder is a checklist item, not a failure; leave it visibly open.

## Output

1. **Before inventory** — the numbered current-state table (from above).
2. **Findings**, ordered by severity. Each finding is one row:
   `Step # | Test that fired | Why it matters (1 sentence) | Concrete fix`
   The fix must be actionable — "split into *Validate input* → *Send confirmation email*", "merge 4+5", "add a rejected-path gateway after 3", "add timeout edge on 6" — not "consider revisiting."
3. **After inventory** — the target-state table: `Box # | Name | Owner | Change | Status (✅/⬜)`. Splits, new boxes, and merges numbered per the rules above; unchanged boxes carried over verbatim.
4. **Fix checklist** — the deltas only (every row that changed or is new), as a checkbox list ready to work through, e.g.
   `- [ ] 15 → split into 15a Ship Items / 15b Prepare Invoice`
   `- [ ] NEW-1 Goods match order? gateway after 16`
   `- [ ] NEW-2 vendor-declines terminal — ⬜ destination undefined`
   Order by leverage. Open placeholders stay unchecked with their `⬜` note.
5. **What's solid** — 1–2 boxes that are correctly sized, so the review isn't only negative.
6. **Verdict** — one line: is this under-decomposed, over-decomposed, uneven, or well-balanced, and the single highest-leverage change to make first.

Be direct. If a box is fine, say so and move on — don't invent problems to fill the table.
