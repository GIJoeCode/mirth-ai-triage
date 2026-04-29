# Healthcare Integration Triage Audit — Offer Sheet

A fixed-scope, fixed-fee audit for healthcare integration teams running
Mirth Connect (or a comparable HL7 v2 interface engine). The deliverable
is a written triage workflow review and a prioritized improvement list
your team can act on the same week.

> Replace the bracketed placeholders below with your final numbers
> before you publish or send this sheet to a buyer.

---

## Who this is for

- Integration teams running Mirth Connect, Rhapsody, Cloverleaf, or
  similar HL7 v2 engines.
- Healthcare IT leaders whose team spends significant time triaging
  interface errors, dead-letter queues, or "stuck message" tickets.
- Vendors and clearinghouses with HL7 inbound feeds who want a third
  set of eyes on how errors are being categorized and routed.

If you do not have an HL7 v2 footprint, this offer is not for you.

## What you get

A written audit report covering:

1. **Triage workflow map.** How errors currently move from detection to
   resolution at your team. Where time is lost.
2. **Severity-rating consistency check.** Whether the same kind of
   error gets the same priority twice, or whether it depends on who
   sees it first.
3. **Root-cause taxonomy.** A draft taxonomy of the recurring failure
   classes in your environment, drawn from the redacted samples you
   provide.
4. **Remediation playbook outline.** For the top failure classes, a
   plain-language playbook a tier-1 responder can follow without
   paging an engineer.
5. **Human-review checklist.** A concise per-incident checklist your
   team can adopt as-is.
6. **Tooling assessment.** Where AI assistance can plausibly help and
   where it cannot. Honest. No magic.
7. **Risks and gotchas.** Things I notice in the redacted samples that
   warrant attention beyond the audit scope.

You also get a 45-minute walkthrough call where I present the report
and answer questions.

## How it works

1. **Intake call (30 min).** We confirm scope, agree on what counts as
   "in" and "out", and exchange a redaction guide.
2. **You send redacted samples.** A handful of HL7 messages and Mirth
   error log excerpts that represent your top failure modes. All PHI
   removed by you before sending. I provide a redaction checklist so
   nothing accidentally slips through.
3. **I run the audit.** Using the workflow described in this repo, I
   produce the report.
4. **Walkthrough call (45 min).** I present findings. You ask
   questions. You leave with the report and the playbook outline.
5. **One follow-up exchange.** A single round of written
   clarifications via email, within 14 days of delivery.

## Timeline

- **Intake to delivery:** [5–7 business days] for the standard scope.
- **Walkthrough call:** scheduled within [3 business days] of delivery.
- **Follow-up window:** [14 days] from delivery.

## Pricing

- **Standard audit:** $[1,500–3,500]
- **Extended audit** (more sample volume, more interfaces, additional
  workflow review): $[3,500–7,500]

Final price is confirmed in writing after the intake call. No surprises.

## What is explicitly out of scope

- Touching your production Mirth Connect server.
- Reading any non-redacted PHI.
- Connecting to your databases, SFTP servers, or VPNs.
- Recommending vendor selection or procurement decisions.
- Compliance certification of any kind (HIPAA, HITRUST, SOC 2).
- Implementing the recommendations. (Implementation is a separate
  engagement.)

## Safety constraints I work under

- I never receive PHI. If a sample arrives unredacted, I delete it and
  ask for a clean version.
- I never claim AI guarantees. The prototype this audit draws on is
  human-in-the-loop by design. See `docs/SAFETY_MODEL.md`.
- I do not auto-apply anything. Every recommendation is for your team
  to evaluate and decide on.

## How to start

Email **[your_email_here]** with a short note about your environment
(engine, message volume, top pain point) and I'll send back available
intake slots and the redaction checklist.

---

*Last updated: [DATE]*
