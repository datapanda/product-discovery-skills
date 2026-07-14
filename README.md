# Process Design Skills

AI skills for **capturing and pressure-testing how work actually happens**. Business processes live in people's heads; these skills turn them into accurate, inspectable artifacts — and audit the artifacts that already exist. Some skills generate (transcripts → service blueprint), others assess (score, decompose, and trace an existing diagram). The collection grows over time.

## The skills

| Skill | Type | What it does |
|-------|------|--------------|
| [**service-blueprint**](skills/service-blueprint/) | Generate | Turns discovery-call transcripts into an interactive HTML service blueprint: swimlanes, systems of record, the core happy path vs. deviations, decision points, and pain points — with print/PDF output. |
| [**assess-diagram-quality**](skills/assess-diagram-quality/) | Assess | Report card. Scores a diagram across seven quality dimensions, gives an overall band, and separates what it can judge from the artifact from what a human must verify. Start here for existing diagrams. |
| [**pressure-test-diagram**](skills/pressure-test-diagram/) | Assess | Decomposition scalpel. Flags steps that hide complexity or add noise, then emits a before/after inventory and a fix checklist. |
| [**interrogate-data-sources**](skills/interrogate-data-sources/) | Assess | Provenance scalpel. For each box, identifies which system every datum comes from, tags the box, and maps identifiers across system boundaries. |

They compose: generate an as-is blueprint from transcripts with **service-blueprint**, then run the assessment skills against it — or against any process diagram you already have.

## Design principles

- **Audit, not fabricate.** Where a data source, owner, or step can't be determined from the source material, the skills flag it as an open question (or lower its confidence) rather than inventing an answer.
- **Evidence-grounded.** service-blueprint cites which transcript supports every step and tracks second-hand hearsay; the assessment trio builds one shared numbered `Box #` inventory so their reports line up box-for-box.
- **Internal quality ≠ external truth.** A clean artifact means the artifact is sound, not that it matches reality. Every output names what a human who runs the process still has to confirm.

## Install

These are [Claude Code Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) — one `<name>/SKILL.md` per skill, auto-activating on intent and invocable with `/name`.

```
cp -r skills/* ~/.claude/skills/          # personal, all projects
# or, per-project:
cp -r skills/* .claude/skills/
```

Invoke with `/service-blueprint`, `/assess-diagram-quality`, `/pressure-test-diagram`, or `/interrogate-data-sources`, or just describe the task and let them auto-activate.

`SKILL.md` is an open standard also read by GitHub Copilot, so the same `skills/` folder works there via `.github/skills/`.

## Repository layout

```
skills/
  assess-diagram-quality/SKILL.md
  interrogate-data-sources/SKILL.md
  pressure-test-diagram/SKILL.md
  service-blueprint/
    SKILL.md                  # entry point + pipeline overview
    references/               # extraction, synthesis, schema, rendering docs
    assets/blueprint-template.html
    examples/blueprint-model.example.json
    scripts/render.py         # stdlib-only validate + render
```

Each `SKILL.md` carries YAML frontmatter (`name`, `description`, and optionally `argument-hint`, `allowed-tools`, `model`) followed by the skill instructions. Edit these files directly — they are the source of truth.

## License

MIT — see [LICENSE](LICENSE).
