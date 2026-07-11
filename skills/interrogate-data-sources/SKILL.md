---
name: interrogate-data-sources
description: Interrogate a process diagram's data provenance — for each box, identify which system every datum comes from, tag the box with its data system(s), and surface cross-system ID mismatches and unknowns.
argument-hint: [path to a mermaid/diagram file, or paste a description of the flow]
allowed-tools: Read
model: opus
---

You are auditing a process diagram for **data provenance**: for every step, exactly where does each piece of data come from, is it authoritative, and does it stay consistent as it crosses system boundaries.

## Input

The diagram to review: $ARGUMENTS

If `$ARGUMENTS` is a file path, read it. If it's a pasted description, work from that. If it's an attached image, read the image. If no diagram is present, ask for one and stop.

## Core principle

Never guess a data source. If you cannot determine where a datum comes from with confidence, mark it `UNKNOWN` and put it in the **Questions** section. A flagged unknown is useful; an invented source is a bug waiting to happen.

## The source taxonomy — check every category

For each box, an identifier or field could originate from any of these. Walk the list so you don't only catch the systems already named in the diagram:

- **Systems of record** — CRM (e.g. Salesforce), transactional/app DB, ERP/billing (Stripe, NetSuite, Zuora), identity/auth (Okta, Auth0, Cognito), CMS.
- **Access mechanisms** — direct DB query, internal API/microservice, external third-party API (payment, shipping, tax, address/geo), message queue or event stream (Kafka/SQS/SNS — event-carried state), webhook/callback (pushed in), object/file storage (S3, uploads), search index (Elasticsearch/Algolia).
- **Easy-to-forget sources** — cache (Redis/CDN — authoritative or a stale copy?), read replica / denormalized copy, config & feature flags (LaunchDarkly, env vars), secrets store, **human input** (a form, a CSR keying data, an approval), **computed-in-flow values** (derived by this box, stored nowhere — provenance is the box itself), **context passed in from a prior step** (in-memory, not re-fetched — may be stale vs. source), ML/inference service output, audit/log sink (write-only), session/state store.

## Do not skip the inventory

Build a numbered table of **every** box. For each, list what it **reads** and what it **writes**. If you can't name what a box reads or writes, that gap is a finding — record it. Work off this explicit inventory; do not reason from a general impression of the diagram.

## Per-datum interrogation

For each datum a box reads or writes, answer:

1. **Origin** — which system is the system of record? Where was this datum born?
2. **Access path** — how does this box get it? Live fetch, passed-in, cached, event payload, human-entered?
3. **Authority** — is the box reading the authoritative source, or a copy/replica/cache/denormalized field?
4. **Freshness** — could it be stale? Roughly what staleness window?
5. **Identifier crossing** — does an ID here map to a *different* ID in another system? (An order ID is often an internal order UUID *and* a Salesforce record ID *and* a Stripe charge ID *and* a WMS/fulfillment ID — each distinct.) Flag every boundary an identifier crosses.
6. **Read/write direction** — read, write, or both? Where does a write land, and must it propagate elsewhere?
7. **Absence/failure** — what happens if the source is down or the datum is missing?

## Tagging vocabulary

Tag every box with its data system(s), using a consistent shorthand with read/write direction:

- System: `SF` (Salesforce), `DB:<table/service>`, `WAREHOUSE`, `BILLING:<vendor>`, `AUTH`, `API:<name>` (external), `SVC:<name>` (internal service), `CACHE`, `EVENT:<topic>`, `SEARCH`, `STORAGE`, `CONFIG`, `HUMAN`, `COMPUTED`, `INHERITED` (passed from prior step), `UNKNOWN`.
- Direction suffix: `:r` read, `:w` write, `:rw` both. Example: `SF:r`, `DB:orders:rw`, `API:shipping:r`.

A box may carry several tags. `COMPUTED` and `INHERITED` are legitimate tags — use them rather than forcing a system where none applies.

## Output

1. **Inventory & interrogation table** — `Box # | Reads | Writes | System tag(s) | Authority/freshness risk`.
2. **Tagged diagram** — return the diagram with tags appended to each node label. If the input was mermaid, emit updated mermaid, e.g. `B["Look up order<br/>(SF:r, DB:orders:r)"]`. Otherwise emit a clean `Box → tags` list.
3. **Identifier cross-boundary map** — a table of each identifier and what it maps to in every system it touches (`internal order UUID ↔ SF Order__c ↔ Stripe pi_… ↔ WMS ref`). This is the highest-value output; be thorough.
4. **Blind spots** — stale-cache reads, authoritative writes with no propagation, data fetches with no failure path, ID translations with no visible mapping step.
5. **Questions for you** — every `UNKNOWN` or ambiguous source, as a specific, answerable question (e.g. "Box 4 reads customer tier — live from Salesforce, or the denormalized copy in the app DB?"). Do not resolve these by guessing.

Be direct and specific. Reference boxes by number. Where provenance is clear, tag it and move on; spend the effort on the boundaries and the unknowns.
