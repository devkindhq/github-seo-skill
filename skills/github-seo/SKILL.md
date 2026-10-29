---
name: github-seo
description: Makes an open-source GitHub repo discoverable and safe to publish. Audits the repo name, description, topics and README for search, writes a search-ready README, runs a pre-publish secret and client-data check, and guides the launch sequence. Covers MCP server registry submissions (Official MCP Registry, Smithery, Glama, mcp.so). Use when the user wants more stars, traffic or search visibility for a repo, is about to open-source a project, asks for GitHub SEO or repo SEO, or wants to publish an MCP server. Not for general website SEO.
license: MIT
---

# GitHub SEO

A playbook for getting an open-source repo found, ranked and cited, in the right order.
Built from Devkind's own SERP research plus standard open-source practice.

## Evidence labels

Every claim in this skill and its references carries one of three labels. Keep them when you
report back, and never upgrade a label without a source.

- **verified**: checked against a primary source or a live search result, with a date.
- **observed**: seen in a real result at a point in time, not a documented rule. Re-check before relying on it.
- **general**: common open-source practice, not tested here. State it as practice, not fact.

GitHub does not publish its search ranking algorithm. Treat any "GitHub ranks X" statement as inference.

## Step 0: pick the path

- **Path A, plain GitHub repo**: a template, starter, benchmark harness, CLI, library or skill.
- **Path B, MCP server**: the project defines tools or resources over the Model Context Protocol
  (look for `server.json`, `mcp.json` or an MCP SDK dependency). Do Path A first, then Step B.

If unsure, check whether the repo exposes MCP tools. If it does, it is Path B plus Path A.

## Step 1: safety pass (mandatory, before anything goes public)

Never skip this, and never let distribution excitement jump ahead of it.

1. Confirm the repo holds no private client code, client names, store domains, internal ticket
   keys, API details specific to a client, or personal data about contractors or employees.
2. Scan the **full git history**, not only the current tree. A key committed and later deleted is
   still recoverable. Use `gitleaks detect --source . -v` when installed; otherwise use the grep
   in `references/publish-safety.md`.
3. If anything questionable appears, stop and tell the repo owner. The public or private call is theirs.
4. Settle the repo name now. Renaming after links accrue is costly (see Step A.1).

Details and the publish-or-not framework: `references/publish-safety.md`.

## Step 2: audit what exists

Run the read-only audit. It needs the GitHub CLI (`gh`) logged in.

```bash
python3 scripts/check_repo_seo.py owner/repo
```

It reports pass, warn or fail for the description, topics, homepage, license, README shape,
and community files, and prints the one lever it cannot check (the social preview image).
Fix failures first, then warnings.

## Step A: plain repo checklist

1. **Slug.** Use a keyword-bearing name, not an internal codename. The slug appears in the page
   title as `owner/repo-name` [observed, 2026-08-08, two top-ranking repos in one SERP].
   Rename before the repo is public. If it is already public and linked, prefer fixing the
   description and H1 over a rename.
2. **README.** Write it from `references/readme-template.md`: 400 to 700 words, keyword-bearing
   H1, a first paragraph that works as a search snippet [observed], a copy-pasteable quickstart.
3. **About box.** One sentence description with the platform nouns people type, the Website
   field set to the canonical write-up, and topics that are accurate (GitHub allows up to 20).
   Field guidance: `references/general-github-seo.md` [general].
4. **License and contributor files.** Add a `LICENSE` (no license reads as "do not use this"),
   `CONTRIBUTING.md` and `SECURITY.md`.
5. **Social preview.** Upload a 1280 by 640 image in Settings, General. GitHub offers no CLI or
   API for it, so tell the owner exactly where to click.
6. **Pin** the repo on the organisation profile and on the maintainer's personal profile.
7. **Canonical write-up.** Publish a long-form post on a domain you own before any community
   post. Community posts link to it, not to the bare repo. If the repo makes a measurable claim,
   put a results table in the post: structured tables from independent-looking domains are what
   comparison-style AI answers tend to cite [observed].
8. **Launch** in the order in `references/distribution-sequence.md`. Order matters; each step
   produces the artifact the next needs.
9. **Upstream galleries and awesome-lists** only once the repo is complete and has real stars.
   Maintainers reject cold, thin submissions.

## Step B: MCP server checklist (after Step A)

Use `references/mcp-registry-checklist.md`. It covers the Official MCP Registry (`server.json`
plus the `mcp-publisher` CLI), Smithery, Glama, mcp.so, mcpservers.org, Cursor Directory, which
registries auto-ingest from the Official one, and common gotchas (stale listings under a personal
account, publish order, domain presence).

## What not to do

- Do not buy stars or run star-for-star swaps. The one visible signal is also the one that gets accounts banned.
- Do not post identical promotional text across subreddits, and do not post in r/programming or r/webdev (see the distribution reference for the posture).
- Do not budget citation lift on `llms.txt`. It is a 20 minute add, not a strategy [observed: a cited study found 97% of such files got zero AI-agent requests].
- Do not publish a benchmark that documents an unfixed live defect in someone's shipping product. Fix it first, then publish the general finding.
- Do not keyword-stuff the About box or topics. Every keyword must be defensible and accurate.
- Do not state registry behaviour or ranking mechanics as fact without a source. Flag it as an assumption.

## Reporting back

When you finish, give the owner three lists: what you changed, what only they can do (social
preview upload, pinning, account-bound registry logins), and which advice is verified, observed
or general.
