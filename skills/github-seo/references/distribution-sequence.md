# Distribution sequence

Order matters more than any single channel. Each step exists to create the artifact the next
step needs. Do not post to Reddit or Hacker News before the repo and the write-up exist, because
every downstream post links back to them.

## Step 1: the repo is public and complete

No announcement yet. License, working quickstart, and a results table if applicable. A
half-finished README poisons every later step.

## Step 2: the canonical write-up

Publish it on a domain you own, with a named author. Every community post points here. Linking
your own domain from a forum is more defensible than linking a bare repo, and reads less like a drive-by.

## Step 3: Reddit (where the risk is)

[observed, medium confidence, 2026-08-08. Subreddit rules and moderator discretion change. Read
each sidebar before posting.]

- r/programming removes most commercial content regardless of framing. Do not post there.
- r/webdev prohibits commercial promotion. Non-commercial project shares are confined to the weekly
  showcase thread and must be technical. A standalone post gets removed.
- Reddit has an informal 90/10 norm: roughly 90% of an account's activity should be non-promotional.
  Cross-posting identical promotional text is one of the fastest routes to a sitewide spam action.
- Post in subreddits specific to the platform or stack, which also tend to surface in search.
- Post the finding, not the repo. Title it as a result ("Measured X across Y, here is what changed").
  Put the table in the post body so it has value if nobody clicks. Link the repo once, at the
  bottom, with your affiliation disclosed.

## Step 4: platform community forums

Underrated for the effort. Answering an existing question on a platform's own forum with a real
measurement or fix is about the least spam-shaped thing you can do, and those threads rank and
persist for years. Find live threads asking the question your project answers, answer properly, link once.

## Step 5: Hacker News

Only once the repo has real stars and the write-up is worth the front page. Submit the write-up,
not the repo. Use "Show HN" only if people can run the thing themselves. There is no second
attempt with the same URL, so spend the shot deliberately.

## Step 6: dev.to

Low risk, low ceiling. Cross-post the write-up with the canonical URL set back to your domain.

## Step 7: upstream template galleries

Runs on its own track and can start in parallel with Step 1 because it has lead time.
Example: `cloudflare/templates`. Requirements below were read from its `CONTRIBUTING.md` on
2026-10-29 [verified, 2026-10-29]. Re-read the live file before relying on them.

- Directory and `package.json` `name` in kebab-case, ending in `-template`.
- `package.json` needs `name` and `description`. If the template is to be published in the
  dashboard it also needs `cloudflare.label` (Title Case) and `cloudflare.products` (three or fewer).
- `cloudflare.bindings` should describe every binding that needs configuration outside Cloudflare.
- A `package-lock.json`, generated with the gallery's own command (`pnpm fix:lockfiles` at the time of reading).
- A README with a getting-started section and a screenshot or live deployment, with the display
  block wrapped in the `dash-content-start` and `dash-content-end` comment markers.
- Preview image and icon URLs can only be supplied by a Cloudflare team member.
- Stated priority: templates that demonstrate full-stack capability and combine several binding
  or handler types.

If you have a warm contact at the gallery's organisation, open the PR first, then message them
with the link. A live PR with green CI turns a cold ask into a review request.

## Step 8: awesome-lists

Only after the repo has real stars and a complete README. Read the list's contribution rules,
follow its entry format exactly, and submit one entry.

## General notes

- Use the same author byline on every artifact, from a personal account where relevant rather than a brand account.
- The specific subreddits, forums and galleries above come from one ecosystem (Shopify and
  Cloudflare). Keep the order (repo, write-up, community, wider channels, galleries) in other
  ecosystems, but re-verify which named communities apply.
