# Outreach Messages

Templates for cold outreach to healthcare integration leads. Edit
every one before sending. Templates that read like templates get
deleted.

Replace bracketed placeholders with the recipient's actual context.
Send only when the safety scanner passes and the Loom is published
(unlisted is fine).

---

## Voice and rules

- Short. The reader has 12 seconds.
- Specific to their environment. If you can't be specific, don't send.
- One ask per message. Most of the time the ask is a 20-minute call.
- No "I'd love to" or "circle back" or "synergy". Talk like a person.
- No fake compliments. No "I've been a huge fan of your work."
- If you don't actually have a Mirth/HL7 background and a working
  repo, do not send these. Outreach without proof is a waste of
  everyone's day.

---

## 1. Cold LinkedIn message (≤ 300 chars)

> Hi [Name] — I built a small prototype that helps integration teams
> triage Mirth/HL7 errors faster. Synthetic data only, human-in-loop.
> Repo + 4-min walkthrough here: [link]. Curious whether the workflow
> would map to what your team sees. Open to a 20-min call?

Variant if they posted recently about HL7/integration pain:

> [Name] — saw your post about [specific topic]. Built a triage
> workflow prototype aimed at exactly that. Mirth-flavored, synthetic
> samples, human-in-the-loop. Walkthrough: [link]. Worth a 20-min
> call to compare notes?

## 2. Cold email — to an integration lead at a hospital, health system, or vendor

Subject: `Mirth/HL7 triage workflow — 4-min look`

> Hi [Name],
>
> I work in healthcare integration and built a workflow prototype
> aimed at the slow part of HL7 error triage — getting from raw
> message + log to a clear hypothesis. The repo and a 4-minute
> walkthrough are here: [link].
>
> Quick context:
>
> - Synthetic data only. No PHI. Demo-safe.
> - Human-in-the-loop. The model proposes; an engineer decides.
> - Designed for tier-1/tier-2 integration responders, not as a
>   replacement for them.
>
> If your team spends meaningful time triaging interface errors, I'm
> running a fixed-scope audit using this workflow against redacted
> samples teams send me. Five to seven business days. Walkthrough
> call included. Offer sheet is in the repo at `docs/OFFER_SHEET.md`.
>
> Worth 20 minutes to see if it maps to what you're seeing?
>
> — [your name]
> [your phone or scheduling link]

## 3. Follow-up (7–10 days later, only once)

Subject: `Re: Mirth/HL7 triage workflow — 4-min look`

> Hi [Name] — bumping this in case it got buried. No pressure either
> way; if it's not a fit, a one-word reply ("not now" / "not a fit")
> is genuinely useful. — [your name]

That's the whole follow-up. Resist the urge to add anything.

## 4. Reply when someone shows interest

> Thanks [Name]. Quick question before we book time: which engine,
> roughly what message volume per day, and what's the failure class
> that costs you the most hours right now? I'll come to the call
> with relevant examples from the redacted-samples library.
>
> Here are some times that work this week: [times].
>
> — [your name]

## 5. Referral ask — to a peer who isn't the buyer but knows the buyer

> Hi [Name] — quick ask. I'm doing fixed-scope HL7/Mirth triage
> audits for integration teams. Synthetic-data, human-in-the-loop,
> short engagement. Anyone in your network worth introducing? Happy
> to share the offer sheet first so you can vet it before passing
> it on. — [your name]

## 6. Reply to "what makes you different from [tool X]"

> Fair question. Three differences:
>
> 1. This is a workflow prototype, not a product trying to replace
>    your engineers. The deliverable is a structured workflow your
>    team owns afterward.
> 2. It's human-in-the-loop by design. Nothing auto-applies. The
>    output is hypotheses + evidence + validation steps.
> 3. It runs on synthetic data only. I never receive PHI.
>
> If [tool X] is solving the problem, you don't need me. If it's
> not, the audit is a low-commitment way to find out whether a
> workflow change would help.

## 7. Reply to "this sounds too small / too cheap"

> Intentional. This is a fixed-scope audit, not a multi-month
> engagement. The point is to give your team a usable artifact in
> a week, not to land a retainer. If after the audit there's a
> bigger piece of work that makes sense, we can talk about that
> separately.

## 8. Reply to "we already have this covered"

> Got it. If your situation changes — or if you know another
> integration team that'd benefit — the offer sheet is at [link].
> Appreciate the response.

---

## Anti-templates: what NOT to send

- "Just checking in!" (Don't.)
- "Following up on my previous email." (You followed up once. Stop.)
- "I see you're a [title] at [company], so I thought you might be
  interested in…" (Says nothing. Delete.)
- Anything that mentions a real client, employer, or facility you've
  worked with by name. The repo and your story are PHI- and
  client-clean. Outreach has to be too.

---

## Tracking

Keep a simple log. Plain text or a spreadsheet. Not a CRM yet.

```
date | name | org (general type) | channel | message # | response | next step
```

Generic org types only ("regional health system", "RCM vendor",
"clearinghouse"). Don't write down real org names in any file that
lives in this repo.
