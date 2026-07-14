# blueprint-model.json schema

This is the single source of truth that the renderer consumes. Produce it during
synthesis. All ids are short, stable, lowercase slugs.

```jsonc
{
  "meta": {
    "title": "Order-to-Cash — As-Is Service Blueprint",
    "process_domain": "order-to-cash",
    "generated_from": ["acme-discovery-2026-06-01.txt", "acme-ops-2026-06-08.txt"],
    "transcript_count": 2,
    "lane_model": "service_stack",     // "service_stack" | "actor_lanes"
    "confidence_notes": "Two calls with the ops team; finance steps inferred, low confidence.",
    "generated_at": "2026-07-13"
  },

  // Lanes rendered top-to-bottom. A lane with no "group" is a standalone
  // category (h1). A lane with "group" is an h2 sub-lane nested under the named
  // group; a group's members MUST be contiguous in this array. Group labels and
  // order live in "lane_groups". When any group exists, the renderer treats every
  // top-level entry as a labeled section: it inserts a thin, full-width header bar
  // (distinct color + heavier weight) above each group AND above each standalone
  // zone. A standalone zone repeats its label in the first-column row beneath its
  // bar; a group's bar sits above its h2 sub-lane rows.
  "lanes": [
    { "id": "customer_journey", "label": "Customer Journey" },
    { "id": "fs_employee", "label": "Employee actions", "group": "frontstage" },
    { "id": "fs_systems",  "label": "Systems",          "group": "frontstage" },
    { "id": "backstage",   "label": "Backstage actions" },
    { "id": "support",     "label": "Support processes" }
  ],
  "lane_groups": [
    { "id": "frontstage", "label": "Front Stage" }
  ],

  // Phases rendered left-to-right. Order here = horizontal order.
  "phases": [
    { "id": "intake",   "label": "Intake" },
    { "id": "qualify",  "label": "Qualification" },
    { "id": "fulfill",  "label": "Fulfillment" }
  ],

  "systems_of_record": [
    { "id": "sfdc",         "name": "Salesforce",        "type": "CRM" },
    { "id": "sap",          "name": "SAP ERP",           "type": "ERP" },
    { "id": "pricing_xls",  "name": "Pricing workbook",  "type": "Spreadsheet" },
    { "id": "email",        "name": "Email",             "type": "Comms" }
  ],

  "steps": [
    {
      "id": "s1",
      "phase": "intake",
      "lane": "customer_action",
      "order": 1,                       // order within the whole flow
      "name": "Customer emails purchase request",
      "description": "Customer sends a PO or request by email to the shared inbox.",
      "actor": "Customer",
      "systems": ["email"],             // ids from systems_of_record
      "variant": "core",                // "core" | "deviation"
      "support_count": 2,               // # of transcripts showing this step
      "occurs_in": ["acme-discovery-2026-06-01.txt", "acme-ops-2026-06-08.txt"],
      "pain_points": ["Requests arrive in inconsistent formats"],
      "evidence": [
        { "transcript": "acme-discovery-2026-06-01.txt", "ref": "rep describes inbox intake" }
      ],
      "confidence": "high"              // "high" | "medium" | "low"
    },

    // A DECISION NODE: kind:"decision" renders as a diamond in the flow instead of
    // a rectangle. Its incoming edge comes from "connections" like any step, but its
    // outgoing edges come from "branches" (each a labeled path to another step). A
    // decision is NOT given a sequence number. Use it for genuine core-path forks
    // where each outcome is a normal path (not an exception — those are deviations).
    {
      "id": "dq1",
      "phase": "qualify",
      "lane": "backstage",
      "order": 4.5,                     // fractional order slots it into the flow
      "kind": "decision",
      "name": "New or existing customer?",
      "actor": "Sales",
      "systems": ["sfdc"],
      "variant": "core",
      "branches": [
        { "label": "New",      "to": "s5" },
        { "label": "Existing", "to": "s7" }
      ]
    }
  ],

  // Sequence + handoff edges between steps (drives arrows in the render).
  // Do NOT add edges out of a decision node here — its "branches" handle those.
  "connections": [
    { "from": "s1", "to": "s2", "type": "sequence" },   // "sequence" | "handoff" | "rejoin"
    { "from": "s3", "to": "dq1", "type": "handoff" }
  ],

  // Deviations: alternate paths that branch off the core.
  "deviations": [
    {
      "id": "d1",
      "label": "Credit hold path",
      "trigger": "Account flagged for credit hold in ERP",
      "branch_from": "s3",              // core step where the branch starts
      "rejoin_at": "s6",                // core step where it rejoins (or null)
      "steps": ["dv1", "dv2"],          // ids of steps with variant:"deviation"
      "occurs_in": ["acme-ops-2026-06-08.txt"],
      "frequency_note": "Seen in 1 of 2 calls; described as ~15% of orders",
      "impact": "Adds 2–3 days; manual finance review"
    }
  ]
}
```

## Validate before rendering

`scripts/render.py` runs these automatically; if splicing by hand, check them
yourself. Errors (must fix): every step's `lane` exists in `lanes`; every step's
`phase` exists in `phases`; every id in a step's `systems` exists in
`systems_of_record`; every lane `group` exists in `lane_groups`; every
deviation's `branch_from`, `rejoin_at`, and `steps[]` reference real steps;
every decision branch `to` references a real step; every connection endpoint
exists. Warnings (should fix): deviations without a `trigger`; deviation
`steps[]` entries not marked `variant: "deviation"`; decisions without
`branches`.

## Field notes

- **Category color (`color` on a lane or lane_group).** Each top-level zone carries
  a `color`; the card renders a color-coded header in that color and the lightbox
  header matches. Sub-lanes inherit their group's color. Suggested mapping:
  Customer Journey `#D07B45`, Front Stage `#587DA8`, Backstage `#8A8177`, Support
  `#7E8D80`; decision diamonds are always ember orange. These are the categories the card
  design's "user-assigned color" system expects.
- **Optional card fields on a step.** The card + lightbox show these when present
  and silently omit them otherwise: `description`, `duration` (Time), `channel`,
  `evidence` (string or `[{ref}]`, rendered as a link), `tags` (string[]),
  `pain_points` (string or string[]), `success_metric`. `systems` render as the
  "Backstage systems" chips in the card's inline-expand and the lightbox.


- **lane_model** switches the whole vertical axis. `service_stack` =
  customer/frontstage/backstage/support. `actor_lanes` = arbitrary org lanes
  (Customer, Sales, Ops, Finance, IT…). The `lanes` array defines whichever set
  is in use; steps reference lanes by id either way.
- **variant** on a step is the atomic core/deviation flag. **deviations[]**
  groups deviation steps into a named branch with a trigger and rejoin point —
  this is what lets the render draw a clean branch rather than scattered flags.
- **support_count / occurs_in** are how core-ness is justified. Keep them honest;
  they drive both rendering emphasis and user trust.
- **evidence.ref** is a short paraphrase pointer, never a long verbatim quote.
- Unknown/inferred values: set `confidence: "low"` and explain in
  `meta.confidence_notes` rather than omitting the step.
