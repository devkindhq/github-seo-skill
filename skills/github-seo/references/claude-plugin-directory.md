# Claude plugin directory

Generalised from one real submission at `claude.ai/directory/manage` on 2026-11-02
[observed, 2026-11-02]. The portal and its checks change, so re-check each step before
repeating this. Anything not seen during the run is marked [unverified].

## Prerequisites

- A paid claude.ai plan [observed, 2026-11-02].
- A public GitHub repo with `.claude-plugin/plugin.json` [observed, 2026-11-02].
- A GitHub account with push access to the repo, used by the submitter [observed, 2026-11-02].
- Limits: at most 10 submissions per organisation per 24 hours (drafts and withdrawn
  submissions count), and one submission per repo and folder [observed, 2026-11-02].

## The five steps

1. **Source.** Point the portal at the repo and folder.
2. **Listing details.** Name, description, icon and related listing fields.
3. **Data handling.** Questions on personal data, whether the plugin sends data to other
   services (declare this in the README), retention, and users under 18 [observed, 2026-11-02].
4. **Compliance.** Four acknowledgements: the Directory Terms and Policy, accuracy of the privacy
   policy, no credential exfiltration, and consent to be contacted. The submitter ticks these
   personally. An agent must not tick them on the owner's behalf.
5. **Review and submit.** An automated scan runs first. Held items go to a human reviewer.
   Approval is not guaranteed, and no review-time estimate was shown [observed, 2026-11-02].

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
