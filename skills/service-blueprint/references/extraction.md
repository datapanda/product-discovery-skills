# Phase 1 — Extraction (per transcript)

Process each transcript **independently** and produce one `extract-<name>.json`.
Do not try to reconcile transcripts yet — that is synthesis (Phase 2). Keeping
extractions separate is what makes core-vs-deviation detection possible later.

## Goal

For a single transcript, produce an ordered list of process steps. For each step
capture: what happens, who does it, which systems of record are touched, and any
conditional/exception language attached to it.

## Procedure

1. **Read the whole transcript once** before extracting. Identify the process
   being described and roughly where it starts and ends. Note the speakers and
   which org/role each represents. **Separate the interviewer from the
   interviewee(s):** the interviewer's questions ("walk me through," "what
   happens next?") are sequencing cues, not process steps. Steps come from the
   interviewee's narration. If a speaker describes a step performed by a team
   they're not on, mark it second-hand (lower `confidence`) in that step's
   `notes`/`ref`.
2. **Walk the narrated process in order.** Each time an action, decision, or
   handoff is described, create a step. A step is a unit of work with an actor
   and (usually) a system. Merge filler/small talk; split when two distinct
   actions are bundled in one sentence.
3. **Tag the actor and lane.** Who performs it? Is it customer-visible
   (frontstage) or internal (backstage), or a supporting system action? If using
   actor lanes instead, assign the org lane.
4. **Tag systems of record.** Capture every tool named or implied: ERP (SAP,
   NetSuite, Oracle), CRM (Salesforce, HubSpot), spreadsheets/workbooks, email,
   ticketing (Zendesk, ServiceNow, Jira), shared drives, homegrown/internal
   apps. Note **handoffs where the system changes** — these are friction hot
   spots worth flagging.
5. **Capture conditional language as deviation candidates.** Flag any step or
   branch introduced by: "usually / normally / typically," "sometimes /
   occasionally / every now and then," "if / when / unless," "the exception is,"
   "for <segment> customers we instead," "if it's urgent/large/international,"
   "when something's wrong we…," "then it goes back to." Mark these
   `deviation_candidate: true` and record the trigger phrase.
6. **Capture pain points** stated or implied (rework, waiting, manual copying,
   duplicate entry, "that's the annoying part").
7. **Capture card details opportunistically.** The rendered card can show more
   than name+actor; when the transcript states them, record per step: a one-
   sentence `description`, `duration` ("~2 min", "2–3 days"), `channel` (phone,
   email, app, portal, in person), a `success_metric` if one is stated, and 1–3
   short `tags`. Do not invent these — omit what wasn't said.

## Output: extract-<name>.json

```jsonc
{
  "transcript": "acme-ops-2026-06-08.txt",
  "process_guess": "order-to-cash",
  "speakers": [
    { "name": "Dana", "role": "Ops lead", "org": "customer" }
  ],
  "steps": [
    {
      "seq": 1,
      "name": "Rep logs request in Salesforce",
      "actor": "Sales rep",
      "lane_guess": "frontstage",
      "systems": ["Salesforce"],
      "deviation_candidate": false,
      "trigger": null,
      "pain_points": [],
      "ref": "short paraphrase pointer, not a long quote"
    },
    {
      "seq": 2,
      "name": "Manual credit check in ERP",
      "actor": "Finance",
      "lane_guess": "backstage",
      "systems": ["SAP ERP"],
      "deviation_candidate": true,
      "trigger": "only when order value > $50k",
      "pain_points": ["Waits on finance; no SLA"],
      "ref": "Dana: big orders get a finance check"
    }
  ],
  "systems_seen": ["Salesforce", "SAP ERP", "Email"],
  "confidence": "medium",
  "notes": "No finance rep on the call; finance steps are second-hand."
}
```

## Guidance

- Normalize system names loosely now (e.g. "SFDC" → "Salesforce"); final
  canonical ids are assigned in synthesis.
- Prefer more, smaller steps over few mega-steps — synthesis can merge, but it
  can't split what you didn't separate.
- Don't force customer-facing framing onto internal-only processes. If the
  transcript never mentions the end customer, `customer_action` may be empty and
  actor lanes may fit better — record that observation in `notes`.
- Keep `ref` short and paraphrased. The evidence trail matters; verbatim bulk
  does not.
