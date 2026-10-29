# README template

Target length: 400 to 700 words on the repo root. Longer material belongs in a canonical
write-up on a domain you own. A long README only gets duplicated later.

**Why this shape** [observed, 2026-08-08]: in a live search for `shopify app cloudflare workers
template`, two top-ranking repos had the README's opening sentence lifted into the search
snippet. GitHub's rendered README is the page body Google indexes, so the first paragraph
functions as the meta description. This is an observation of two results, not a published rule.

## The eight sections, in order

1. **H1 is the plain-English name with the platform nouns.** Searchers type "shopify" or
   "cloudflare workers", not your internal codename. Make the H1 match or contain the repo name.
2. **First paragraph, two or three sentences, keyword-bearing.** Write it as a meta description:
   what the project does and what it runs on. No marketing adjectives.
3. **The headline number, as a small results table above the fold**, if the project makes a
   measurable claim. This is the part that gets quoted and extracted. Rules that make a claim citable [observed]:
   - One number per sentence with its unit and method: "103 KiB gzipped, measured with
     `wrangler deploy --dry-run`" survives extraction; "much smaller" does not.
   - Stable column headers.
   - State negative results plainly. A caveat such as "X is an upper bound because Y failed"
     makes the rest more trustworthy.
4. **Quickstart.** Copy-pasteable, working, under six commands.
5. **How this was measured** (if applicable). The exact command and the date, two paragraphs at most.
   Provenance travels with the sentence when an assistant reproduces the claim.
6. **One prominent link** to the full write-up. One link, not a nav bar of twelve.
7. **Author line.** "Built by Org. Maintained by Name." Use the same name and wording on every
   public artifact. Consistency is the credibility signal, not any single page.
8. **License and contributing.** Link `LICENSE` and `CONTRIBUTING.md`.

## Set in the same pass (not README body)

- Repo description (About), one sentence
- Topics, accurate ones only (GitHub cap is 20)
- Website field pointing at the canonical write-up
- Social preview image, 1280 by 640
- Pinned on the org and personal profiles

## Avoid

- A 2,000 word README meant to rank for everything.
- The internal codename as H1 or slug.
- Badge walls. Keep to the few that carry information (CI, license, version).
- Em dashes and filler. Plain sentences read as human and quote cleanly.
