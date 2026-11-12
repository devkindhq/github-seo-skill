#!/usr/bin/env python3
"""Read-only GitHub repo SEO and security audit.
Usage: check_repo_seo.py [owner/repo] [--security-only | --skip-security]

Needs the GitHub CLI (`gh`) logged in. Makes no changes (GET requests only). Exits 1 if any check fails.
Security checks that need admin rights print MANUAL instead of guessing.
"""
import base64
import json
import re
import subprocess
import sys
from urllib.parse import quote

results = []


def gh(*args):
    out = subprocess.run(["gh", *args], capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"gh {' '.join(args)} failed: {out.stderr.strip()}")
    return out.stdout


def record(level, name, detail):
    results.append((level, name, detail))


def api(path):
    """GET via gh. Returns (status, parsed JSON or None). Never raises, never prints credentials."""
    out = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if out.returncode == 0:
        try:
            return 200, json.loads(out.stdout) if out.stdout.strip() else {}
        except ValueError:
            return 200, None
    m = re.search(r"HTTP (\d{3})", out.stderr)
    return (int(m.group(1)) if m else 0), None


def security_checks(slug, default_branch):
    """Repo security and permission checks. Reports only; never changes settings."""
    need = "could not check, needs admin"
    st, repo = api(f"repos/{slug}")
    if st != 200 or not isinstance(repo, dict):
        record("MANUAL", "security", f"could not read repo settings (HTTP {st or 'error'})")
        return
    default_branch = repo.get("default_branch") or default_branch
    admin = bool((repo.get("permissions") or {}).get("admin"))
    sa = repo.get("security_and_analysis")
    record("PASS" if admin else "WARN", "token permission", "admin" if admin else "read or write only. Settings checks below are limited.")

    def branch_rules(branch):
        st_r, rules = api(f"repos/{slug}/rules/branches/{quote(branch, safe='')}")
        types = {r.get("type") for r in rules} if st_r == 200 and isinstance(rules, list) else set()
        legacy = None
        if admin:
            st_p, prot = api(f"repos/{slug}/branches/{quote(branch, safe='')}/protection")
            if st_p == 200 and isinstance(prot, dict):
                legacy = prot
                if prot.get("required_pull_request_reviews"):
                    types.add("pull_request")
                if not (prot.get("allow_deletions") or {}).get("enabled"):
                    types.add("deletion")
                if not (prot.get("allow_force_pushes") or {}).get("enabled"):
                    types.add("non_fast_forward")
        return st_r, types, legacy

    def report_branch(label, branch, need_pr):
        st_r, types, _ = branch_rules(branch)
        if st_r != 200:
            record("MANUAL", label, f"rules endpoint returned HTTP {st_r or 'error'} for {branch}")
            return
        wanted = ["deletion", "non_fast_forward"] + (["pull_request"] if need_pr else [])
        missing = [t for t in wanted if t not in types]
        names = {"deletion": "deletion blocked", "non_fast_forward": "force-push blocked", "pull_request": "PR required"}
        if not missing:
            record("PASS", label, f"{branch}: " + ", ".join(names[t] for t in wanted))
        elif not types and not admin:
            record("MANUAL", label, f"{branch}: no active ruleset seen; legacy branch protection {need}")
        else:
            note = "" if admin else f" (legacy branch protection {need})"
            record("FAIL" if not types else "WARN", label, f"{branch}: missing " + ", ".join(names[t] for t in missing) + note)

    report_branch("default branch rules", default_branch, True)

    if repo.get("has_pages"):
        st_g, pg = api(f"repos/{slug}/pages")
        src = (pg or {}).get("source") if st_g == 200 and isinstance(pg, dict) else None
        if src and src.get("branch"):
            if src["branch"] == default_branch:
                record("PASS", "pages branch rules", f"publishes from {default_branch}, covered above")
            else:
                report_branch("pages branch rules", src["branch"], False)
        elif st_g == 200 and isinstance(pg, dict):
            record("MANUAL", "pages branch rules", f"build_type {pg.get('build_type')}: check the github-pages environment deployment rule in Settings > Environments")
        else:
            record("MANUAL", "pages branch rules", f"Pages is on but the source could not be read (HTTP {st_g or 'error'})")

    if isinstance(sa, dict):
        for key, label in (("secret_scanning", "secret scanning"), ("secret_scanning_push_protection", "push protection"), ("dependabot_security_updates", "dependabot security updates")):
            status = (sa.get(key) or {}).get("status")
            record("PASS" if status == "enabled" else "WARN", label, status or "not reported")
    else:
        for label in ("secret scanning", "push protection", "dependabot security updates"):
            record("MANUAL", label, need)
    if admin:
        st_v, _ = api(f"repos/{slug}/vulnerability-alerts")
        record("PASS" if st_v == 200 else "WARN", "dependabot alerts", "enabled" if st_v == 200 else "disabled (HTTP 404)" if st_v == 404 else f"HTTP {st_v or 'error'}")
    else:
        record("MANUAL", "dependabot alerts", need)

    st_p, pvr = api(f"repos/{slug}/private-vulnerability-reporting")
    if st_p == 200 and isinstance(pvr, dict):
        record("PASS" if pvr.get("enabled") else "WARN", "private vulnerability reporting", "enabled" if pvr.get("enabled") else "disabled. SECURITY.md should say where to report.")
    else:
        record("MANUAL", "private vulnerability reporting", f"HTTP {st_p or 'error'}, {need}")

    st_w, wf = api(f"repos/{slug}/actions/permissions/workflow")
    if st_w == 200 and isinstance(wf, dict):
        record("PASS" if wf.get("default_workflow_permissions") == "read" else "WARN", "actions default token", f"default_workflow_permissions={wf.get('default_workflow_permissions')}")
        record("PASS" if not wf.get("can_approve_pull_request_reviews") else "WARN", "actions approve PRs", f"can_approve_pull_request_reviews={wf.get('can_approve_pull_request_reviews')}")
    else:
        record("MANUAL", "actions workflow permissions", f"HTTP {st_w or 'error'}, {need}")
    st_f, fp = api(f"repos/{slug}/actions/permissions/fork-pr-contributor-approval")
    if st_f == 200 and isinstance(fp, dict):
        pol = fp.get("approval_policy")
        record("PASS" if pol in ("first_time_contributors", "all_external_contributors") else "WARN", "fork PR approval", str(pol))
    else:
        record("MANUAL", "fork PR approval", f"HTTP {st_f or 'error'}, {need}")


def finish(slug, meta):
    width = max(len(n) for _, n, _ in results)
    for level, n, d in results:
        print(f"{level:<6} {n:<{width}}  {d}")
    return slug, meta


flags = [a for a in sys.argv[1:] if a.startswith("--")]
target = [a for a in sys.argv[1:] if not a.startswith("--")][:1]
if "--security-only" in flags and "--skip-security" in flags:
    sys.exit("use only one of --security-only and --skip-security")
meta = json.loads(
    gh(
        "repo", "view", *target, "--json",
        "nameWithOwner,name,description,homepageUrl,licenseInfo,repositoryTopics,isPrivate,defaultBranchRef",
    )
)
slug = meta["nameWithOwner"]
name = meta["name"]
default_branch = (meta.get("defaultBranchRef") or {}).get("name") or "main"

if "--security-only" in flags:
    security_checks(slug, default_branch)
    finish(slug, meta)
    sys.exit(1 if any(l == "FAIL" for l, _, _ in results) else 0)

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

# MCP server metadata (only when a server.json is present)
if "server.json" in files:
    try:
        sj = json.loads(base64.b64decode(json.loads(gh("api", f"repos/{slug}/contents/server.json"))["content"]))
    except (SystemExit, ValueError):
        sj = None
        record("FAIL", "server.json", "present but not valid JSON")
    if sj is not None:
        owner = slug.split("/")[0].lower()
        sname = sj.get("name", "")
        if sname.lower().startswith(f"io.github.{owner}/"):
            record("PASS", "server.json name", sname)
        else:
            record("WARN", "server.json name", f'"{sname}" is not io.github.{owner}/*. Fine only with domain auth.')
        sdesc = sj.get("description", "")
        record("PASS" if 0 < len(sdesc) <= 100 else "FAIL", "server.json description", f"{len(sdesc)} chars, max 100")
        record("PASS" if sj.get("websiteUrl") else "WARN", "server.json websiteUrl", sj.get("websiteUrl") or "empty. Set the official homepage field.")
        pkgs = sj.get("packages") or []
        if any(p.get("registryType") == "oci" for p in pkgs):
            df = ""
            if "dockerfile" in files:
                df = base64.b64decode(json.loads(gh("api", f"repos/{slug}/contents/Dockerfile"))["content"]).decode()
            has = "io.modelcontextprotocol.server.name" in df and sname in df
            record("PASS" if has else "FAIL", "OCI label", "matches server.json name" if has else "Dockerfile lacks LABEL io.modelcontextprotocol.server.name matching the name")
        elif any(p.get("registryType") == "npm" for p in pkgs):
            record("PASS", "npm mcpName", "check package.json mcpName equals server.json name (not read by this script)")

if "--skip-security" not in flags:
    security_checks(slug, default_branch)

finish(slug, meta)
print(f"\nMANUAL  social preview: cannot be read or set by CLI. Settings > General > Social preview (1280x640) for {slug}.")
if meta["isPrivate"]:
    print("NOTE    repo is private, so it is invisible to search until it is made public.")
sys.exit(1 if any(l == "FAIL" for l, _, _ in results) else 0)
