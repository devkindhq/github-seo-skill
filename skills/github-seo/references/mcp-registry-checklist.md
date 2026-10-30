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
| **Official MCP Registry** | A `server.json` in your project, published with the `mcp-publisher` CLI. Names take the form `io.github.<github-user-or-org>/<name>` and you must authenticate as that GitHub account [verified, 2026-10-29, registry README]. A pull request to the registry repo does not publish a server [verified, 2026-10-29]. | Direct. Do this first, because other registries ingest from it. |
| **Smithery** | Listed under an organisation namespace. Shows a quality score that depends on the live tool surface [observed]. | Direct. Check for stale listings under a personal account. |
| **PulseMCP** | Ingests from the Official Registry [observed]. | None once the Official entry is live. |
| **mcpbench.ai** | Indexes from the Official Registry, can lag [observed]. | Verify it appears. |
| **Glama** | Manual submission, goes to review [observed]. | Direct, then wait. |
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
  Smithery. Find it and have it removed, through the registry's support if there is no self-service delete.
- **Publish order.** Merge pull requests that change the tool surface before publishing to the
  Official Registry. The `server.json` tool list must match what ships, and some registries
  recompute a quality score from the live tool count.
- **Domain presence compounds** [general]. Several distinct root domains linking to the project is
  likely a stronger signal than one domain repeating. If you control more than one property,
  mention the server on each.

## After submission

Most manual registries have a review queue and no way to speed it up. Track pending reviews in a
note and check back, rather than resubmitting.
