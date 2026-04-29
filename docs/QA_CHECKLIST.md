# QA Checklist

Run this checklist **before** any of the following:

- Making the GitHub repo public.
- Posting the Loom walkthrough on a public channel.
- Sending an outreach message that links to the repo.
- Sending the offer sheet to a buyer.

A failure in any section means **stop and fix before proceeding.**

---

## 1. Repository hygiene

- [ ] `git status` is clean (no uncommitted changes you don't intend
      to ship).
- [ ] `.gitignore` excludes `.env`, `__pycache__/`, `.venv/`, `venv/`,
      `*.pyc`, `.idea/`, `.vscode/`, and any local notes folder.
- [ ] No `.env` file is tracked. (Run `git ls-files | grep -E '^\.env$'`
      and confirm empty output.)
- [ ] No backup files committed (`*.bak`, `*~`, `*.orig`).
- [ ] `requirements.txt` is current and minimal.
- [ ] README renders correctly on GitHub (preview before publishing).

## 2. Public-safety scan

- [ ] `python scripts/check_public_safety.py` exits **0**.
- [ ] If the scan reports warnings, every warning has been read and
      verified harmless. Document why in a commit message.
- [ ] No real API keys anywhere. Spot-check `.env.example`, README,
      docs, and any code files.
- [ ] No real client names, employer names, facility names, vendor
      names, or product names from past work appear anywhere.
- [ ] No real email addresses, phone numbers, or contact info except
      the public contact you intend to publish.

## 3. Synthetic-data verification

- [ ] Every file in `samples/` contains a `SYNTHETIC_DEMO_DATA` marker
      near the top.
- [ ] `samples/README.md` declares the synthetic-only policy.
- [ ] No HL7 message contains a name, MRN, address, phone, DOB, or <!-- noqa: safety -->
      identifier that could be mistaken for a real patient. <!-- noqa: safety -->
- [ ] No log excerpt contains a real server hostname, internal IP,
      database name, or job name from a real environment.
- [ ] Patient names in samples follow `LASTNAME^FIRSTNAME` patterns <!-- noqa: safety -->
      that are obviously synthetic (`SYNTHETIC^DEMO`, `TEST^PATIENT`, <!-- noqa: safety -->
      `SAMPLE^ALPHA`).

## 4. Claims and language

- [ ] README does not say the system "fixes" interfaces. It "assists
      with triage."
- [ ] README does not claim HIPAA, HITRUST, or SOC 2 compliance.
- [ ] README does not promise specific accuracy numbers or success
      rates without qualification.
- [ ] No language implying the system replaces engineers.
- [ ] No language implying the system runs in production unattended.
- [ ] Every "automatic" capability is paired with a human review step.

## 5. Offer sheet review

- [ ] All `[BRACKETED_PLACEHOLDERS]` in `OFFER_SHEET.md` are replaced
      with real values (or intentionally left as a draft and the
      sheet is not yet being sent).
- [ ] Pricing is set. Not "$X-$Y" — a specific number for the
      standard tier.
- [ ] Contact email is real and monitored.
- [ ] Out-of-scope section reflects what you actually will not do.
- [ ] Timeline reflects what you can actually deliver.

## 6. Outreach readiness

- [ ] Templates in `OUTREACH_MESSAGES.md` have been edited for the
      specific recipient. Generic sends do not count as outreach.
- [ ] The Loom is published (unlisted is fine for outreach).
- [ ] The repo is set to the visibility you intended (public vs
      unlisted-share).
- [ ] You have a tracking log set up (plain text or spreadsheet).

## 7. Personal conduct guardrails

- [ ] Nothing in the repo identifies a current or former employer.
- [ ] Nothing in the repo identifies any client of a current or
      former employer.
- [ ] Nothing in the repo references a specific real production
      issue you handled at work.
- [ ] No screenshots from work systems. None.
- [ ] No code copied from a work codebase. None.

## 8. Loom walkthrough

- [ ] Recording was done in a fresh browser profile.
- [ ] No work tabs, work apps, or work notifications appeared on
      screen.
- [ ] No real domains or hostnames visible in any terminal or URL.
- [ ] Audio is clear; mic was tested first.
- [ ] Recording is under 5 minutes.
- [ ] Description and title match the repo's positioning.

## 9. Final gate

- [ ] One full re-read of `README.md` from top to bottom, out loud.
- [ ] One full re-watch of the Loom at 1x speed.
- [ ] One re-run of `python scripts/check_public_safety.py`.
- [ ] One commit with a clean, descriptive message.

If all eight sections pass, you are clear to publish or send.

If any section fails, stop. Fix it. Re-run the checklist. Do not
shortcut this.
