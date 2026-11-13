# Changelog

All notable changes are listed here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed
- MCP distribution facts (2026-11-02): Official MCP Registry `_meta` 4 KB limit and npm version timing, Glama listing claim, awesome-mcp-servers requirements, Claude plugin directory rules.
- MCP distribution facts (2026-11-03): Glama build config and stale listings, awesome-mcp-servers bot and entry rules, Claude plugin preparation.
- Retired platforms (2026-11-05): one table in `references/mcp-registry-checklist.md`; guidance for retired platforms removed.
- Claude plugin directory (2026-11-11): the file types and components the directory accepts from an organisation that is not Verified, and commands that list the files the directory is likely to refuse.
- Claude plugin directory (2026-11-05): a "Decide first" check for plugins that return third-party personal data, keep plugin files when not submitting, and two more documented holds (brand name, MCP server command).

### Added
- `references/audit-checks.md`: the repo audit and the listing checks as read-only GitHub CLI commands and tables. The audit flags files and README lines that name a retired platform. The listing checks cover the Official MCP Registry entry, its npm or Docker Hub package, Glama and awesome-mcp-servers.

### Removed
- `skills/github-seo/scripts/check_repo_seo.py`, `scripts/validate_skill.py` and the SVG assets. The Claude plugin directory accepts only Markdown, text, JSON, YAML and PNG, JPEG, GIF, WebP or ICO files from an organisation that is not Verified. CI runs the validator checks inline. The 0.3.0 security checks are now commands and result rules in `references/repo-security-checklist.md`.

## [0.3.0] - 2026-11-13

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
