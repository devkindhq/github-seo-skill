# Changelog

All notable changes are listed here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Repo security and permission checks in `check_repo_seo.py` (read-only, GET only): default branch and Pages publishing branch rules (PR required, deletion and force-push blocked), secret scanning, push protection, Dependabot, private vulnerability reporting, Actions token permissions and fork PR approval. Checks that need admin print MANUAL.
- `--security-only` and `--skip-security` flags.
- `references/repo-security-checklist.md` with evidence labels and the exact `gh api` commands (checked 2026-11-13).
- SKILL.md Step 1b, and evals for security audit prompts. The existing `set up branch protection rules on main` should_not_trigger case stays valid: the skill audits and recommends, it never configures.

## [0.2.0] - 2026-11-02

### Added
- `references/mcp-install-and-metadata.md`: package types and ownership checks, `server.json` fields, README install routes per client, listing files, org visibility.
- Audit checks for `server.json` (description length, `websiteUrl`, namespace) and the OCI label.
- Docker/OCI registry quality eval.
- MCP publishing learnings from a real run (2026-11-02): org namespace auth, OCI build and verify flow, no `validate` command, listing check, Docker MCP Registry route, leaked-history scrub, README install block generation, closing "who built this" section.

## [0.1.0] - 2026-10-29

### Added
- `github-seo` skill with plain-repo and MCP-server paths.
- References: README template, distribution sequence, MCP registry checklist, publish safety, general GitHub SEO.
- `check_repo_seo.py`, a read-only audit script built on the GitHub CLI.
- Trigger and quality evals, a validator, and CI.
- Claude Code plugin and marketplace manifests.
