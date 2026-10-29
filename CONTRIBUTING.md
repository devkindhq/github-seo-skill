# Contributing

Thanks for helping. The most valuable contribution is a correction or addition backed by a source.

## What makes a good change

- **Cite it.** New claims need a source or a dated observation, and one of the three labels
  (verified, observed, general) described in `skills/github-seo/SKILL.md`.
- **Date it.** Registry flows, subreddit rules and gallery requirements change. Include the date you checked.
- **Keep it short.** The skill should stay easy for a model to follow. Move depth into `references/`.
- **No client data.** Never include names, domains or details from private projects.

## Workflow

1. Fork and branch from `main`.
2. Make the change.
3. Run `python3 scripts/validate_skill.py`. It must print `ok`.
4. If you changed when the skill should trigger, update `skills/github-seo/evals/evals.json`.
5. Add a line to `CHANGELOG.md` under an Unreleased heading.
6. Open a pull request and fill in the template.

## Reporting a wrong claim

Open an issue using the bug report template and link the source that contradicts the skill.
