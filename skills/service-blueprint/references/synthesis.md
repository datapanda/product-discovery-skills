# Phase 2 — Synthesis (across transcripts)

Merge the independent `extract-<name>.json` files into one
`blueprint-model.json`. This is where the common core process and its deviations
are determined. Read `blueprint-schema.md` for the exact output shape.

## Step A — Canonicalize systems of record

Collect every `systems_seen` value across extractions and collapse synonyms into
one canonical list with ids and types (CRM, ERP, Spreadsheet, Ticketing, Comms,
Internal app, Other). Example: "SFDC," "Salesforce.com," "the CRM" → one entry
`sfdc`. Every step's `systems` will reference these ids.

## Step B — Align steps into a canonical sequence

You are matching steps that mean the same thing across transcripts even when
worded differently ("logs it in Salesforce" ≈ "creates the opportunity record").

1. Cluster equivalent steps across transcripts by their action + actor + system.
2. Give each cluster one canonical step with a clean name.
3. Record `occurs_in` (which transcripts) and `support_count` (how many).
4. Order the canonical steps into one end-to-end sequence. Where transcripts
   disagree on order, prefer the order seen most often and note the conflict.
5. Group steps under phases (coarse stages). Infer phase boundaries from natural
   breaks (intake → work → resolution/close).

## Step C — Decide core vs deviation

**First determine the coverage pattern**, because it changes the rule:

- **Overlapping coverage** — interviewees describe the *same* slice of the
  process (e.g. three intake agents). Frequency is meaningful: a step in most
  transcripts is core; a step in few is suspect.
- **Role-segmented (complementary) coverage** — interviewees each own a
  *different* slice (e.g. intake → adjuster → payments). Most legitimate core
  steps will appear in only ONE transcript because only one role can describe
  them. Frequency is NOT meaningful here — do not demote a step to deviation
  just because a single transcript shows it.

Tell-tale signs of role-segmented coverage: each interviewee disclaims the
others' segments ("you'd have to ask them," "I have no visibility into
payments"), the narrated slices chain end-to-end with little overlap, and
handoffs between the roles are described from both sides.

**For overlapping coverage**, apply the frequency rule: core if the step appears
in all or a strong majority of transcripts (default threshold
`support_count / N >= 0.6`) AND sits on the main narrated path — treated as
guidance, not gospel.

**For role-segmented coverage**, core-ness rests on *role ownership +
narration*: a step is core if it's on the main path narrated by the role that
owns that segment. Cross-transcript corroboration still matters where segments
touch — handoffs, shared holds, and escalations described by two roles get
`support_count: 2` and higher confidence. Say which pattern you used (and why)
in `meta.confidence_notes`.

**Either way**, a step is a deviation if it is introduced by conditional
language (`deviation_candidate: true`), or represents rework / an alternate
branch / an escalation — regardless of how many transcripts mention it.

Single-transcript case: there is no cross-call frequency, so lean entirely on
conditional language. The main path = core; every `deviation_candidate` becomes
a deviation with `support_count: 1` and `confidence` no higher than medium.

## Step D — Assemble deviations into named branches

Scattered deviation flags are hard to read. Group them:

1. For each deviation, identify its **trigger** (the condition), the **core step
   it branches from** (`branch_from`), the deviation steps, and where it
   **rejoins** the core (`rejoin_at`, or `null` if it terminates).
2. Give the branch a human name ("Credit hold path," "Expedite / rush order,"
   "Missing PO rework loop").
3. Record `occurs_in` and a `frequency_note` in plain language ("1 of 3 calls;
   described as ~15% of orders"). Quantify only what was actually said.
4. If a deviation has no stated trigger, go back to the transcript. If truly
   none exists, name the best-supported condition and mark `confidence: "low"`.
   "It depends" is not a trigger.

## Step E — Build connections

Emit `connections` edges: `sequence` along the core path, `handoff` where the
system of record or owning team changes (worth visually emphasizing), and
`rejoin` where a deviation returns to the core.

## Step F — Fill meta and confidence

- **Auto-pick `lane_model`.** Decide with this test, then justify in
  `confidence_notes`:
  - Choose `service_stack` if the interviews describe an **end customer who
    experiences the service** (there are real `customer_action` steps and a
    line of visibility worth drawing). Lanes: customer_action, frontstage,
    backstage, support.
  - Choose `actor_lanes` if it's an **internal cross-team workflow** with no
    single customer journey. Derive the lanes from the actual teams/roles named
    across transcripts (e.g. Customer, Sales, Ops, Finance, IT) — include only
    lanes that actually appear, in the order work flows through them.
  - Tie-breaker: if a customer appears only at the very start/end (submits a
    request, receives a result) but the body is internal handoffs, prefer
    `actor_lanes` with a "Customer" lane at the top.
- Summarize what's solid vs inferred. Call out any step present in zero
  transcripts that you added by inference (ideally none).

## Anti-patterns to avoid

- Don't over-merge: two similarly named steps in different systems are usually
  two steps, not one.
- Don't promote a one-off complaint to a formal deviation branch unless it's a
  real alternate path.
- Don't let the happy path swallow a common exception just because it's messy —
  frequent exceptions are the most valuable thing a blueprint surfaces.
