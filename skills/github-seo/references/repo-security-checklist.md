# Repo security and permission checklist

Run by `python3 scripts/check_repo_seo.py owner/repo --security-only`. The skill reports and
recommends. It never changes repo settings: the owner applies fixes in Settings.

Labels: **verified** = primary doc checked 2026-11-13; **observed** = live `gh api` GET on
2026-11-13; **general** = common practice. Sources are under docs.github.com.

## Who can see what

- Admin token: every endpoint below is readable [observed].
- Read-only token: `rules/branches/{branch}`, `rulesets` and `private-vulnerability-reporting`
  return 200. The Actions permission endpoints return 403. `security_and_analysis` is absent from
  the repo object, and `vulnerability-alerts`, `automated-security-fixes`, `secret-scanning/alerts`
  and `pages` return a 404 that cannot be told apart from "off" [observed, 2026-11-13].
- So a 403 or an ambiguous 404 is reported as MANUAL ("could not check, needs admin"), never
  as a pass or a fail.

## Checks

| Check | Command (GET only) | Notes |
|---|---|---|
| Effective rules on a branch | `gh api repos/OWNER/REPO/rules/branches/BRANCH` | Look for `deletion`, `non_fast_forward`, `pull_request`. Includes org rulesets; excludes evaluate and disabled ones [verified: /en/rest/repos/rules]. |
| Rulesets list | `gh api repos/OWNER/REPO/rulesets` | `enforcement` must be `active` [observed]. |
| Legacy branch protection | `gh api repos/OWNER/REPO/branches/BRANCH/protection` | Admin only in practice. 404 "Branch not protected" does not mean unprotected when a ruleset exists [observed]. The doc does not define 404 [verified: /en/rest/branches/branch-protection]. |
| Pages enabled and source | `gh api repos/OWNER/REPO --jq .has_pages` then `gh api repos/OWNER/REPO/pages` | `source.branch` is the publishing branch (any branch, root or /docs) [verified]. The docs do not tell you to protect it, but anyone who can push there can change the live site [general]. Apply deletion and force-push blocking at least. A PR rule can break deploy bots, so it is not required for this branch. |
| Pages via Actions | `gh api repos/OWNER/REPO/pages --jq .build_type` | `workflow`: restrict the `github-pages` environment to the default branch [verified: Pages publishing source doc]. Not readable here, so MANUAL. |
| Secret scanning, push protection, Dependabot security updates | `gh api repos/OWNER/REPO --jq .security_and_analysis` | Free on public repos [verified: /en/code-security/getting-started/github-security-features]. Field only appears for admin [observed]. |
| Dependabot alerts | `gh api -i repos/OWNER/REPO/vulnerability-alerts` | 204 on, 404 "Vulnerability alerts are disabled." off, for admin [observed]. |
| Private vulnerability reporting | `gh api repos/OWNER/REPO/private-vulnerability-reporting` | `{"enabled": bool}`, readable without admin [observed]. Pair with a SECURITY.md. |
| Actions default token | `gh api repos/OWNER/REPO/actions/permissions/workflow` | Want `default_workflow_permissions: read` and `can_approve_pull_request_reviews: false`. Defaults are not documented [verified: /en/rest/actions/permissions]. |
| Fork PR approval | `gh api repos/OWNER/REPO/actions/permissions/fork-pr-contributor-approval` | `approval_policy`: `first_time_contributors_new_to_github` (weakest), `first_time_contributors`, `all_external_contributors` [verified]. |
| Code scanning | `gh api repos/OWNER/REPO/code-scanning/alerts` | 404 "no analysis found" means not set up [observed]. Not scored by the script. |
| CODEOWNERS | `gh api repos/OWNER/REPO/contents/.github/CODEOWNERS` | Optional for solo repos. 404 means absent [observed]. Not scored. |

## Reporting

- Failures first, then warnings, then MANUAL items the owner must check in Settings.
- Recommend, do not apply. Tell the owner the path (Settings, Rules, Rulesets) and the setting.
- Say plainly which checks ran with a read-only token.
