# Changelog

All notable changes are listed here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed
- MCP distribution facts (2026-11-02): Smithery is now a passive registry, Official MCP Registry `_meta` 4 KB limit and npm version timing, Glama listing claim, awesome-mcp-servers requirements, Claude plugin directory rules.
- Claude plugin directory (2026-11-03): listing fields in `plugin.json` (`icon` and URL fields), local `claude plugin validate`, how to choose the plugin folder.

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
