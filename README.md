# mirth-ai-triage

**An AI-assisted healthcare integration triage workflow prototype.**

A small, opinionated prototype that helps an integration engineer get
from a raw HL7 message and a Mirth-Connect-style error log to a
clear, defensible hypothesis faster. It runs on synthetic data only.
It is human-in-the-loop by design. It does not auto-apply anything.

> If you are looking for an autonomous fixer or a production-ready
> SaaS, this is not that. The shape of this project is intentional —
> see *What this is not* below.

---

## What this is

- A workflow prototype that takes a synthetic HL7 message and/or a
  synthetic Mirth error log and produces:
  1. Structural observations (segment-level, with line references).
  2. A severity rating with reasoning.
  3. Ranked root-cause hypotheses with the evidence each is based on.
  4. Validation steps a human can run to confirm or rule out each
     hypothesis.
  5. Plain-language remediation suggestions for human review.
  6. A per-incident human-review checklist.
- A reference for what a credible AI-assisted integration triage
  workflow looks like — including the safety model, the synthetic-
  data policy, and the consulting offer that wraps around it.

## What this is not

- It is **not** a tool that fixes interface errors automatically.
- It is **not** approved for use against real PHI or real production
  logs.
- It is **not** a replacement for an integration engineer.
- It is **not** a Mirth Connect plugin or a deployed service. It is
  a prototype that runs locally on synthetic input.
- It is **not** certified for HIPAA, HITRUST, SOC 2, or any other
  compliance regime. The prototype makes no compliance claims.

## Human-in-the-loop safety model

The full safety model is documented in
[`docs/SAFETY_MODEL.md`](docs/SAFETY_MODEL.md). The short version:

- **The model proposes. A human decides.** Every output is a
  hypothesis or suggestion paired with the evidence behind it. A
  human integration engineer reviews and decides what to act on.
- **No destructive actions.** The system parses, classifies, and
  generates text. It does not write to Mirth, modify channels,
  re-route messages, or touch any production system.
- **Bounded confidence.** Outputs include the model's own
  uncertainty. Low-confidence outputs are labeled.
- **Auditable.** Every output is paired with the input, the prompt
  template, and a timestamp, so reviewers can reconstruct what was
  asked and what came back.
- **Reversible by default.** Read-only inputs, text-only outputs.

## Synthetic demo data only

This repository operates under a strict synthetic-data-only policy.
No PHI, no production logs, no real client/employer/facility data,
no real patient identifiers, ever, in any file in this repo or any <!-- noqa: safety -->
artifact derived from it.

The full policy is in
[`docs/demo_data_policy.md`](docs/demo_data_policy.md). Highlights:

- Names follow obviously-synthetic patterns
  (`SYNTHETIC^DEMO`, `TEST^PATIENT`). <!-- noqa: safety -->
- Identifiers use `DEMO`/`SYNTH`/`TEST` prefixes.
- Phone numbers use the `555-0100`–`555-0199` reserved-fictional
  range.
- Email addresses use `example.com` / `example.org`.
- Every synthetic file carries the literal marker
  `SYNTHETIC_DEMO_DATA` near the top.

## Setup

**Requirements:** Python 3.11+ and an Anthropic API key
(get one at https://console.anthropic.com/).

```bash
# 1. Clone the repo and change into it
git clone https://github.com/GIJoeCode/mirth-ai-triage.git
cd mirth-ai-triage

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# macOS / Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy the env example and add your key locally
# Windows PowerShell:
copy .env.example .env
# macOS / Linux:
cp .env.example .env

# Then edit .env and set ANTHROPIC_API_KEY=<your key>.
# Do NOT commit .env. The .gitignore already excludes it.
```

## Running the demo

The demo is a small FastAPI backend that serves a single-page web
UI. Start the backend, then open the page in a browser.

```bash
# From the repo root, with the venv activated
cd mvp_demo
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

Then open <http://localhost:8001> in your browser.

The UI loads the synthetic samples from `samples/` so you can walk
through the triage workflow without supplying any data of your own.

## QA / public-safety check

Run the safety scanner before every commit and before every public
share. It walks the repo and flags risky strings (real-looking API
keys, SSN-shaped numbers, real-name denylist entries, non-placeholder <!-- noqa: safety -->
phone numbers and emails, embedded private keys, etc.).

```bash
python scripts/check_public_safety.py
```

Exit codes:

- **0** — clean, safe to publish.
- **1** — findings detected. Review and fix before publishing.
- **2** — script error / bad invocation.

A `--strict` flag treats warnings as errors. Use it in CI if you add
CI later.

The full pre-publish checklist is in
[`docs/QA_CHECKLIST.md`](docs/QA_CHECKLIST.md). Run through it
before making the repo public, posting the walkthrough video, or
sending outreach.

## Consulting / audit offer

This prototype is the proof artifact for a fixed-scope consulting
offer: a redacted HL7/Mirth triage audit for healthcare integration
teams.

The full offer is in
[`docs/OFFER_SHEET.md`](docs/OFFER_SHEET.md). In short:

- **Standard audit:** $2,500 fixed fee, 5 business days after receipt
  of redacted samples.
- **Extended audit:** $5,000+ depending on scope, 7–10 business
  days. Final price confirmed in writing after intake.
- You send a handful of redacted HL7 messages and Mirth log
  excerpts. (PHI removed by you, with a redaction checklist I
  provide.)
- I run the audit using the workflow in this repo and deliver a
  triage workflow review, a root-cause taxonomy of your top failure
  classes, a remediation playbook outline, a human-review checklist,
  and a 45-minute walkthrough call.

I never receive PHI. I do not touch your production systems. The
deliverable is a workflow artifact your team owns.

## Roadmap

Near term:

- [ ] Tighten prompts with more failure-class coverage.
- [ ] Add a small per-hypothesis confidence calibration pass.
- [ ] Add unit tests for the parser and the clustering step.
- [ ] Add example output transcripts in `samples/transcripts/`.

Medium term:

- [ ] Optional second-provider fallback so the prototype isn't
      single-provider-locked.
- [ ] More sample failure classes (ADT mismatches, ACK timeouts,
      transformer errors).
- [ ] A redaction-helper script for buyers to use on their own
      samples before sending.

Explicitly **not** on the roadmap:

- Full SaaS deployment.
- Auto-applying fixes to real interfaces.
- Anything that processes real PHI.
- Compliance certification.

## Repository layout

```
mirth-ai-triage/
├── README.md                       this file
├── requirements.txt                Python dependencies
├── .env.example                    environment-variable template
├── mvp_demo/
│   └── main.py                     FastAPI backend entry point
├── prompts/
│   ├── hl7_triage_prompt.txt       prompt template for HL7 triage
│   └── mirth_analyzer_prompt.txt   prompt template for log analysis
├── samples/
│   ├── README.md                   synthetic-only policy reminder
│   ├── broken_oru.hl7              synthetic HL7 with intentional defects
│   └── mirth_error_sample.log      synthetic Mirth-style error log
├── scripts/
│   └── check_public_safety.py     pre-publish safety scanner
├── docs/
│   ├── OFFER_SHEET.md              consulting/audit offer sheet
│   ├── SAFETY_MODEL.md             human-in-the-loop safety model
│   ├── LOOM_SCRIPT.md              walkthrough video script
│   ├── OUTREACH_MESSAGES.md        outreach message templates
│   ├── QA_CHECKLIST.md             pre-publish review checklist
│   └── demo_data_policy.md         synthetic-data-only policy
└── web/
    └── index.html                  single-page UI served by the backend
```

## Contact

For audit inquiries, contact the repository owner through GitHub
(open an issue on this repository) or via LinkedIn.

## License

No license is granted by default. If you want to use, fork, or
distribute any part of this repository, contact the author first.
