# MCP server install routes and listing metadata

How to make an MCP server easy to install from the README and complete in every registry entry.
Labels follow `SKILL.md`. Registry facts were checked against the official docs on 2026-10-31
[verified]. The install-route patterns come from a published, live MCP server README
[observed]; the per-client steps in them were not re-checked against each vendor's docs.

## 1. Pick the package type first

The Official MCP Registry stores metadata only. The package must already exist on a supported
host before you publish the entry [verified]. Each type has its own ownership check, and a
mismatch is the most common publish failure.

| Package type | `registryType` | Ownership check [verified] |
|---|---|---|
| npm (public registry only) | `npm` | `mcpName` in `package.json` equals the `server.json` `name` |
| PyPI | `pypi` | `mcp-name: <name>` string in the package README (a comment is fine) |
| NuGet | `nuget` | `mcp-name: <name>` string in the package README |
| Cargo | `cargo` | `mcp-name: <name>` as visible text, because crates.io strips HTML comments |
| Docker/OCI | `oci` | Image label `io.modelcontextprotocol.server.name` equals the `server.json` `name` |
| MCPB bundle | `mcpb` | URL contains "mcp", and `fileSha256` is set (clients check the hash) |

OCI details [verified]: supported hosts are Docker Hub, `ghcr.io`, Google Artifact Registry,
`*.azurecr.io` and `mcr.microsoft.com`. The `identifier` is `registry/namespace/repository:tag`
(a digest also works). Pin a version tag, not `latest`. Put the `LABEL` in the Dockerfile and
rebuild before the final push, because the label has to be in the pushed image.

## 2. Namespace and auth [verified]

- GitHub login gives `io.github.<user-or-org>/<name>`. A live org-owned entry exists
  (`io.github.devkindhq/swell`) [observed], so org namespaces work in practice.
- Domain auth (DNS TXT record or an HTTP file at `/.well-known/mcp-registry-auth`) gives a
  reverse-DNS name such as `com.example.*/<name>`.
- `mcp-publisher login github` is an interactive device-code flow. The repo owner runs it.

## 3. `server.json` fields that matter for discovery

Schema `2025-12-11` [verified]:

| Field | Rule | Why it matters |
|---|---|---|
| `name` | Required, 3 to 200 chars, exactly one `/` | The registry identity. Must match the package ownership check. |
| `description` | Required, **max 100 chars** | Shown in listings. Capability, not implementation. |
| `title` | Optional, max 100 | Display name. Use the product name. |
| `version` | Required, no ranges | Match the package version. |
| `websiteUrl` | Optional, URI | The official homepage field. **Set it.** |
| `repository` | `url` and `source` | Source link for inspection. |
| `icons` | Optional | PNG or JPEG for UI display. |
| `packages` | Array | One entry per install route (see section 1). |
| `_meta` | Vendor extension | Free-form. Put author, tool list and website here as a bonus, not instead of `websiteUrl`. |

Observed gap: a live entry that put the website only under `_meta` and left `websiteUrl` empty
[observed, 2026-10-31]. Whether downstream directories display `_meta` is unknown, so fill both.

Environment variables go in `packages[].environmentVariables` with `name`, `description`,
`isRequired` and `isSecret`. Names only, never values.

Verify after publishing:

```bash
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=<your-server-name>"
```

The registry is in preview, so breaking changes or data resets can happen [verified].

## 4. README install routes

Readers arrive with different clients. One "Standard config" block, then one collapsible block per
client, is the pattern used by a live server README [observed]:

1. **Requirements** line: runtime version, supported clients, which credentials are needed.
2. **Standard config**: the JSON that works in most clients. Show the launch command exactly as the
   package type dictates (`npx <pkg>` for npm, `uvx <pkg>` for PyPI, `docker run --rm -i <image>`
   for OCI). Use placeholder values for secrets.
3. **One `<details>` per client**, each with the shortest working path:
   - Claude Desktop: paste into `claude_desktop_config.json`.
   - Cursor: an install deeplink button plus the manual Settings path.
   - VS Code: the settings route plus `code --add-mcp '<json>'`.
   - Windsurf, Goose, LM Studio, Warp: the settings menu path, then reuse the standard config.
   - Claude Code: `claude mcp add` [general, confirm the flag syntax against current docs].
4. **Credentials**: where to find each key, the environment variable names, and a debug flag.
5. **Transports**: say which of stdio and HTTP the server supports.

Why it helps: each client name is a searchable phrase, the first copy-paste works for most
readers, and the collapsed blocks keep the README short [general]. Keep to the 400 to 700 word
target by linking out to the write-up for anything long, and cap the client list at the clients
you have actually tested.

Docker-only servers: the standard config is
`{"command":"docker","args":["run","--rm","-i","<image>:<tag>"]}`. Add resource limits only if the
server needs them.

## 5. Repo files that feed listings

| File | Feeds | Notes |
|---|---|---|
| `server.json` | Official MCP Registry | Section 3. Commit it to the repo root. |
| `smithery.yaml` | Smithery | `name`, `description`, `vendor`, `homepage`, `license`, `startCommand` with a config schema [observed]. |
| `manifest.json` | MCPB bundle, desktop installs | Carries `author` with name and URL, `repository`, and `user_config` prompts for credentials [observed]. |
| README badges | Humans | "Built by <org>" badge linking to the homepage. |

Keep one source of truth for the description, tool list and homepage, and copy it into each file.
A version drift between `package.json`, `server.json` and `manifest.json` is easy to introduce
[observed: one repo had `1.1.0` in two files and `1.0.9` in the third].

## 6. Make the org visible in every listing

- Same organisation name and the same homepage URL in `server.json` (`websiteUrl`), `smithery.yaml`,
  `manifest.json`, the README byline and the repo About box.
- Link to a page on a domain you own that is specific to the server or its category, not only the
  home page.
- Whether a given directory shows the website or follows the link must be checked per directory
  [unverified]. Open the live listing and look.

## 7. Automate the release [general]

A manual publish drifts out of date. The registry documents a GitHub Actions route using OIDC
[verified: documented, not tested here]. Wire `mcp-publisher publish` into the release job so the
registry version tracks the package version.
