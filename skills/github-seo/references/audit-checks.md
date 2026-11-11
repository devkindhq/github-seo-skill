# Audit checks

Read-only checks for Step 2 (repo audit) and for after a registry submission (listing checks).
Each `gh` command needs the GitHub CLI logged in. Nothing here changes the repo.

Report each check as pass, warn or fail.

## Repo audit

Read the facts for `owner/repo`:

```bash
gh repo view owner/repo --json nameWithOwner,name,description,homepageUrl,licenseInfo,repositoryTopics,isPrivate
gh api repos/owner/repo/readme -H "Accept: application/vnd.github.raw"
gh api repos/owner/repo/contents/ --jq '.[].name'
gh api "repos/owner/repo/git/trees/HEAD?recursive=1" --jq '.tree[] | select(.type=="blob") | .path'
```

| Check | Fail | Warn |
|---|---|---|
| Description | Empty, or over 350 characters. It is the About text and the search snippet. | Over 120 characters. It can truncate in results. |
| Topics | None set. | Fewer than 5. Add accurate ones. |
| Homepage | | Empty. Point it at the canonical write-up. |
| License | None, or GitHub reports the key `other`. It reads as "do not use this". | |
| README | Missing. | Under 150 words (too thin to rank) or over 700 words (move depth to a write-up). Do not count words in code blocks. |
| README H1 | No H1. | The H1 lacks one or more words of the repo name. Split the name on `-` and `_`, ignore words of 1 or 2 letters, and ignore case. |
| First paragraph | | None after the H1, or over 320 characters. It acts as the search snippet. Skip badges, headings, tables, lists and code. |
| Community files | | `CONTRIBUTING.md` or `SECURITY.md` is missing in the repo root. |
| Retired platforms | A file path or a README line names a platform in the "Retired platforms" table of `mcp-registry-checklist.md`. In a clone, `git grep -n -i <name>` finds the other mentions. | |

Two points no command can check:

- The social preview image cannot be read or set by CLI. Tell the owner: Settings, General,
  Social preview (1280 by 640).
- If `isPrivate` is true, the repo is invisible to search until the owner makes it public.

### When the repo root has a `server.json`

```bash
gh api repos/owner/repo/contents/server.json -H "Accept: application/vnd.github.raw"
```

| Check | Fail | Warn |
|---|---|---|
| `server.json` | Not valid JSON. | |
| `name` | | Does not start with `io.github.<owner>/`. This is fine only with domain auth. |
| `description` | Empty, or over 100 characters. | |
| `websiteUrl` | | Empty. Set the official homepage field. |
| OCI package, when `packages` has one | The root `Dockerfile` is missing, or lacks `LABEL io.modelcontextprotocol.server.name` with the same value as `name`. | |
| npm package, when `packages` has one | `mcpName` in the root `package.json` is missing or differs from `name`. | |

## Listing checks

Run these after a registry submission. Read `name` from `server.json` first. A repo with no
`server.json` has no MCP listing to check.

Fetch each URL and read the HTTP status and the JSON body. A status that the table does not name,
or no response, is a fail:

| Listing | URL | Pass | Otherwise |
|---|---|---|---|
| Official MCP Registry | `https://registry.modelcontextprotocol.io/v0/servers/<name, URL-encoded>/versions/latest` | 200. Note `server.version` and `server.packages`. | Fail: not found. |
| npm package (for each npm entry in `server.packages`) | `https://registry.npmjs.org/<identifier>/latest` | 200, and `version` equals the version of that package entry, or `server.version` when the entry has none. | Warn: the versions differ. Fail: not found. |
| Docker Hub image (for each OCI entry on Docker Hub) | `https://hub.docker.com/v2/repositories/<image>/tags/<tag>` | 200. Take `<image>` and `<tag>` from the identifier without the `docker.io/` prefix, split at `:`. With no tag, use `latest`. With no `/` in the image, put `library/` before it. | Fail: the tag does not exist. Warn: the image is on another host (the first part of the image name has a dot), so check it by hand. |
| Glama | `https://glama.ai/mcp/servers/owner/repo` | 200. | Warn on 404: Glama can list a server under another name, so search glama.ai by hand. |

Check the registry packages, not the `server.json` in the repo, so that the result matches what
clients install.

awesome-mcp-servers:

```bash
gh api repos/punkpeye/awesome-mcp-servers/contents/README.md -H "Accept: application/vnd.github.raw" | grep -i -c "\[owner/repo\]"
gh pr list --repo punkpeye/awesome-mcp-servers --state all --search "owner/repo" --json number,state
```

A count of 1 or more means the list has the repo. If the count is 0, report it as a warn with the
state of each pull request found.

Directories that need a login or have no API stay a manual check: the Claude plugin directory,
mcp.so, mcpservers.org and Cursor Directory.
