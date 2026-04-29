# Samples

<!-- SYNTHETIC_DEMO_DATA: this directory contains synthetic test data only. -->

Every file in this directory is **synthetic demo data**. None of it
came from a real interface, a real patient, a real facility, or a
real production system. None of it ever will.

See `../docs/demo_data_policy.md` for the policy this directory
operates under.

## Files

- **`broken_oru.hl7`** — A synthetic HL7 v2 ORU^R01 (observation
  result) message that contains intentional structural defects. Used
  by the demo to exercise the triage workflow's parser-and-classify
  step. All names, identifiers, and dates are clearly fictional.
- **`mirth_error_sample.log`** — A synthetic Mirth-Connect-style error
  log excerpt. Used by the demo to exercise log clustering and
  root-cause hypothesis generation. All hostnames, channel names, and
  identifiers are clearly fictional.

## Rules for adding new sample files

1. The file must include the literal string `SYNTHETIC_DEMO_DATA`
   somewhere in the first 20 lines (a comment line is fine).
2. Names, MRNs, DOBs, phone numbers, emails, hostnames must follow
   the patterns in `docs/demo_data_policy.md`.
3. Run `python ../scripts/check_public_safety.py` from the repo root
   after adding. It must exit 0.
4. Add a short description of the new file to this README.

## Rules for editing existing sample files

Same as above. Re-run the scanner after every edit. If the scanner
flags an error-severity finding, fix the sample, not the scanner.
