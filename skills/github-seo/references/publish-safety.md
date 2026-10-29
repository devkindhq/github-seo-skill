# Publish safety: what going public costs, and the checks to run

Run these checks on every repo, every time, before the first public push.

## What publishing costs

1. **Decisions become public.** If you publish a recommendation and later reverse it, the reversal
   is visible. Publish measurements and the reasoning, framed as conditional on the numbers. A
   benchmark that updates when the numbers change is credible; a manifesto that flip-flops is not.
   This is the argument for shipping a re-runnable harness rather than a static opinion.
2. **Others save the effort you spent.** Anyone reading a published comparison skips the work of
   producing it. Usually the scarce asset is the delivery capacity around the knowledge, not the knowledge itself. Weigh the specific case.
3. **A fact is not a method.** Publishing a fact (a benchmark number, a starter template) is
   different from publishing a method (a full internal delivery pipeline). The method is closer to
   a competitive asset. Decide which one the repo is before it goes public.

## A reasonable default line (re-decide per project)

- **Publish freely:** reproducible measurements, benchmark harnesses, methodology write-ups, clean starter templates.
- **Publish deliberately:** scaffolds and plugins meant to be copied, with long-form docs on your own domain and the repo as the supporting artifact.
- **Do not publish:** anything containing client-specific configuration, or an internal end-to-end delivery pipeline you consider an asset. Never link a client's production repo. Extract the general finding as a measurement or template instead.

The public or private decision belongs to the repo owner. When in doubt, stop and ask.

## Mandatory checks

1. **Full-history secret scan.** The current tree is not enough.

   ```bash
   gitleaks detect --source . -v
   ```

   Without gitleaks, a minimum grep over history:

   ```bash
   git log -p | grep -Ei '(sk-[a-zA-Z0-9]{20,}|AIza[0-9A-Za-z_-]{20,}|ya29\.[0-9A-Za-z_-]+|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|password\s*=|secret\s*=|token\s*=)'
   ```

2. **Client-identifying content.** Search for client names, store domains, internal ticket keys,
   API details tied to a client's setup, and personal data about contractors or staff.
3. **Live-defect check.** If a finding implies an unfixed bug in someone's shipping product, fix it
   first. Publishing a benchmark that documents it is a bad look even without naming the client.
4. **If a secret was ever committed,** rotate it, then start the public repo from a fresh history.
   Deleting the file is not enough.
5. **Start fresh when in doubt.** Initialise the public repo from a clean copy with a single
   initial commit rather than flipping a long-lived private repo to public.
