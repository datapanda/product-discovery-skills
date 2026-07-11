# Diagram Quality Skills

Three AI skills for **pressure-testing process diagrams** — physical processes or digital experiences. They exist to get a process that lives in people's heads captured accurately and at the right level of detail.

| Skill | What it does |
|-------|--------------|
| **assess-diagram-quality** | Report card. Scores a diagram across seven quality dimensions, gives an overall band, and separates what it can judge from the artifact from what a human must verify. Start here. |
| **pressure-test-diagram** | Decomposition scalpel. Flags steps that hide complexity or add noise, then emits a before/after inventory and a fix checklist. |
| **interrogate-data-sources** | Provenance scalpel. For each box, identifies which system every datum comes from, tags the box, and maps identifiers across system boundaries. |

## Design principles

- **Audit, not fabricate.** Where a data source, owner, or routing can't be determined from the diagram, the skills flag it as an open question rather than inventing an answer.
- **One shared numbered inventory.** All three build the same `Box #` inventory first, so running all three on one diagram lines up box-for-box (box 15 means the same thing in every report).
- **Internal quality ≠ external truth.** A clean score means the artifact is sound, not that it matches reality. Every assessment ends by naming what a human who runs the process still has to confirm.

## Install

These are [Claude Code Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) — one `<name>/SKILL.md` per skill, auto-activating on intent and invocable with `/name`.

```
cp -r skills/* ~/.claude/skills/          # personal, all projects
# or, per-project:
cp -r skills/* .claude/skills/
```

Invoke with `/assess-diagram-quality`, `/pressure-test-diagram`, or `/interrogate-data-sources`, or just describe a diagram and let them auto-activate.

`SKILL.md` is an open standard also read by GitHub Copilot, so the same `skills/` folder works there via `.github/skills/`.

## Repository layout

```
skills/
  assess-diagram-quality/SKILL.md
  interrogate-data-sources/SKILL.md
  pressure-test-diagram/SKILL.md
```

Each `SKILL.md` carries YAML frontmatter (`name`, `description`, `argument-hint`, `allowed-tools`, `model`) followed by the skill instructions. Edit these files directly — they are the source of truth.

## License

MIT — see [LICENSE](LICENSE).
