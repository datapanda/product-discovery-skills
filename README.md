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

These follow the [Agent Skills](https://agentskills.io) open standard — one `<name>/SKILL.md` folder per skill — so they work across several agents. Skills do **not** sync between surfaces; install them wherever you want to use them.

**Claude Code** — copy the folders in; no upload step. Invoke with `/service-blueprint` (etc.), or just describe the task and let them auto-activate.

```
cp -r skills/* ~/.claude/skills/     # personal — all your projects
cp -r skills/* .claude/skills/       # project — checked in for the team
```

They can also ship inside a [Claude Code plugin](https://code.claude.com/docs/en/plugins) for one-command install from a marketplace.

**Claude.ai / Claude Desktop** — zip a skill folder and upload it under **Settings → Features → Skills**. Requires a Pro, Max, Team, or Enterprise plan with code execution ("Create and edit files") enabled; uploaded skills are per-user, not org-wide.

```
cd skills && zip -r service-blueprint.zip service-blueprint
```

**Claude API** (and Claude on AWS / Microsoft Foundry) — upload via the `/v1/skills` endpoint, then reference the returned `skill_id` in the `container` parameter of a request that uses the [code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) (beta header `skills-2025-10-02`). Shared workspace-wide.

**GitHub Copilot** — Copilot reads the same standard; drop the folders in `.github/skills/` (repo) or `~/.copilot/skills/` (personal). Works in VS Code, JetBrains, the Copilot CLI, and the cloud agent.

**Any other agent** — the format is just Markdown. Point the agent at a `SKILL.md` and it has everything it needs.

> **Sandbox-friendly.** Every skill here is Markdown plus — for service-blueprint — one stdlib-only Python script and a fully self-contained HTML template. No network calls, no package installs, so they run as-is inside the locked-down API and claude.ai containers.

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
