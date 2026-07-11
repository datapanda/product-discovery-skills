---
name: assess-diagram-quality
description: Assess a process diagram's overall quality against a rubric — scores completeness, control-flow integrity, decomposition, ownership, data traceability, clarity, and fit-for-purpose, then separates what it can judge from the artifact from what a human must verify against reality.
argument-hint: [diagram path or description] — optionally state the purpose/audience
allowed-tools: Read
model: opus
---

You are giving a process diagram an overall **quality assessment** — a report card, not a deep dive. Your job is to say how trustworthy this map is and whether it's captured at the right level, with scored evidence and a single highest-priority fix.

## Input

The diagram to assess: $ARGUMENTS

If `$ARGUMENTS` is a file path, read it. If it's an attached image, read it. If no diagram is present, ask for one and stop.

**Purpose is required for one dimension.** If the person hasn't stated the diagram's *purpose and audience* (onboarding a new hire? exec sign-off? handing to a build team? redesign analysis?), ask once, then proceed. If they decline, assess against a stated default and flag it.

## How this relates to the other commands

This is the triage layer. Where a dimension scores low and they want depth, point them to:
- **Decomposition & altitude** → `/pressure-test-diagram`
- **Data & artifact traceability** → `/interrogate-data-sources`

Don't duplicate those analyses here — summarize and defer.

## Do not skip the inventory

Before scoring anything, build a numbered table of **every** box and gateway in the diagram: `Box # | Name | Owner`. Number activities and decisions in flow order. If you can't name a box's owner, leave it blank — that gap is itself evidence for the ownership dimension.

This numbering is load-bearing: it is the shared reference across all three diagram commands, so `/pressure-test-diagram` and `/interrogate-data-sources` line up box-for-box with this report. From this point on, **refer to every box by its number** (e.g. "box 15"), not by name alone, in the scorecard and everywhere else.

## Scoring rule

Rate each dimension **1–4**: `1 Absent · 2 Partial · 3 Solid · 4 Strong`. Two hard rules:
- **No score without evidence.** Cite specific box numbers or edges for every rating. A rating with no citation is invalid.
- **When evidence is mixed, score down.** Do not inflate. A diagram that's polished but incomplete is not "Strong."

## The rubric

**1 · Completeness of paths** *(blocking)* — all real paths present: happy path, exceptions, failures, edge cases, with explicit start and end state(s).
`1` happy path only · `2` some exceptions, major failures missing · `3` main exceptions & failures covered, ends explicit · `4` exceptions, failures, timeouts, and terminal states all present and reachable.

**2 · Control-flow integrity** *(blocking)* — every decision's branches labeled and exhaustive; no dead ends, orphans, or unreachable nodes; every loop provably terminates.
`1` unlabeled branches / dead ends / orphans · `2` minor gaps (an unlabeled *No*, one dangling edge) · `3` all branches labeled, no orphans, one soft spot · `4` fully connected, exhaustive, all loops exit.

**3 · Decomposition & altitude** — consistent granularity; each box passes one-owner / one-exit / one-failure. *(defer depth → /pressure-test-diagram)*
`1` wild altitude mix, boxes hide subprocesses · `2` uneven in places · `3` mostly consistent, a few split/merge candidates · `4` uniform altitude, every box atomic.

**4 · Ownership & handoffs** — every step has a clear actor; cross-actor handoffs are explicit edges.
`1` no actors / ambiguous ownership · `2` actors present but handoffs implicit · `3` swimlaned, most handoffs explicit · `4` every step owned, every handoff an explicit edge with the artifact named.

**5 · Data & artifact traceability** — what flows between steps is named; sources are identifiable. *(defer depth → /interrogate-data-sources)*
`1` nothing on edges · `2` some artifacts named, sources unknown · `3` artifacts named on key edges · `4` artifacts + sources traceable, identifiers carry across boundaries.

**6 · Clarity & labeling** — verb-noun step names; decisions phrased as answerable questions; one term per concept.
`1` vague/noun-only labels, ambiguous decisions · `2` inconsistent naming · `3` clear names, answerable decisions · `4` crisp verb-noun throughout, consistent terms, unambiguous gateways.

**7 · Fit for purpose / right level** — altitude matches the stated audience and use.
`1` level clearly wrong for the use · `2` partially matched · `3` appropriate, minor mismatches · `4` pitched exactly for the audience.

**Blocking rule:** if dimension 1 or 2 scores `1`, the overall band caps at **Draft** no matter how the rest score. A map with holes in its paths or its wiring is not trustworthy, however polished.

## Overall band

Roll the scores into one band (describe *internal* quality only — external truth still needs a human):
- **Draft** — not yet trustworthy; structural gaps remain.
- **Usable** — fine for discussion; known gaps.
- **Solid** — dependable for building or onboarding.
- **Validated-ready** — only an external fidelity check remains.

## Output

1. **Purpose/audience** used (stated or assumed) — one line.
2. **Inventory** — the numbered `Box # | Name | Owner` table.
3. **Scorecard** — table: `Dimension | Level (1–4) | Evidence (cite box numbers/edges)`.
4. **Overall band** + the single blocking issue, if any.
5. **Top 3 fixes**, highest-leverage first, each concrete and actionable.
6. **Fidelity & confidence** — what you can't judge from the artifact: assumptions you had to make, boxes you couldn't interpret, and the specific things to confirm with someone who actually runs the process. This section is mandatory; a clean scorecard does not mean the map is true.
7. **Dig deeper** — which of the two deep-dive commands to run next, and why.

Be direct. Name the weakest dimension plainly. Don't pad the score to be encouraging — an inflated report card is worse than a harsh one, because someone will build on this map.
