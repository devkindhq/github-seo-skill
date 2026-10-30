# Changelog

All notable changes are listed here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `references/mcp-install-and-metadata.md`: package types and ownership checks, `server.json` fields, README install routes per client, listing files, org visibility.
- Audit checks for `server.json` (description length, `websiteUrl`, namespace) and the OCI label.
- Docker/OCI registry quality eval.

## [0.1.0] - 2026-10-29

### Added
- `github-seo` skill with plain-repo and MCP-server paths.
- References: README template, distribution sequence, MCP registry checklist, publish safety, general GitHub SEO.
- `check_repo_seo.py`, a read-only audit script built on the GitHub CLI.
- Trigger and quality evals, a validator, and CI.
- Claude Code plugin and marketplace manifests.
