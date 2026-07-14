# Theme Handoff: "Warm Gray Ember" — Service Blueprint Generator

## What this is
The chosen visual theme for the service blueprint skill's HTML output. `service-blueprint-template.html` is the full working app with the theme already applied — same markup, JS, and behavior as the current skill template; **only color values changed**. The skill should inherit this file as its new template (the `BLUEPRINT_MODEL` markers are intact — replace only that object, as before).

## Theme intent
Cleaner, softer, warmer. Warm paper neutrals; muted slate blue for core/frontstage; warm grays for backstage; gray-sage for support; ember orange as the accent for customer journey, decisions, and deviations. Orange = "a human chose / something diverged"; blue-gray = machinery.

## Token map (semantic role → hex)

### Neutrals (CSS vars in `:root`)
- `--paper` page background: `#FAF9F7`
- `--panel` cards/sidebar: `#FFFFFF`
- `--ink` primary text: `#2E2A26`
- `--ink-soft` secondary text: `#6E675F`
- `--grid` grid/hairlines: `#EAE6E0`
- `--lane-band` lane tint: `#F2EFEA`
- `--chip` chip fill: `#F0EDE7`, `--chip-ink`: `#55504A`
- Notes/callout text: `#4A423A`

### Core & deviation (CSS vars)
- `--core`: `#587DA8` · `--core-soft`: `#EBF1F6` · `--core-line`: `#C2D3E2`
- `--dev`: `#B06A31` · `--dev-soft`: `#F8ECDF` · `--dev-line`: `#E3BE93`

### Lane category colors (in `BLUEPRINT_MODEL` lane/group `color` fields + JS fallback)
- Front Stage: `#587DA8`
- Backstage actions: `#8A8177`
- Support processes: `#7E8D80`
- Customer Journey: `#D07B45`
- JS fallback color (`catOf`): `#587DA8`

### Decision diamond
- Chip/fill accent: `#D07B45` · border: `#E8C9A8` · text: `#A8683C` · hover wash: `#F8EFE4`

### Semantic
- Evidence link: `#56789A`
- Pain band red: `#A85043`
- Minimap: bg `#2E2A26`, core blip `#9BB3CC`, deviation blip `#DFA579`

## How to inherit in the skill
1. Replace the skill's HTML template with `service-blueprint-template.html`.
2. When generating `blueprint-model.json`, emit the lane category colors above (they live in the model, not the CSS).
3. If new categories are added, derive colors in the same register: muted, ~40–55% lightness, low chroma; reserve saturated ember orange for journey/decision/deviation roles.

## Provenance
Derived from `service-blueprint_2.html` (the skill's current output) via a pure color remap — diff the two files to see every substitution.
