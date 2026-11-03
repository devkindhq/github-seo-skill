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

npm timing: the registry checks that the exact version exists on npm. Right after `npm publish`
it can reject the version with "NPM package '...' exists, but version 'X' was not found (status:
404). A newly published release can take a moment to appear..." [verified, 2026-11-02, registry
`internal/validators/registries/npm.go`]. Publish to the registry only after
`npm view <pkg>@<version>` returns the version. The version became visible about one minute
after publish [observed on a Devkind npm MCP server, 2026-11-02].

OCI details [verified]: supported hosts are Docker Hub, `ghcr.io`, Google Artifact Registry,
`*.azurecr.io` and `mcr.microsoft.com`. The `identifier` is `registry/namespace/repository:tag`
(a digest also works). Pin a version tag, not `latest`. Put the `LABEL` in the Dockerfile and
rebuild before the final push, because the label has to be in the pushed image.

OCI route end to end [verified, 2026-11-02, observed from real runs]:

1. Add `LABEL io.modelcontextprotocol.server.name="<server.json name>"` to the Dockerfile.
2. Build multi-arch and push, using a `docker-container` builder:
   `docker buildx build --builder <builder> --push --platform linux/amd64,linux/arm64 -t <ns>/<img>:<ver> -t <ns>/<img>:latest .`
3. Verify with `docker buildx imagetools inspect <ns>/<img>:<ver>`. Extra `unknown/unknown`
   entries are buildx provenance and SBOM attestations, not platforms. Check the label on each
   platform with `--format '{{json .Image}}'`.
4. Smoke test: pull the image and import the server module.
5. Only then run `mcp-publisher publish`.

Order: make the repo public first, push the image second, publish third. The `server.json`
`identifier` still pins the version tag even though `latest` is also pushed.

## 2. Namespace and auth [verified]

- GitHub login gives `io.github.<user-or-org>/<name>`. Org-owned entries are live in
  the registry [observed], so org namespaces work in practice.
- Domain auth (DNS TXT record or an HTTP file at `/.well-known/mcp-registry-auth`) gives a
  reverse-DNS name such as `com.example.*/<name>`.
- `mcp-publisher login github` is an interactive device-code flow. The repo owner runs it.
- Org namespace gotcha [verified, 2026-11-02, observed from a real run]: the device flow grants
  only the user's personal namespace. Publishing `io.github.<org>/<name>` returned 403 with
  "You have permission to publish: io.github.<user>/*". The fix that worked was logging in with
  a GitHub token that has the `read:org` scope, as a user who is an org Owner or admin. Run
  `mcp-publisher login --help` for the token option, and supply the token yourself so it is never
  printed or pasted. Alternative: the GitHub Actions OIDC route (section 7).
  Never paste a token into a chat.
- `mcp-publisher` has no `validate` command [verified, 2026-11-02]. Its commands are `init`,
  `login`, `logout`, `publish` and `status`. The registry validates on publish, and the 100 char
  description limit is enforced by the schema.

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
| `_meta` | Vendor extension | Only `io.modelcontextprotocol.registry/publisher-provided` is kept, max 4096 bytes of JSON. Put author and website here as a bonus, not instead of `websiteUrl`. |

Observed gap: a live entry that put the website only under `_meta` and left `websiteUrl` empty
[observed, 2026-10-31]. Whether downstream directories display `_meta` is unknown, so fill both.

`_meta` limit [verified, 2026-11-02, registry `internal/validators/validators.go`
`validatePublisherExtensions` and `docs/reference/server-json/official-registry-requirements.md`]:
the registry drops every other `_meta` key, and fails the publish when the publisher-provided
object exceeds 4 KB, with "publisher-provided extension exceeds 4KB limit (N bytes)". A full
tool-name list can pass that limit. A 125-tool server failed at 4474 bytes [observed on a Devkind
npm MCP server, 2026-11-02]. Keep the tool list out of `_meta` for a large server.

Environment variables go in `packages[].environmentVariables` with `name`, `description`,
`isRequired` and `isSecret`. Names only, never values.

Verify after publishing:

```bash
curl -s "https://registry.modelcontextprotocol.io/v0.1/servers?search=<your-server-name>"
```

A good result shows status `active`, `isLatest` true and `websiteUrl` populated [verified,
2026-11-02, observed from a real run].

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

Generate every README install block (standard config, Cursor deeplink, per-client blocks) from
one script so they stay consistent [general]. Hand-edited copies drift.

Docker-only servers: the standard config is
`{"command":"docker","args":["run","--rm","-i","<image>:<tag>"]}`. Add resource limits only if the
server needs them.

## 5. Repo files that feed listings

| File | Feeds | Notes |
|---|---|---|
| `server.json` | Official MCP Registry | Section 3. Commit it to the repo root. |
| `smithery.yaml` | Nothing now | Smithery stopped hosted deploys on 31 Oct 2026. Do not add or update this file [verified, 2026-11-02, smithery.ai/future]. |
| `manifest.json` | MCPB bundle, desktop installs | Carries `author` with name and URL, `repository`, and `user_config` prompts for credentials [observed]. |
| README badges | Humans | "Built by <org>" badge linking to the homepage. |

Keep one source of truth for the description, tool list and homepage, and copy it into each file.
A version drift between `package.json`, `server.json` and `manifest.json` is easy to introduce
[observed: one repo had `1.1.0` in two files and `1.0.9` in the third].

## 6. Make the org visible in every listing

- Same organisation name and the same homepage URL in `server.json` (`websiteUrl`),
  `manifest.json`, the README byline and the repo About box.
- Link to a page on a domain you own that is specific to the server or its category, not only the
  home page.
- Whether a given directory shows the website or follows the link must be checked per directory
  [unverified]. Open the live listing and look.

## 7. Automate the release [general]

A manual publish drifts out of date. The registry documents a GitHub Actions route using OIDC
[verified: documented, not tested here]. Wire `mcp-publisher publish` into the release job so the
registry version tracks the package version.

## 8. Docker MCP Registry, a second distribution route

`docker/mcp-registry` lists containerised servers for Docker's MCP tooling. Facts below are from
its `CONTRIBUTING.md` [verified, 2026-11-02]: https://github.com/docker/mcp-registry/blob/main/CONTRIBUTING.md

- Open a PR that adds `servers/<name>/server.yaml`. `task wizard` or `task create` generate it.
- `server.yaml` pins a source commit SHA (`source.project` and `source.commit`).
- Every PR needs a review from the Docker team, and CI must pass.
- Without `--image`, Docker builds and hosts the image under its `mcp/` namespace, with
  signatures, provenance and SBOMs. With `--image <org>/<img>`, your own image is used and
  those extras do not apply.
- The contributing guide asks that the server license allow consumption (MIT or Apache 2 named as
  good, GPL as not).
- Review turnaround and listing criteria beyond the above are [unverified].

## 9. Scrubbing a leaked repo history

If the secret scan finds leaks in history and the token lacks `delete_repo`
[verified, 2026-11-02, observed from a real run]:

1. Rename the old repo.
2. Create a new repo under the original name.
3. Push only `main`. Do not mirror refs, because leaked content can sit in `refs/pull/*`.
4. Re-scan the new repo with `gitleaks`.
5. Have the owner delete the old repo in the GitHub UI.

Rotate any leaked credential regardless. History scrubbing does not un-leak it.

## 10. Earn mentions with a closing "who built this" section [general]

End the README with a short, related and non-pushy section that tells readers who maintains the
server and where to get help or related work. It earns a branded mention and a link back from every
directory that renders the README. Keep it specific to the server's audience, not generic.

- Heading that names the reader's need, for example "Need this wired into your stack?".
- Two or three sentences on what you or your organisation offers that relates to the server.
- One link to a specific page on a domain you own (a services, consulting or product page, not
  only the home page) plus a contact address.
- Request each linked URL first and confirm it returns 200.
- Use the same organisation name and homepage as in `server.json` and the About box.
