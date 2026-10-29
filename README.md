<p align="center">
  <img src="assets/social-preview.png" alt="GitHub SEO Skill: get your open-source repo found" width="640"/>
</p>

# GitHub SEO Skill

[![CI](https://github.com/devkindhq/github-seo-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/devkindhq/github-seo-skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

GitHub SEO Skill is an Agent Skill for Claude Code that gets open-source GitHub repos found on
Google and GitHub search. It audits a repo's name, description, topics and README, writes a
search-ready README, runs a pre-publish secret and client-data check, and walks MCP servers
through registry submissions such as the Official MCP Registry, Smithery, Glama and mcp.so.

It works with any tool that supports the [Agent Skills](https://agentskills.io) format.

## Quick start

Install with the [skills CLI](https://skills.sh):

```bash
npx skills add devkindhq/github-seo-skill
```

Or as a Claude Code plugin:

```
/plugin marketplace add devkindhq/github-seo-skill
/plugin install github-seo-skill@github-seo-skill
```

Or copy the skill folder into a project:

```bash
git clone https://github.com/devkindhq/github-seo-skill.git
cp -r github-seo-skill/skills/github-seo your-project/.claude/skills/
```

Then ask in plain words, for example "audit github.com/you/your-repo for search visibility" or
"we are about to open-source this CLI, what should we check first?". The skill activates from its description.

## What it does

| Stage | What you get |
|---|---|
| Safety pass | Full-history secret scan and client-data check before anything goes public |
| Audit | A read-only script scores the description, topics, homepage, license, README shape and community files |
| README | An eight-section template aimed at the search snippet, 400 to 700 words |
| Metadata | Repo slug, About text, topics, Website field and social preview guidance |
| Launch | A tested order: repo, write-up, community, wider channels, template galleries |
| MCP servers | A registry-by-registry checklist built around the Official MCP Registry |

## Run the audit yourself

Needs the [GitHub CLI](https://cli.github.com) logged in. The script changes nothing.

```bash
python3 skills/github-seo/scripts/check_repo_seo.py owner/repo
```

It prints `PASS`, `WARN` or `FAIL` per check and exits non-zero on any `FAIL`. The social preview
image cannot be read or set through the CLI, so it is listed as a manual step.

## How the advice is labelled

GitHub does not publish how its search ranks repositories, so every claim in the skill carries a label:

- **verified**: checked against a primary source, with a date.
- **observed**: seen in a real search result at a point in time. Re-check before relying on it.
- **general**: common open-source practice that has not been tested here.

The skill is built to repeat those labels when it reports back, instead of presenting guesses as rules.

## Repository layout

```
skills/github-seo/        # the skill: SKILL.md, references/, scripts/, evals/
.claude-plugin/           # plugin and marketplace manifests
scripts/validate_skill.py # checks frontmatter, evals, manifests and links (runs in CI)
```

## Related projects

[Paldom/github-skills](https://github.com/Paldom/github-skills) is a broader set of skills for
professional repos (README authoring, docs sites, community files, protections). This skill
focuses on search visibility, safe publishing and MCP registry listings, and the two complement each other.

## Contributing

Corrections backed by a source are the most useful contribution. See [CONTRIBUTING.md](CONTRIBUTING.md).
Security issues go through [SECURITY.md](SECURITY.md), and everyone is expected to follow the
[Code of Conduct](CODE_OF_CONDUCT.md).

## License

[MIT](LICENSE). Built by [Devkind](https://devkind.com.au).
