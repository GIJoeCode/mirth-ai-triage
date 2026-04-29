# Safety Model

This document describes the human-in-the-loop safety model that governs
`mirth-ai-triage`. It is the most important document in the repo. Every
feature, demo, and consulting engagement built on this prototype must
respect it.

## Core principles

1. **The model proposes. A human decides.** The system suggests
   hypotheses, severity scores, and remediation steps. It does not apply
   fixes. It does not commit changes. It does not re-route messages. It
   does not alter Mirth Connect channels, transformers, or filters.
2. **Synthetic data only.** No PHI, no production logs, no real client
   data, no real facility names, no real patient identifiers ever enter <!-- noqa: safety -->
   this prototype. Everything in `samples/` is synthetic and clearly
   marked as such.
3. **Reversible by default.** Anything the system *does* do (parse,
   classify, generate text) is read-only. There is no destructive
   action surface.
4. **Auditable.** Every model output is paired with the input it was
   derived from, the prompt template that produced it, and a timestamp.
   Reviewers can reconstruct what was asked and what came back.
5. **Bounded confidence.** The system reports confidence and its own
   uncertainty. It does not claim guaranteed-correct fixes. A
   "high-confidence" hypothesis still requires a human integration
   engineer to confirm before any production action.

## What the model is allowed to do

- Parse synthetic HL7 messages and report structural observations
  (segment order, field counts, malformed delimiters, missing required
  fields).
- Parse synthetic Mirth-style error logs and cluster similar errors.
- Suggest a severity rating on a defined scale (informational, minor,
  major, critical) along with the reasoning.
- Propose root-cause hypotheses ranked by likelihood, each with the
  evidence the model used.
- Suggest validation steps a human can run to confirm or rule out a
  hypothesis.
- Suggest remediation steps in plain language for a human reviewer to
  evaluate.
- Generate a human-review checklist tailored to the message or batch.

## What the model is NOT allowed to do

- Apply changes to a Mirth Connect server.
- Modify HL7 messages and re-send them.
- Connect to real production systems.
- Read or write to any database that contains real patient data. <!-- noqa: safety -->
- Email, page, or notify anyone outside the local demo environment.
- Make claims of regulatory compliance (HIPAA, HITRUST, SOC 2, etc.) on
  behalf of the user. The prototype does not certify anything.
- Replace the judgment of a qualified integration engineer or clinical
  informaticist.

## Review gates

Any output that would inform a real decision passes through these gates
before it leaves the demo environment:

1. **Synthetic-data gate.** The input must be confirmed synthetic
   (either provided in `samples/` or vouched for by the operator).
2. **Self-check gate.** The system reports its own confidence and any
   ambiguity it noticed. Low-confidence outputs are labeled.
3. **Human review gate.** A human reads the output, agrees or
   disagrees, and records the decision. The system does not act on its
   own conclusions.
4. **Public-safety gate.** Before any artifact (logs, exports, demo
   recordings) leaves the developer's machine, it passes
   `scripts/check_public_safety.py`.

## Failure modes the model can have

These are documented up front so users know what to watch for:

- **Hallucinated structure.** The model may describe an HL7 segment
  that isn't there. Mitigation: pair every claim with the line/segment
  it references; reviewers verify.
- **Plausible-but-wrong root cause.** The model may pick the most
  common cause for a symptom even when the actual cause is rare.
  Mitigation: validation steps are part of every hypothesis; humans run
  them.
- **Over-confident severity.** The model may rate something major when
  it is actually minor (or vice versa). Mitigation: severity comes with
  reasoning; reviewers can override.
- **Stale knowledge.** HL7 v2 is stable but vendor implementations
  drift. The model may reference older field semantics. Mitigation:
  hypotheses are validated against the user's actual interface
  configuration before action.

## What this means for buyers

A consulting engagement built on this prototype is sold as **a
structured workflow that helps an integration engineer triage faster**.
It is not sold as "AI that fixes your interfaces." Anyone selling the
latter is misrepresenting the system.
