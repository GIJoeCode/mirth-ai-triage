#!/usr/bin/env python3
"""
check_public_safety.py
----------------------
Pre-publish safety scanner for the mirth-ai-triage repo.

Walks the repo and flags strings that should NEVER appear in a public
buyer-facing proof asset: real API keys, real PHI, real client/employer
names, real contact info, etc.

Designed to be run before every commit and before every public push.

Usage:
    python scripts/check_public_safety.py
    python scripts/check_public_safety.py --root .
    python scripts/check_public_safety.py --strict        # treat warnings as errors

Exit codes:
    0  - clean, safe to publish
    1  - findings detected (review before publishing)
    2  - script error / bad invocation

Allowlist mechanism:
    * Files containing the marker `SYNTHETIC_DEMO_DATA` (anywhere in the
      first 20 lines) are allowed to use clinical-context terms like
      "patient", "DOB", "MRN", "SSN" because synthetic HL7 samples
      legitimately need them. Hard secrets and real-name patterns are
      ALWAYS flagged regardless of marker.
    * Lines ending with `# noqa: safety` (or `<!-- noqa: safety -->`
      for HTML/markdown) are skipped entirely. Use sparingly.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCANNED_EXTENSIONS = {
    ".md", ".txt", ".py", ".html", ".htm", ".css", ".js", ".ts",
    ".json", ".yml", ".yaml", ".toml", ".ini", ".cfg", ".env",
    ".hl7", ".log", ".sql", ".sh", ".ps1", ".bat",
}

# Files with no extension that should still be scanned
SCANNED_FILENAMES = {
    "Dockerfile", "Makefile", ".env", ".env.local", ".env.production",
}

IGNORED_DIRS = {
    ".git", "__pycache__", "venv", ".venv", "env", ".env.d",
    "node_modules", ".idea", ".vscode", "dist", "build", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "htmlcov", ".tox",
}

SYNTHETIC_MARKER = "SYNTHETIC_DEMO_DATA"
NOQA_PATTERNS = ("# noqa: safety", "<!-- noqa: safety -->", "// noqa: safety")

# Placeholder strings that are explicitly safe to appear anywhere
SAFE_PLACEHOLDERS = {
    "your_api_key_here",
    "your-api-key-here",
    "your_anthropic_api_key_here",
    "your_openai_api_key_here",
    "sk-ant-your-key-here",
    "sk-your-key-here",
    "sk-...",
    "sk-ant-...",
    "example.com",
    "you@example.com",
    "demo@example.com",
    "test@example.com",
    "name@example.com",
    "user@example.com",
    "555-555-5555",
    "(555) 555-5555",
    "555-0100", "555-0101", "555-0102", "555-0103", "555-0104",
    "555-0105", "555-0106", "555-0107", "555-0108", "555-0109",
}

# Names of real organizations/clients/employers that must NEVER appear.
# Keep this list private to the scanner; it's the last line of defense.
# Add more as needed for your situation.
REAL_NAME_DENYLIST = {
    "medaxion",
}

# ---------------------------------------------------------------------------
# Detection rules
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern
    severity: str  # "error" | "warn"
    clinical_context: bool = False  # if True, allowed in SYNTHETIC_DEMO_DATA files
    description: str = ""


HARD_SECRET_RULES: list[Rule] = [
    Rule(
        name="anthropic_api_key",
        pattern=re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"),
        severity="error",
        description="Looks like a real Anthropic API key.",
    ),
    Rule(
        name="openai_api_key",
        pattern=re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
        severity="error",
        description="Looks like a real OpenAI-format API key.",
    ),
    Rule(
        name="anthropic_env_assignment",
        pattern=re.compile(
            r"ANTHROPIC_API_KEY\s*=\s*['\"]?(?!your_|YOUR_|sk-ant-your)[A-Za-z0-9_\-]{10,}",
        ),
        severity="error",
        description="ANTHROPIC_API_KEY assigned to what looks like a real value.",
    ),
    Rule(
        name="openai_env_assignment",
        pattern=re.compile(
            r"OPENAI_API_KEY\s*=\s*['\"]?(?!your_|YOUR_|sk-your)[A-Za-z0-9_\-]{10,}",
        ),
        severity="error",
        description="OPENAI_API_KEY assigned to what looks like a real value.",
    ),
    Rule(
        name="generic_password_assignment",
        pattern=re.compile(
            r"\b(password|passwd|pwd|secret|token)\s*[:=]\s*['\"]?(?!your_|YOUR_|<|\$\{|example|placeholder|changeme|REPLACE)"
            r"[^\s'\"]{6,}",
            re.IGNORECASE,
        ),
        severity="error",
        description="Assignment to password/secret/token with non-placeholder value.",
    ),
    Rule(
        name="aws_access_key",
        pattern=re.compile(r"AKIA[0-9A-Z]{16}"),
        severity="error",
        description="Looks like an AWS access key ID.",
    ),
    Rule(
        name="private_key_block",
        pattern=re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        severity="error",
        description="Embedded private key block.",
    ),
]

CLINICAL_CONTEXT_RULES: list[Rule] = [
    Rule(
        name="phi_term_patient",
        pattern=re.compile(r"\bpatient\b", re.IGNORECASE),
        severity="warn",
        clinical_context=True,
        description="Mentions 'patient' — fine in synthetic samples, review elsewhere.",
    ),
    Rule(
        name="phi_term_dob",
        pattern=re.compile(r"\bDOB\b"),
        severity="warn",
        clinical_context=True,
        description="Mentions 'DOB' — fine in synthetic samples, review elsewhere.",
    ),
    Rule(
        name="phi_term_ssn",
        pattern=re.compile(r"\bSSN\b"),
        severity="warn",
        clinical_context=True,
        description="Mentions 'SSN' — fine in synthetic samples, review elsewhere.",
    ),
    Rule(
        name="phi_term_mrn",
        pattern=re.compile(r"\bMRN\b"),
        severity="warn",
        clinical_context=True,
        description="Mentions 'MRN' — fine in synthetic samples, review elsewhere.",
    ),
    Rule(
        name="ssn_format",
        pattern=re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        severity="error",  # always-bad even in samples
        clinical_context=False,
        description="Looks like a real SSN format. Use 000-00-0000 or 999-99-9999 in samples.",
    ),
]

CONTACT_RULES: list[Rule] = [
    Rule(
        name="phone_number",
        pattern=re.compile(
            r"(?<!\d)(\(\d{3}\)\s?\d{3}-\d{4}|\d{3}-\d{3}-\d{4}|\d{3}\.\d{3}\.\d{4})(?!\d)",
        ),
        severity="warn",
        description="Phone-number-shaped string. Use 555-0100..555-0199 (reserved fictional).",
    ),
    Rule(
        name="email_address",
        pattern=re.compile(
            r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b",
        ),
        severity="warn",
        description="Email address. Should be on example.com / example.org or clear placeholder.",
    ),
]

ALL_RULES = HARD_SECRET_RULES + CLINICAL_CONTEXT_RULES + CONTACT_RULES

# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    path: Path
    line_no: int
    rule: Rule
    snippet: str

    def format(self, root: Path) -> str:
        rel = self.path.relative_to(root) if self.path.is_relative_to(root) else self.path
        sev = "ERROR" if self.rule.severity == "error" else "WARN "
        return (
            f"[{sev}] {rel}:{self.line_no}  ({self.rule.name})\n"
            f"        {self.snippet.strip()[:200]}\n"
            f"        -> {self.rule.description}"
        )


def should_scan(path: Path) -> bool:
    if path.suffix.lower() in SCANNED_EXTENSIONS:
        return True
    if path.name in SCANNED_FILENAMES:
        return True
    return False


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        # Skip the scanner itself — it legitimately contains pattern strings.
        try:
            if path.resolve() == Path(__file__).resolve():
                continue
        except (OSError, ValueError):
            pass
        if should_scan(path):
            yield path


def line_contains_safe_placeholder(line: str) -> bool:
    lowered = line.lower()
    return any(p.lower() in lowered for p in SAFE_PLACEHOLDERS)


def has_synthetic_marker(text: str) -> bool:
    head = "\n".join(text.splitlines()[:20])
    return SYNTHETIC_MARKER in head


def line_has_noqa(line: str) -> bool:
    return any(token in line for token in NOQA_PATTERNS)


def email_is_placeholder(match_text: str) -> bool:
    domain = match_text.split("@", 1)[1].lower()
    placeholder_domains = {"example.com", "example.org", "example.net", "demo.local", "localhost"}
    if domain in placeholder_domains:
        return True
    placeholder_locals = {"you", "demo", "test", "user", "name", "your", "someone"}
    local = match_text.split("@", 1)[0].lower()
    return local in placeholder_locals


def scan_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"[SKIP ] could not read {path}: {e}", file=sys.stderr)
        return findings

    is_synthetic = has_synthetic_marker(text)

    # Real-name denylist (always flags, even with synthetic marker)
    lowered_text = text.lower()
    for name in REAL_NAME_DENYLIST:
        if name.lower() in lowered_text:
            for line_no, line in enumerate(text.splitlines(), 1):
                if name.lower() in line.lower() and not line_has_noqa(line):
                    findings.append(Finding(
                        path=path,
                        line_no=line_no,
                        rule=Rule(
                            name="real_name_denylist",
                            pattern=re.compile(re.escape(name), re.IGNORECASE),
                            severity="error",
                            description=f"Denylisted real-organization name '{name}' must never appear publicly.",
                        ),
                        snippet=line,
                    ))

    for line_no, line in enumerate(text.splitlines(), 1):
        if line_has_noqa(line):
            continue
        for rule in ALL_RULES:
            for match in rule.pattern.finditer(line):
                matched_text = match.group(0)

                # Skip if line contains a known safe placeholder
                if line_contains_safe_placeholder(line):
                    continue

                # Email-specific allowlist
                if rule.name == "email_address" and email_is_placeholder(matched_text):
                    continue

                # Clinical-context terms allowed in synthetic-marker files
                if rule.clinical_context and is_synthetic:
                    continue

                findings.append(Finding(
                    path=path,
                    line_no=line_no,
                    rule=rule,
                    snippet=line,
                ))
    return findings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan repo for unsafe-to-publish strings.")
    parser.add_argument("--root", default=".", help="Repo root to scan (default: cwd).")
    parser.add_argument("--strict", action="store_true",
                        help="Treat WARN findings as errors too.")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Root path does not exist: {root}", file=sys.stderr)
        return 2

    print(f"Scanning {root} ...")
    print("(Files with SYNTHETIC_DEMO_DATA marker are exempt from clinical-term warnings.)\n")

    all_findings: list[Finding] = []
    files_scanned = 0
    for path in iter_files(root):
        files_scanned += 1
        all_findings.extend(scan_file(path))

    errors = [f for f in all_findings if f.rule.severity == "error"]
    warnings = [f for f in all_findings if f.rule.severity == "warn"]

    if all_findings:
        print(f"Findings ({len(errors)} errors, {len(warnings)} warnings):\n")
        for finding in all_findings:
            print(finding.format(root))
            print()
    else:
        print("No findings.")

    print(f"\nScanned {files_scanned} files.")
    print(f"Errors:   {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if errors:
        print("\nFAIL: errors must be resolved before publishing.")
        return 1
    if warnings and args.strict:
        print("\nFAIL (strict mode): warnings must be resolved.")
        return 1
    if warnings:
        print("\nPASS with warnings. Review each warning manually before publishing.")
        return 0

    print("\nPASS: clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
