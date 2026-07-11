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

### Claude Code

**Recommended — Agent Skills** (auto-activate + `/name` invocation):
```
cp -r skills/* ~/.claude/skills/          # personal, all projects
# or, per-project:
cp -r skills/* .claude/skills/
```

**Legacy — slash commands** (single-file, still fully supported):
```
cp claude-code/commands/*.md ~/.claude/commands/
```
Invoke with `/pressure-test-diagram`, `/interrogate-data-sources`, `/assess-diagram-quality`.

### GitHub Copilot

**Prompt files** (VS Code, Visual Studio 17.10+, JetBrains) — invoke with `/name` in Copilot Chat:
```
mkdir -p .github/prompts && cp github-copilot/prompts/*.prompt.md .github/prompts/
```

**Agent Skills** — the `skills/` folder is the same open standard Copilot uses; auto-activates on intent:
```
mkdir -p .github/skills && cp -r skills/* .github/skills/
```

### ChatGPT

The `chatgpt/` files are ready to paste — no frontmatter. Two ways to use them:
- **Custom GPT:** GPT Builder → Configure → paste a skill's full text into **Instructions**. The GPT will ask for the diagram, then run the skill.
- **Project:** create a Project → paste a skill into the project **Instructions** field.

(ChatGPT's account-level Custom Instructions fields cap at ~1,500 characters — too small for these. Use a Custom GPT or Project instead.)

### Microsoft Copilot Studio

The `copilot-studio/` files carry YAML frontmatter (`name`, `description`) followed by the instruction body — the convention for declarative agents. To install: create an agent in Agent Builder (or `m365.cloud.microsoft/chat/agent/new`), copy `name` and `description` from the frontmatter into the agent's Name and Description fields, and paste the body (everything below the closing `---`) into **Instructions**. All three bodies are sized under the ~8,000-character instruction limit.

## Formats at a glance

| Platform | Folder | File form | Input mechanism |
|----------|--------|-----------|-----------------|
| Claude Code (skills) | `skills/` | `<name>/SKILL.md` | `$ARGUMENTS` |
| Claude Code (legacy) | `claude-code/commands/` | `<name>.md` | `$ARGUMENTS` |
| GitHub Copilot | `github-copilot/prompts/` | `<name>.prompt.md` | `${input:diagram}` |
| ChatGPT | `chatgpt/` | `<name>.md` (paste-in) | user provides in chat |
| Copilot Studio | `copilot-studio/` | `<name>.md` — YAML frontmatter (`name`, `description`) + body | user provides in chat |

`SKILL.md` is an open standard shared by Claude Code and GitHub Copilot, so the `skills/` folder works in both.

## Editing

`skills/<name>/SKILL.md` is the source of truth. Edit there, then regenerate every other variant:
```
python build.py
```
Don't hand-edit the generated folders — `build.py` overwrites them.

## License

MIT — see [LICENSE](LICENSE).
