#!/usr/bin/env python3
"""Read-only check of an MCP server's public listings. Usage: check_listings.py owner/repo

Reads the server name from server.json in the repo with the GitHub CLI (`gh`), then checks the
Official MCP Registry, the package it points at (npm or Docker Hub), Glama and awesome-mcp-servers.
Makes no changes. Exits 1 if any check fails.
"""
import base64
import json
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

if len(sys.argv) != 2 or "/" not in sys.argv[1]:
    sys.exit(__doc__)
slug = sys.argv[1]
results = []


def gh(*args, required=False):
    out = subprocess.run(["gh", *args], capture_output=True, text=True)
    if out.returncode == 0:
        return out.stdout
    if required:
        sys.exit(f"gh {' '.join(args)} failed: {out.stderr.strip()}")
    return None


def get(url):
    """Return (status, body). A 404 is a result, not an error; status 0 means no response."""
    req = urllib.request.Request(url, headers={"User-Agent": "github-seo-skill"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, ""
    except urllib.error.URLError as e:
        return 0, str(e.reason)


def record(level, name, detail):
    results.append((level, name, detail))


gh("repo", "view", slug, "--json", "name", required=True)
raw = gh("api", f"repos/{slug}/contents/server.json", "--jq", ".content")
if not raw:
    sys.exit(f"{slug} has no server.json in the default branch, so there is no MCP listing to check.")
try:
    name = json.loads(base64.b64decode(raw))["name"]
except (ValueError, KeyError):
    sys.exit(f"{slug}: server.json is not valid JSON or has no name")

# Official MCP Registry. Search results are paged, so ask for the latest version directly.
status, body = get(
    f"https://registry.modelcontextprotocol.io/v0/servers/{urllib.parse.quote(name, safe='')}/versions/latest"
)
live = json.loads(body)["server"] if status == 200 else {}
if live:
    record("PASS", "Official MCP Registry", f"{name} {live['version']}")
else:
    record("FAIL", "Official MCP Registry", f"{name} not found (HTTP {status})")

# Packages in the live registry entry, so the check matches what clients install
for pkg in live.get("packages", []):
    kind, ident = pkg.get("registryType"), pkg.get("identifier", "")
    if kind == "npm":
        status, body = get(f"https://registry.npmjs.org/{urllib.parse.quote(ident, safe='@')}/latest")
        if status != 200:
            record("FAIL", "npm", f"{ident} not found (HTTP {status})")
        else:
            npm_v = json.loads(body)["version"]
            want = pkg.get("version") or live["version"]
            record("PASS" if npm_v == want else "WARN", "npm", f"{ident} {npm_v}, registry {want}")
    elif kind == "oci":
        image, _, tag = ident.removeprefix("docker.io/").partition(":")
        if "/" not in image:
            image = f"library/{image}"
        if "." in image.split("/")[0]:
            record("WARN", "OCI image", f"{ident} is not on Docker Hub. Check it by hand.")
            continue
        status, _ = get(f"https://hub.docker.com/v2/repositories/{image}/tags/{tag or 'latest'}")
        record("PASS" if status == 200 else "FAIL", "Docker Hub tag", f"{ident} (HTTP {status})")

# Glama
status, _ = get(f"https://glama.ai/mcp/servers/{slug}")
record("PASS" if status == 200 else "FAIL", "Glama", f"https://glama.ai/mcp/servers/{slug} (HTTP {status})")

# awesome-mcp-servers: listed in the README, or a pull request for the repo
listed = gh("api", "repos/punkpeye/awesome-mcp-servers/contents/README.md", "-H", "Accept: application/vnd.github.raw")
if listed and f"[{slug}]".lower() in listed.lower():
    record("PASS", "awesome-mcp-servers", "listed in README")
else:
    prs = gh("pr", "list", "--repo", "punkpeye/awesome-mcp-servers", "--state", "all", "--search", slug,
             "--json", "number,state")
    if prs is None:
        detail = "pull request search failed"
    else:
        detail = ", ".join(f"#{p['number']} {p['state']}" for p in json.loads(prs)) or "no pull request found"
    record("WARN", "awesome-mcp-servers", f"not listed; {detail}")

width = max(len(n) for _, n, _ in results)
for level, n, d in results:
    print(f"{level:<5} {n:<{width}}  {d}")
print("\nMANUAL  Claude plugin directory, mcp.so, mcpservers.org and Cursor Directory need a login or have no API.")
sys.exit(1 if any(level == "FAIL" for level, _, _ in results) else 0)
