# Demo Data Policy

This repository operates under a **synthetic-data-only** policy. There
are no exceptions.

## The rule

No real protected health information (PHI), no real production logs,
no real patient identifiers, no real facility identifiers, no real <!-- noqa: safety -->
client or employer data, no real provider names, no real device
identifiers, no real interface configurations, ever, under any
circumstance, in any file in this repository or in any artifact
generated from it.

## What synthetic means here

- **Names:** clearly fictional patterns like `SYNTHETIC^DEMO`,
  `TEST^PATIENT`, `SAMPLE^ALPHA`. Never `DOE^JOHN` or `SMITH^JANE` — <!-- noqa: safety -->
  those look real enough to confuse a reviewer.
- **Identifiers (MRN, account, encounter):** prefixes like `DEMO`, <!-- noqa: safety -->
  `SYNTH`, `TEST` followed by short numeric strings. Never a 9-digit
  number that could be mistaken for an SSN. <!-- noqa: safety -->
- **Dates of birth:** stylized clearly fake dates (e.g. `19000101`,
  `20000101`).
- **Phone numbers:** the 555-0100 through 555-0199 range, which is
  reserved for fictional use.
- **Email addresses:** `*@example.com`, `*@example.org`, or
  placeholder-local addresses (`you@…`, `demo@…`, `test@…`).
- **Hostnames / domains:** `example.com`, `example.org`,
  `demo.local`, `localhost`. Never a real internal hostname.
- **Hospital / facility names:** `DEMO HOSPITAL`, `SAMPLE HEALTH
  SYSTEM`. Never a real one.

## Marker

Every file in `samples/` (and any future synthetic data file
elsewhere) **must** include the literal string `SYNTHETIC_DEMO_DATA`
within the first 20 lines. The safety scanner uses this marker to
distinguish legitimate synthetic samples from accidental leakage.

## Where synthetic data may be used

- `samples/` — primary demo inputs.
- `tests/` — if test fixtures are added later, same rules apply.
- README and docs — only when illustrating a small snippet, and the
  snippet must include the marker or be obviously synthetic
  (`SYNTHETIC^DEMO` / `DEMO000001`).

## Where synthetic data must NOT be used

- As a placeholder pretending to be real data in a sales conversation.
  ("Here's an example from a real client" — no.)
- In any way that suggests the prototype has been tested against real
  PHI. It has not, and it is not approved for that use.

## Verification before each release / demo

1. Run `python scripts/check_public_safety.py`. It must exit 0 with
   no error-severity findings.
2. Spot-check one random file in `samples/` and confirm the marker
   is present and the content is obviously synthetic.
3. Spot-check the README for any added snippet that may have
   slipped past the scanner.
4. If a Loom or screenshot is being produced, the same rules apply
   to anything visible on screen.

## What to do if real data accidentally enters the repo

1. **Do not push.** If it has not been pushed, delete it
   immediately, run the scanner again, and verify clean.
2. If it was pushed, treat it as a security incident. Rotate any
   secrets that may have been adjacent. Force-purge from git history
   (`git filter-repo` or BFG). Force-push the clean history.
   Notify yourself that this happened and document the failure mode
   so it does not recur.
3. **Do not** merely add a follow-up commit removing the data. Git
   history retains it. Purge.

## Why this policy is strict

Two reasons:

1. **Legal and ethical.** PHI and confidential business data are not
   yours to publish, even by accident.
2. **Commercial.** A buyer who sees a single real-looking name in
   your demo repo will assume you are careless with theirs.
   Carelessness in a public demo translates directly to "this
   person should not be near my interface engine."

This policy is the cheapest part of being credible. Follow it.
