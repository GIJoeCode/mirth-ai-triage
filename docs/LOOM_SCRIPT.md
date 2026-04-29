# Loom Walkthrough Script

A 3–5 minute screen recording that turns this repo into a credible
demo. Read the script casually; do not perform it. The goal is "this
person knows what they're doing and isn't selling snake oil."

Aim for **4 minutes**. Cut anything that doesn't earn its time.

---

## 0:00–0:15 — Hook

> "Hi, I'm [your name]. If your team runs Mirth Connect and spends
> hours every week triaging HL7 interface errors, this is a 4-minute
> look at a workflow prototype I built for that exact problem. No PHI,
> no magic, no auto-fixers. Just a structured way to get to a
> hypothesis faster."

Switch to screen share. Show the GitHub repo landing page.

## 0:15–0:45 — What this is (and isn't)

> "Quick framing. This is a prototype of an AI-assisted triage
> workflow. Everything in this repo runs on synthetic data. The
> samples are clearly labeled. The model proposes — a human decides.
> That's the core of the safety model and it's documented right here
> in the repo."

Click into `docs/SAFETY_MODEL.md`. Scroll for two seconds. Click back.

## 0:45–1:30 — The problem

> "If you've worked an integration queue, you know the pattern. An
> interface throws an error. A ticket gets opened. A tier-1 responder
> looks at the message, looks at the log, and either resolves it or
> escalates. The slow part is usually not the fix — it's the path
> from raw error to clear hypothesis. Especially when the same kind
> of error keeps showing up under different surface symptoms."

> "This prototype is aimed at that path."

## 1:30–3:00 — Demo

Open the demo. Point at one synthetic HL7 message. One synthetic
Mirth-style error log.

> "Here's a synthetic ORU message that fails validation. Here's a
> synthetic Mirth log entry. The workflow takes both, and produces
> four things."

Walk through, showing each:

1. **Structural observations.** "Segment X is malformed because of Y."
2. **Severity rating with reasoning.** "I'd rate this major because…"
3. **Ranked root-cause hypotheses with evidence.** "Most likely:
   sender truncated the OBX field. Alternate: schema mismatch. Less
   likely: encoding issue."
4. **Validation steps.** "To confirm hypothesis 1, run X. To rule out
   hypothesis 2, check Y."
5. **Human-review checklist.** "Items the responder confirms before
   escalating or closing."

Pause on the checklist. Point at it.

> "Notice what isn't here. There's no 'apply fix' button. There's no
> auto-route. Nothing leaves this environment. The output is a
> structured starting point for a human responder, not a substitute
> for one."

## 3:00–3:45 — Why this matters for buyers

> "If you're an integration lead, what you actually want is a faster
> path from 'something broke' to 'I know what I'm escalating'. That's
> what this workflow is optimized for."

> "I'm offering a fixed-scope audit using this workflow against your
> redacted samples. You send a handful of redacted HL7 messages and
> Mirth log excerpts. I send back a triage workflow review, a
> root-cause taxonomy of your top failure classes, and a human-review
> checklist your team can adopt. Five to seven business days.
> Walkthrough call included."

> "The full offer sheet is in `docs/OFFER_SHEET.md`."

## 3:45–4:00 — CTA

> "If this looks useful, my email is in the README. Send me a note
> about your environment — interface engine, rough message volume,
> top pain point — and I'll send back the intake slots and a
> redaction checklist."

> "Thanks for watching."

End on the GitHub repo landing page. Stop recording.

---

## Recording checklist

Before you hit record:

- [ ] Browser zoom is at 110–125% so text is readable.
- [ ] Close every tab that isn't the repo and the demo.
- [ ] Close every desktop notification source (Slack, email,
      Teams, Signal). Do this for real.
- [ ] No employer Slack, no employer email, no employer
      anything visible anywhere on screen.
- [ ] Wallpaper is neutral. Dock/taskbar is clean.
- [ ] Run `python scripts/check_public_safety.py` one more time.
      Pass before you record.
- [ ] Demo terminal window has no history showing real keys
      or real domains. Open a fresh one.
- [ ] Microphone test, then a 30-second take-one to check
      levels. Do not use the take-one as the final.

After recording:

- [ ] Watch the full thing at 1x. Anything visible on screen
      that shouldn't be? Re-record.
- [ ] Title: "Mirth AI Triage — workflow prototype walkthrough
      (4 min)".
- [ ] Description: 1 sentence + repo link + offer sheet link.
- [ ] Privacy: unlisted, then share the link directly. Public
      only after the QA checklist is signed off.
