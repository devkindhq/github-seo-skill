# MCP server registry checklist

Generalised from a real MCP server submission run across these registries on 2026-05-15
[observed]. Registries change their processes, so re-check each flow before repeating this.

## Prerequisite

Finish Step A in `SKILL.md` first (README, description, topics, license). A registry listing
points back at the repo, and a thin repo makes a thin listing. Then work through
`mcp-install-and-metadata.md` for the package type, `server.json` fields and README install routes.

## Prepare the submission copy once

Write the fields every listing asks for, then reuse them verbatim so listings stay consistent.

| Field | Notes |
|---|---|
| Name | Product name, same everywhere |
| Package | npm or PyPI package name, if any |
| Repository | GitHub URL |
| Homepage | Canonical page on a domain you own |
| Author | Organisation name |
| License | Match the repo's actual license |
| Description | One or two sentences: what it integrates, what an AI client can do with it |
| Tools | Full list of exposed tool names |
| Install | For example `npx <package-name>` |
| Env vars | Every required variable name. Never the values |

## Registry status

| Registry | How it works | Action |
|---|---|---|
| **Official MCP Registry** | A `server.json` in your project, published with the `mcp-publisher` CLI. Names take the form `io.github.<github-user-or-org>/<name>` and you must authenticate with access to that namespace [verified, 2026-10-29, registry README]. For an org namespace the device flow is not enough, see `mcp-install-and-metadata.md` section 2 [verified, 2026-11-02]. A pull request to the registry repo does not publish a server [verified, 2026-10-29]. | Direct. Do this first, because other registries ingest from it. |
| **Docker MCP Registry** | PR adding `servers/<name>/server.yaml`, Docker team review [verified, 2026-11-02]. | Optional second route, see `mcp-install-and-metadata.md` section 8. |
| **PulseMCP** | Ingests from the Official Registry [observed]. | None once the Official entry is live. |
| **mcpbench.ai** | Indexes from the Official Registry, can lag [observed]. | Verify it appears. |
| **Glama** | Manual submission, goes to review [observed]. A listing can exist before you submit [observed, 2026-11-02]. Approval comes by email [observed, 2026-11-03]. The listing gets tools and a score only after a Glama build passes [observed, 2026-11-03]. | Search Glama first. Claim an existing listing (see Gotchas), else submit with Add Server and wait for the email. Then set the build (see Gotchas). |
| **mcp.so** | Manual submission with name, icon and server config, human approval [observed]. | Direct, then wait. |
| **mcpservers.org** | Free manual listing, category required, email approval [observed]. | Direct, then wait. |
| **Cursor Directory** | Manual submission with an icon upload [observed]. | Direct. |
| **MCPMarket** | Observed to index without a submission form [observed]. | Verify the listing and description. |
| **Community lists** (selective, unclear criteria) | Small subsets of servers, links may be nofollow [observed]. | Low priority. |

## Retired platforms

Do not submit to these. Remove their config files, scripts and doc mentions, but keep released
changelog entries. The Step 2 audit
(`scripts/check_repo_seo.py`) reads this table and flags any file path or README line that names
a platform here. To retire a platform, add a row.

| Platform | Status |
|---|---|
| **Smithery** | Out of service. Its hosting, API, accounts, CLI and SDKs shut down on 31 Oct 2026. Only a read-only directory remains, with nothing to publish [verified, 2026-11-05, smithery.ai/future]. |

## Gotchas

- **Empty `websiteUrl`.** Put the homepage in the official `websiteUrl` field, not only under
  `_meta`. See `mcp-install-and-metadata.md`.
- **Version drift.** Keep `package.json`, `server.json` and `manifest.json` on the same version.
- **Stale listings under a personal account.** If the server was ever published from a personal
  GitHub account before the org account existed, that listing can persist on other registries. Find it
  and have it removed, through the registry's support if there is no self-service delete.
- **Unclaimed Glama listing.** An npm-published server with a private repo already had an
  unclaimed Glama page with an older README [observed on a Devkind npm MCP server, 2026-11-02].
  The claim box on a Glama server page says access comes from the repo, with no form
  [observed, 2026-11-03, Glama server page claim box]:
  - The owner of a personal repo signs in as that GitHub account. The page becomes theirs at once.
  - For an org-owned repo, add `glama.json` at the repo root with your GitHub username under
    `maintainers`, then sign in. Glama recognises you on the next sync.

  ```json
  {"$schema": "https://glama.ai/mcp/schemas/server.json", "maintainers": ["github-username"]}
  ```

  After you change `glama.json`, do the Claim flow again [verified, 2026-11-02,
  https://glama.ai/blog/2025-07-08-what-is-glamajson].
- **Glama build config.** Glama builds its own image from the settings on the server page under
  Admin, Dockerfile. The repo needs no Dockerfile for this [observed, 2026-11-03]. Glama generated
  `pnpm install` build steps for a repo that pins `"packageManager": "yarn@1.22.22"`, and the build
  failed with "This project is configured to use yarn" [observed, 2026-11-03]. Set the build steps
  for the repo's own package manager, for example
  `["npm install -g yarn@1.22.22", "yarn install --frozen-lockfile", "yarn build"]`, and the CMD
  to the stdio entry point, for example `["mcp-proxy", "--", "node", "dist/index.js"]`. Check the
  generated environment schema as well: one set `TRANSPORT` to `http` for a server whose default
  is stdio [observed, 2026-11-03]. Use placeholder values only, never real keys.
- **Stale Glama listing.** The summary, tool list and score come from the latest Glama release,
  not from the repo [observed, 2026-11-03]. An old README or tool count after a sync usually means
  the build fails. Fix the build, then run Build & Release. Auto-Release then builds on every
  GitHub release [observed, 2026-11-03]. Glama numbers its releases on its own, so they do not
  match npm versions [observed, 2026-11-03].
- **Publish order.** Merge pull requests that change the tool surface before publishing to the
  Official Registry. If `server.json` lists tools, that list must match what ships, and some registries
  recompute a quality score from the live tool count.
- **Domain presence compounds** [general]. Several distinct root domains linking to the project is
  likely a stronger signal than one domain repeating. If you control more than one property,
  mention the server on each.

## awesome-mcp-servers

`punkpeye/awesome-mcp-servers` needs a Glama listing first. Its CI
(`.github/workflows/check-glama.yml`) and `CONTRIBUTING.md` require the following
[verified, 2026-11-02, commit 29f2d49]:

- A public GitHub repo. A remote-only server goes to `punkpeye/awesome-remote-mcp-servers`.
- The entry name in `owner/repo` form, linked to the GitHub repo. The CI message: "The entry
  name must use the full `owner/repo` format (not just the repo name)."
- A Glama score badge in the entry. Without it, CI adds the label `missing-glama`:
  `[![owner/repo MCP server](https://glama.ai/mcp/servers/owner/repo/badges/score.svg)](https://glama.ai/mcp/servers/owner/repo)`
- At least one permitted emoji and no other emoji. 🎖️ marks an official implementation only.
- Alphabetical order within the category.

The list's bot and recent merges add these rules:

- The Glama listing must pass Glama's checks, not only show a badge. The bot asks that the server
  "passes all checks" and that it "start and respond to introspection requests", which is the Glama
  build above [verified, 2026-11-03, bot comment on a closed PR].
- One server per PR. Nearly every merged PR adds one line [observed, 2026-11-03].
- The scope emoji follows the note under the README legend: ☁️ "when MCP server is talking to
  remote APIs", 🏠 "when MCP server is talking to a locally installed software" [verified,
  2026-11-03, README legend note].
- Put the badge right after the repo link, as the existing entries do [observed, 2026-11-03].
- `CONTRIBUTING.md` sets no star minimum. The Glama checks are the gate for this list
  [verified, 2026-11-03, CONTRIBUTING.md].

Order: make the repo public, get the Glama listing, then open the awesome-list PR.

## After submission

Most manual registries have a review queue and no way to speed it up. Track pending reviews in a
note and check back, rather than resubmitting.

Check the listings with one command. It needs `gh` logged in and reads `server.json` from the repo:

```bash
python3 scripts/check_listings.py owner/repo
```

It finds the latest Official MCP Registry entry and checks the package it names: the npm version
matches, or the OCI image tag exists on Docker Hub. It also checks that the Glama page exists, and
whether awesome-mcp-servers lists the repo or has a pull request for it. Directories that need a login, such as the Claude plugin
directory, stay a manual check.
