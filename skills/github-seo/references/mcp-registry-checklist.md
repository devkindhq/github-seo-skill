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
| **Smithery** | On 31 Oct 2026 its hosted server URLs, API, Connect and Toolbox, accounts and API keys, and CLI and SDKs stop working (current versions marked deprecated). It remains a public, non-proxied MCP registry powered by Arcade.dev [verified, 2026-11-02, smithery.ai/future]. | None. Do not publish to Smithery, and skip deploy or `smithery.yaml` work. An existing listing stays as a passive registry entry. |
| **PulseMCP** | Ingests from the Official Registry [observed]. | None once the Official entry is live. |
| **mcpbench.ai** | Indexes from the Official Registry, can lag [observed]. | Verify it appears. |
| **Glama** | Manual submission, goes to review [observed]. A listing can exist before you submit [observed, 2026-11-02]. | Search Glama first. Claim an existing listing (see Gotchas), else submit and wait. |
| **mcp.so** | Manual submission with name, icon and server config, human approval [observed]. | Direct, then wait. |
| **mcpservers.org** | Free manual listing, category required, email approval [observed]. | Direct, then wait. |
| **Cursor Directory** | Manual submission with an icon upload [observed]. | Direct. |
| **MCPMarket** | Observed to index without a submission form [observed]. | Verify the listing and description. |
| **Community lists** (selective, unclear criteria) | Small subsets of servers, links may be nofollow [observed]. | Low priority. |

## Gotchas

- **Empty `websiteUrl`.** Put the homepage in the official `websiteUrl` field, not only under
  `_meta`. See `mcp-install-and-metadata.md`.
- **Version drift.** Keep `package.json`, `server.json` and `manifest.json` on the same version.
- **Stale listings under a personal account.** If the server was ever published from a personal
  GitHub account before the org account existed, that listing can persist on registries such as
  Smithery. Find it and have it removed, through the registry's support if there is no self-service delete, though Smithery, now a passive registry, may no longer remove listings.
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
- **Publish order.** Merge pull requests that change the tool surface before publishing to the
  Official Registry. The `server.json` tool list must match what ships, and some registries
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

Order: make the repo public, get the Glama listing, then open the awesome-list PR.

## After submission

Most manual registries have a review queue and no way to speed it up. Track pending reviews in a
note and check back, rather than resubmitting.
