# General GitHub repo SEO (label: general)

Everything here is common open-source practice, not tested by this project. GitHub does not
publish its search relevance algorithm, and some widely repeated claims trace back to a single
third-party blog post. Treat each item as plausible, not confirmed, and re-check against GitHub's
own documentation before stating it as fact to anyone.

Two items below are corroborated by direct observation (labelled observed) and deserve more weight.

## Two tiers

| Tier | What you control | Levers |
|---|---|---|
| GitHub-native discovery (GitHub search, topic pages, social unfurls) | Repo metadata only | Name, description, topics, homepage, README H1 and headings, social preview |
| Web and AI discovery (Google, language-model crawlers) | Full page metadata, but only on a site you own | Title, meta description, structured data, readable URLs on a docs or Pages site |

A README cannot set the HTML head of the repo page. For full control, add a docs site.
Work the first tier first: every lever is a one-line `gh` command or a settings toggle.

## Repo-level fields

- **Slug** [observed]: appears in the search result title as `owner/repo-name`. The highest-leverage field and the most expensive to change.
- **Description** [general]: one sentence. Lead with the category word people type ("CLI",
  "template", "library", "MCP server"), then the audience or platform, then the outcome. A useful
  shape is "[Category] for [audience] to [outcome]". Under about 120 characters displays
  untruncated in most results and unfurls. Hard limit is 350 characters.
- **Website field** [general]: set it to the canonical write-up instead of leaving it blank.
- **README first paragraph** [observed]: behaves like a meta description in search snippets.
- **Topics** [general]: they feed topic pages, a real browsing surface. Use accurate ones that
  other repos also use (check the topic page exists and is active). Quality over quantity: fill
  toward GitHub's cap of 20 only with topics you can defend. Lowercase, hyphenated.
- **Social preview image** [general]: 1280 by 640. Improves link unfurls in chat and social
  apps. Not a ranking factor.
- **Freshness** [general]: recent commits and releases appear to help a maintained repo against
  an abandoned one. No metadata can fake it.

## Org and profile level

- **Pinning** [general]: helps people browsing an org or profile. No evidence either way for search ranking.
- **Profile README** [general]: a personal profile naming the company and linking its site is a
  cheap credibility signal. Treat it as credibility, not ranking.

## Contribution hygiene

- **LICENSE**: absence reads to developers as "do not use this". This is established open-source norm.
- **CONTRIBUTING.md, SECURITY.md, issue and pull request templates**: signal a maintained project
  and give visitors a next step.

## Measuring

GitHub's traffic page (Insights, Traffic) keeps 14 days of views and clones. Compare views and
unique visitors across a few 14 day windows before and after a change, and screenshot them,
because older data is dropped. Do not promise numbers from vendor blog statistics.

## How to report this file's content

When you pass these items on, say they are general practice rather than verified findings.
