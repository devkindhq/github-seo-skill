# Claude plugin directory

Generalised from one real submission at `claude.ai/directory/manage` on 2026-11-02
[observed, 2026-11-02]. The portal and its checks change, so re-check each step before
repeating this. Anything not seen during the run is marked [unverified].

## Prerequisites

- A paid claude.ai plan [observed, 2026-11-02]. On Team and Enterprise, the submitter needs the
  Owner role or, on Enterprise, a custom role with the Directory permission [verified, 2026-11-02,
  claude.com/docs/directory/publish.md].
- A GitHub repo with `.claude-plugin/plugin.json` [observed, 2026-11-02]. The repo can stay
  private while you validate and submit, but must be public before the listing goes live
  [verified, 2026-11-02, claude.com/docs/plugins/submit.md].
- A GitHub account with push access to the repo, used by the submitter [observed, 2026-11-02],
  and connected on claude.ai in the submitting organisation [verified, 2026-11-02, same page].
- The listing belongs to the organisation you submit from. Submit from the organisation that
  should own it long term [verified, 2026-11-02, claude.com/docs/directory/publish.md].
- Limits: at most 10 submissions per organisation per 24 hours (drafts and withdrawn
  submissions count), and one submission per repo and folder [observed, 2026-11-02].

## The five steps

1. **Source.** In the portal, select Submit new, then Plugin bundle [verified, 2026-11-02,
   claude.com/docs/plugins/submit.md]. Point the portal at the repo and folder.
2. **Listing details.** Name, description, icon and related listing fields.
3. **Data handling.** Questions on personal data, whether the plugin sends data to other
   services (declare this in the README), retention, and users under 18 [observed, 2026-11-02].
4. **Compliance.** Four acknowledgements: the Directory Terms and Policy, accuracy of the privacy
   policy, no credential exfiltration, and consent to be contacted. The submitter ticks these
   personally. An agent must not tick them on the owner's behalf.
5. **Review and submit.** An automated scan runs first. Held items go to a human reviewer.
   Approval is not guaranteed, and no review-time estimate was shown [observed, 2026-11-02].

## Prepare the plugin

- The plugin folder is the folder that holds `.claude-plugin/plugin.json`, and installers get that
  whole folder [verified, 2026-11-03, claude.com/docs/plugins/pre-submission-checklist.md]. If it
  is the root of a repo that also holds the server's `package.json` and `yarn.lock`, every install
  shows a note that the listed packages were not installed, because plugin installs do not support
  yarn or pnpm lockfiles [observed, 2026-11-03, `claude plugin list`]. A server that runs from
  npm through `npx` never uses those packages, so the note does not affect it [general].
- Set `displayName`, and set `icon` to a path inside the plugin, such as `./assets/icon.png`. The
  directory reads `icon`, `documentationUrl`, `supportUrl`, `privacyPolicyUrl` and
  `termsOfServiceUrl` from `plugin.json` only [verified, 2026-11-03,
  code.claude.com/docs/en/plugins-reference].
- Add a README "Network access and data" section: what the plugin downloads, which hosts it calls,
  what each request carries and what it stores. The checklist asks the README to describe
  everything the plugin runs, sends or fetches [verified, 2026-11-03, pre-submission checklist].
- Run `claude plugin validate .` in the plugin folder before you push. It checks syntax and schema
  only, so the portal's Validate still runs [verified, 2026-11-03, pre-submission checklist].

## Validate

Validate runs 7 checks and reports three kinds of result: Blocking findings, policy holds and
warnings [observed, 2026-11-02]. It is commit-specific, so re-run it after every push that
touches a fix [observed, 2026-11-02].

| Trigger seen | Result | Fix that cleared it |
|---|---|---|
| A doc telling users to run `$(gh auth token)` | Policy hold, "Uses a credential from the user's machine" | Tell users to supply their own token |
| An `npx ... add` install line in the README | Non-blocking "download-and-execute" warning (cause inferred, [unverified]) | Add a README "Network access and data" section |
| Missing `.claude-plugin/icon.png` | Warning | Add the icon |
| No display name or marketplace description | Listing fields incomplete | Add `displayName` in `plugin.json` and `description` in `marketplace.json` |

All rows [observed, 2026-11-02].

### Documented rules for packages and files

From claude.com/docs/plugins/pre-submission-checklist.md [verified, 2026-11-02]:

| Rule | Result if broken |
|---|---|
| Pin every package a launcher runs to an exact version, such as `npx <pkg>@1.2.3` | Blocks, "Unpinned npx launcher" |
| A launcher with an exact pin | Still held for a reviewer, "Runs a pinned npx or uvx package" |
| `.npmrc` or another file that sets a registry or package source, in a plugin with a launcher | Blocks |
| `package.json` beside `package-lock.json`, `npm-shrinkwrap.json`, `bun.lock` or `bun.lockb` in the plugin folder root | Held for a reviewer, "Dependencies install from a lockfile". `yarn.lock` is not on the list |
| Keep every file that is not an image or font under 256 KiB | Held for a reviewer |
| Keep the plugin to 512 files or fewer | Held for a reviewer |

### Scanner false positives (second submission, 2026-11-02)

Two more plugins went through Validate on 2026-11-02. The scanner reads text in skills and
READMEs, not only code, so documentation can trigger holds [observed, 2026-11-02].

| Trigger seen | Result | What happened |
|---|---|---|
| A skill doc example reading `process.env.X_API_KEY` next to a `fetch()` | Two policy holds, "Uses a credential from the user's machine" | Cleared after the example read was rewritten as pseudocode and the variable renamed [observed, 2026-11-02] |
| The English word "pass" in skill prose, such as "a later pass can reference" | Same credential hold, worded as reading the installer's "pass" (the `pass` password manager), paired with a documented `curl` upload | Rewording one instance surfaced the next. The scanner reports one hit per run, and the word appears in dozens of skill bodies. Left for reviewer confirmation [observed, 2026-11-02] |
| Many example images (66 files) in the repo | Policy hold, "Image or font file that the plugin's code could run" | Not fixable without removing or relocating the images, so the plugin goes to a reviewer [observed, 2026-11-02] |
| Docs saying to run a `curl` command that a tool returns, and some PNG files | Non-blocking "download-and-run" warning | Doc-only mentions need no change per the portal. Only PNGs were flagged, not the WebP files. Converting five flagged PNGs to WebP was tried; whether that clears the warning is [unverified] |

Each hold on a skill-text false positive can be left for reviewer confirmation instead of
being chased, when the plugin is going to a reviewer anyway [general].

Icon: square PNG or JPEG, 512 to 2048 px, under 2 MB. It reportedly locks on first save or
submit, so get it right before then [observed, 2026-11-02; the lock behaviour is reported, not
tested, so treat it as [unverified]].

## Publishing and updates

The review step offers an auto-publish toggle. Two update modes were shown [observed, 2026-11-02]:

- **Push webhook (recommended by the portal).** After submit, the portal gives a URL and a
  secret. In the repo, go to Settings, Webhooks, add the URL, set content type to
  `application/json`, and select push events only. This needs repo admin rights. Never paste the
  secret into chat or commit it.
- **Scheduled check**, about every 6 hours.

## Other routes

- `anthropics/claude-plugins-official` is by partner contact only [observed, 2026-11-02].
- Your own `marketplace.json` lets users run `/plugin marketplace add <owner>/<repo>` [general].
- A skills.sh listing is automatic, built from `npx skills add` telemetry [observed, 2026-11-02].
- `/plugin install <name> --marketplace <owner>/<repo>` adds the marketplace and installs in one
  step. It needs Claude Code v2.1.275 or later [verified, 2026-11-02,
  code.claude.com/docs/en/plugins/publish.md].
- The directory no longer accepts desktop extension (MCPB) listings. Ship a local MCP server
  inside a plugin bundle instead [verified, 2026-11-02, claude.com/docs/directory/publish.md].
