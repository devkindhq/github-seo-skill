#!/usr/bin/env python3
"""Validate the skill, its evals, the plugin manifests and internal markdown links. Stdlib only."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def err(msg):
    errors.append(msg)


for skill_md in sorted(ROOT.glob("skills/*/SKILL.md")):
    d = skill_md.parent
    m = re.match(r"^---\n(.*?)\n---\n", skill_md.read_text(), flags=re.S)
    if not m:
        err(f"{skill_md}: missing frontmatter")
        continue
    fm = dict(
        line.split(":", 1) for line in m.group(1).splitlines() if ":" in line and not line.startswith(" ")
    )
    fm = {k.strip(): v.strip() for k, v in fm.items()}
    name = fm.get("name", "")
    if name != d.name:
        err(f"{skill_md}: name '{name}' must equal directory '{d.name}'")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        err(f"{skill_md}: name must be lowercase-hyphenated")
    desc = fm.get("description", "")
    if not desc:
        err(f"{skill_md}: description is empty")
    elif len(desc) > 1024:
        err(f"{skill_md}: description is {len(desc)} chars, limit 1024")

    evals = d / "evals" / "evals.json"
    if not evals.exists():
        err(f"{d}: missing evals/evals.json")
    else:
        cases = json.loads(evals.read_text()).get("cases", [])
        kinds = {c.get("type") for c in cases}
        for needed in ("should_trigger", "should_not_trigger", "quality"):
            if needed not in kinds:
                err(f"{evals}: no '{needed}' cases")
        for c in cases:
            if c.get("type") == "quality" and not c.get("expected_behavior"):
                err(f"{evals}: quality case without expected_behavior: {c.get('prompt')}")

for manifest in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"):
    try:
        json.loads((ROOT / manifest).read_text())
    except Exception as e:  # noqa: BLE001
        err(f"{manifest}: {e}")

link = re.compile(r"\]\((?!https?:|#|mailto:)([^)#\s]+)")
for md in ROOT.rglob("*.md"):
    if ".git" in md.parts:
        continue
    for target in link.findall(md.read_text()):
        if not (md.parent / target).exists():
            err(f"{md.relative_to(ROOT)}: broken link '{target}'")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("ok")
