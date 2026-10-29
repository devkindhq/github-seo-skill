#!/usr/bin/env python3
"""Read-only GitHub repo SEO audit. Usage: check_repo_seo.py [owner/repo]

Needs the GitHub CLI (`gh`) logged in. Makes no changes. Exits 1 if any check fails.
"""
import base64
import json
import re
import subprocess
import sys

results = []


def gh(*args):
    out = subprocess.run(["gh", *args], capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"gh {' '.join(args)} failed: {out.stderr.strip()}")
    return out.stdout


def record(level, name, detail):
    results.append((level, name, detail))


target = sys.argv[1:2]
meta = json.loads(
    gh(
        "repo", "view", *target, "--json",
        "nameWithOwner,name,description,homepageUrl,licenseInfo,repositoryTopics,isPrivate",
    )
)
slug = meta["nameWithOwner"]
name = meta["name"]

# Description
desc = (meta["description"] or "").strip()
if not desc:
    record("FAIL", "description", "empty. This is the About text and the search snippet.")
elif len(desc) > 350:
    record("FAIL", "description", f"{len(desc)} chars, over the 350 limit")
elif len(desc) > 120:
    record("WARN", "description", f"{len(desc)} chars, may truncate in results (aim for 120 or fewer)")
else:
    record("PASS", "description", f"{len(desc)} chars")

# Topics
topics = [t["name"] for t in (meta["repositoryTopics"] or [])]
if not topics:
    record("FAIL", "topics", "none set")
elif len(topics) < 5:
    record("WARN", "topics", f"{len(topics)} set ({', '.join(topics)}). Add accurate ones.")
else:
    record("PASS", "topics", f"{len(topics)} set")

# Homepage and license
if meta["homepageUrl"]:
    record("PASS", "homepage", meta["homepageUrl"])
else:
    record("WARN", "homepage", "empty. Point it at the canonical write-up.")
lic = meta["licenseInfo"]
if lic and lic.get("key") != "other":
    record("PASS", "license", lic["name"])
else:
    record("FAIL", "license", "no recognised license. It reads as 'do not use this'.")

# README shape
try:
    readme = base64.b64decode(json.loads(gh("api", f"repos/{slug}/readme"))["content"]).decode()
except SystemExit:
    readme = ""
if not readme:
    record("FAIL", "readme", "missing")
else:
    words = len(re.findall(r"\w+", re.sub(r"```.*?```", "", readme, flags=re.S)))
    if words > 700:
        record("WARN", "readme length", f"{words} words. Target 400 to 700; move depth to a write-up.")
    elif words < 150:
        record("WARN", "readme length", f"{words} words. Probably too thin to rank.")
    else:
        record("PASS", "readme length", f"{words} words")

    body = re.sub(r"<[^>]+>|!?\[[^\]]*\]\([^)]*\)|\[!?\[.*?\n", "", readme)
    h1 = re.search(r"^# (.+)$", body, flags=re.M)
    tokens = [t for t in re.split(r"[-_]", name.lower()) if len(t) > 2]
    if not h1:
        record("FAIL", "readme H1", "no H1 found")
    elif tokens and not all(t in h1.group(1).lower() for t in tokens):
        record("WARN", "readme H1", f'"{h1.group(1)}" does not contain all words of "{name}"')
    else:
        record("PASS", "readme H1", h1.group(1))

    after = body[h1.end():] if h1 else body
    first = next((p.strip() for p in re.split(r"\n\s*\n", after) if p.strip() and not p.lstrip().startswith(("#", "|", "```", "-", "[!"))), "")
    if not first:
        record("WARN", "first paragraph", "none found. It acts as the search snippet.")
    elif len(first) > 320:
        record("WARN", "first paragraph", f"{len(first)} chars. Keep it to 2 or 3 sentences.")
    else:
        record("PASS", "first paragraph", f"{len(first)} chars")

# Community files
tree = json.loads(gh("api", f"repos/{slug}/contents/"))
files = {f["name"].lower() for f in tree}
for label, candidates in [
    ("CONTRIBUTING", {"contributing.md"}),
    ("SECURITY", {"security.md"}),
]:
    ok = bool(files & candidates)
    record("PASS" if ok else "WARN", label, "present" if ok else "missing in repo root")

width = max(len(n) for _, n, _ in results)
for level, n, d in results:
    print(f"{level:<5} {n:<{width}}  {d}")
print(f"\nMANUAL  social preview: cannot be read or set by CLI. Settings > General > Social preview (1280x640) for {slug}.")
if meta["isPrivate"]:
    print("NOTE    repo is private, so it is invisible to search until it is made public.")
sys.exit(1 if any(l == "FAIL" for l, _, _ in results) else 0)
