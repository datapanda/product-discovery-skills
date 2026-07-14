#!/usr/bin/env python3
"""Render a service blueprint: splice blueprint-model.json into the HTML template.

Usage:
    python3 render.py <blueprint-model.json> [template.html] [output.html]

Defaults: template = ../assets/blueprint-template.html (relative to this script),
output = service-blueprint.html in the current directory.

Zero dependencies (stdlib only). Validates the model before rendering and prints
any referential-integrity problems it finds. If Python is unavailable, do the
same splice by hand: open the template, find the block between
`/* === BLUEPRINT_MODEL:START === */` and `/* === BLUEPRINT_MODEL:END === */`,
and replace ONLY the `const BLUEPRINT_MODEL = {...};` statement with your model.
Never edit anything outside the markers.
"""
import json, re, sys, os

START = "/* === BLUEPRINT_MODEL:START ==="
END = "/* === BLUEPRINT_MODEL:END === */"


def validate(m):
    errs, warns = [], []
    lanes = {l.get("id") for l in m.get("lanes", [])}
    groups = {g.get("id") for g in m.get("lane_groups", [])}
    phases = {p.get("id") for p in m.get("phases", [])}
    systems = {s.get("id") for s in m.get("systems_of_record", [])}
    steps = {s.get("id"): s for s in m.get("steps", [])}

    for req in ("meta", "lanes", "phases", "steps"):
        if not m.get(req):
            errs.append(f"missing or empty required section: {req}")
    for l in m.get("lanes", []):
        if l.get("group") and l["group"] not in groups:
            errs.append(f"lane '{l.get('id')}' references unknown group '{l['group']}'")
    for s in m.get("steps", []):
        sid = s.get("id", "?")
        if s.get("lane") not in lanes:
            errs.append(f"step '{sid}' has unknown lane '{s.get('lane')}'")
        if s.get("phase") not in phases:
            errs.append(f"step '{sid}' has unknown phase '{s.get('phase')}'")
        for sysid in s.get("systems", []):
            if sysid not in systems:
                errs.append(f"step '{sid}' references unknown system '{sysid}'")
        if s.get("kind") == "decision":
            for br in s.get("branches", []):
                if br.get("to") not in steps:
                    errs.append(f"decision '{sid}' branch '{br.get('label')}' -> unknown step '{br.get('to')}'")
            if not s.get("branches"):
                warns.append(f"decision '{sid}' has no branches")
    for d in m.get("deviations", []):
        did = d.get("id", "?")
        if d.get("branch_from") not in steps:
            errs.append(f"deviation '{did}' branch_from unknown step '{d.get('branch_from')}'")
        if d.get("rejoin_at") and d["rejoin_at"] not in steps:
            errs.append(f"deviation '{did}' rejoin_at unknown step '{d.get('rejoin_at')}'")
        for sid in d.get("steps", []):
            if sid not in steps:
                errs.append(f"deviation '{did}' lists unknown step '{sid}'")
            elif steps[sid].get("variant") != "deviation":
                warns.append(f"deviation '{did}' step '{sid}' is not variant:'deviation'")
        if not d.get("trigger"):
            warns.append(f"deviation '{did}' has no trigger ('it depends' is not a trigger)")
    for c in m.get("connections", []):
        if c.get("from") not in steps or c.get("to") not in steps:
            errs.append(f"connection {c.get('from')} -> {c.get('to')} references unknown step(s)")
    return errs, warns


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    model_path = sys.argv[1]
    here = os.path.dirname(os.path.abspath(__file__))
    template_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "..", "assets", "blueprint-template.html")
    out_path = sys.argv[3] if len(sys.argv) > 3 else "service-blueprint.html"

    model = json.load(open(model_path, encoding="utf-8"))
    errs, warns = validate(model)
    for w in warns:
        print(f"WARN: {w}")
    if errs:
        for e in errs:
            print(f"ERROR: {e}")
        print(f"\n{len(errs)} error(s) — fix the model before rendering.")
        sys.exit(1)

    tpl = open(template_path, encoding="utf-8").read()
    js = "const BLUEPRINT_MODEL = " + json.dumps(model, ensure_ascii=False) + ";"
    pat = re.compile(re.escape(START) + r".*?\*/\n.*?\n" + re.escape(END), re.S)
    marker_block = None
    mobj = re.search(re.escape(START) + r"(.*?)\*/", tpl, re.S)
    if not mobj:
        print("ERROR: template is missing the BLUEPRINT_MODEL markers.")
        sys.exit(1)
    replacement = START + mobj.group(1) + "*/\n" + js + "\n" + END
    out, n = pat.subn(replacement, tpl)
    if n != 1:
        print(f"ERROR: expected exactly 1 marker block, found {n}.")
        sys.exit(1)
    open(out_path, "w", encoding="utf-8").write(out)
    print(f"OK: wrote {out_path}  ({len(model.get('steps', []))} steps, "
          f"{len(model.get('deviations', []))} deviations, "
          f"{len(model.get('systems_of_record', []))} systems)")


if __name__ == "__main__":
    main()
